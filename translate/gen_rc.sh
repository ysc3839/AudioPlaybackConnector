#!/bin/sh

./po2ymo.py ./source/zh_CN.po ./generated/zh_CN.ymo
./po2ymo.py ./source/zh_TW.po ./generated/zh_TW.ymo

./xamlmin.py ../Menu.xaml ./generated/en_US.xaml
./po2xaml.py ./xaml/zh_CN.po ./generated/zh_CN.xaml -t ../Menu.xaml
#./po2xaml.py ./xaml/zh_TW.po ./generated/zh_TW.xaml -t ../Menu.xaml

echo '#include "../../targetver.h"' > ./generated/translate.rc
echo '#include "windows.h"' >> ./generated/translate.rc

echo 'LANGUAGE LANG_ENGLISH, SUBLANG_ENGLISH_US' >> ./generated/translate.rc
echo '1 XAML "en_US.xaml"' >> ./generated/translate.rc

echo 'LANGUAGE LANG_CHINESE, SUBLANG_CHINESE_SIMPLIFIED' >> ./generated/translate.rc
echo '1 XAML "zh_CN.xaml"' >> ./generated/translate.rc
echo '1 YMO "zh_CN.ymo"' >> ./generated/translate.rc

echo 'LANGUAGE LANG_CHINESE, SUBLANG_CHINESE_TRADITIONAL' >> ./generated/translate.rc
#echo '1 XAML "zh_TW.xaml"' >> ./generated/translate.rc
echo '1 YMO "zh_TW.ymo"' >> ./generated/translate.rc
