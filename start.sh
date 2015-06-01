#!/bin/sh

if [ ! -f "setup/alienbreed2k5x6.zip" ]
then
  cd setup
  wget "https://web.archive.org/web/20070224083158/http://homepage.ntlworld.com/xavnet/alienbreed/alienbreed2k5x6.zip"
  python2.7 extract.py
  cd ..
fi

python2.7 -m gameengine $@
