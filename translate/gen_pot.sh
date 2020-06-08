#!/bin/sh

FILES="AudioPlaybackConnector.cpp"

COPYRIGHT_HOLDER="Richard Yu <yurichard3839@gmail.com>"
PKG_NAME="AudioPlaybackConnector"

cd ..
xgettext -o translate/source/messages.pot --c++ --add-comments=/ --keyword=_ --keyword=C_:1c,2 --copyright-holder="$COPYRIGHT_HOLDER" --package-name="$PKG_NAME" $FILES
