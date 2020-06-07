#pragma once

constexpr uint32_t FNV1_32_INIT = 0x811c9dc5;
constexpr uint32_t FNV_32_PRIME = 0x01000193;

uint32_t fnv1a_32(const void* buf, size_t len, uint32_t hval = FNV1_32_INIT)
{
	auto p = reinterpret_cast<const uint8_t*>(buf);

	for (size_t i = 0; i < len; ++i) {
		hval ^= static_cast<uint32_t>(p[i]);
		hval *= FNV_32_PRIME;
	}

	return hval;
}
