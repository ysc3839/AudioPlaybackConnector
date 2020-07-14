#pragma once

void DrawSvgTohDC(std::string_view svg, HDC hdc, LONG width, LONG height, const D2D1_COLOR_F& color)
{
	winrt::com_ptr<ID2D1Factory> factory;
	winrt::check_hresult(D2D1CreateFactory(D2D1_FACTORY_TYPE_SINGLE_THREADED, factory.put()));

	D2D1_RENDER_TARGET_PROPERTIES props = {
		.type = D2D1_RENDER_TARGET_TYPE_DEFAULT,
		.pixelFormat = {
			.format = DXGI_FORMAT_B8G8R8A8_UNORM,
			.alphaMode = D2D1_ALPHA_MODE_PREMULTIPLIED
		},
		.dpiX = 0, .dpiY = 0,
		.usage = D2D1_RENDER_TARGET_USAGE_NONE,
		.minLevel = D2D1_FEATURE_LEVEL_DEFAULT
	};
	winrt::com_ptr<ID2D1DCRenderTarget> gdiDCRT;
	winrt::check_hresult(factory->CreateDCRenderTarget(&props, gdiDCRT.put()));

	RECT rect = { 0, 0, width, height };
	winrt::check_hresult(gdiDCRT->BindDC(hdc, &rect));

	auto istream = SHCreateMemStream(reinterpret_cast<const BYTE*>(svg.data()), static_cast<UINT>(svg.size()));
	THROW_IF_NULL_ALLOC(istream);
	winrt::com_ptr<IStream> stream(istream, winrt::take_ownership_from_abi);

	auto dc = gdiDCRT.as<ID2D1DeviceContext5>();
	dc->SetAntialiasMode(D2D1_ANTIALIAS_MODE_ALIASED);

	winrt::com_ptr<ID2D1SvgDocument> svgDoc;
	winrt::check_hresult(dc->CreateSvgDocument(stream.get(), { static_cast<FLOAT>(width), static_cast<FLOAT>(height) }, svgDoc.put()));

	winrt::com_ptr<ID2D1SvgElement> svgRoot;
	svgDoc->GetRoot(svgRoot.put());
	svgRoot->SetAttributeValue(L"fill", color);

	dc->BeginDraw();
	dc->DrawSvgDocument(svgDoc.get());
	dc->EndDraw();
}

auto CreateDIB(HDC hdc, LONG width, LONG height, WORD bitCount)
{
	BITMAPINFO bmi = { .bmiHeader = {
		.biSize = sizeof(BITMAPINFOHEADER),
		.biWidth = width,
		.biHeight = height,
		.biPlanes = 1,
		.biBitCount = bitCount,
		.biCompression = BI_RGB,
	} };
	return wil::unique_hbitmap(CreateDIBSection(hdc, &bmi, DIB_RGB_COLORS, nullptr, nullptr, 0));
}

HICON SvgTohIcon(std::string_view svg, LONG width, LONG height, const D2D1_COLOR_F& color)
{
	wil::unique_hdc hdc(CreateCompatibleDC(nullptr));
	THROW_IF_NULL_ALLOC(hdc);

	auto hBitmap = CreateDIB(hdc.get(), width, height, 32);
	THROW_IF_NULL_ALLOC(hBitmap);
	auto hBitmapMask = CreateDIB(hdc.get(), width, height, 1);
	THROW_IF_NULL_ALLOC(hBitmapMask);

	auto select = wil::SelectObject(hdc.get(), hBitmap.get());
	DrawSvgTohDC(svg, hdc.get(), width, height, color);

	ICONINFO iconInfo = {
		.fIcon = TRUE,
		.hbmMask = hBitmapMask.get(),
		.hbmColor = hBitmap.get()
	};
	HICON hIcon = CreateIconIndirect(&iconInfo);
	THROW_LAST_ERROR_IF_NULL(hIcon);

	return hIcon;
}
