#!/bin/bash

# Install SDL2 and libtool

sudo apt install -y \
	libsdl2-dev \
	libtool

# Download libtcod
LIBTCOD=20171127-libtcod-1.6.4

wget https://bitbucket.org/libtcod/libtcod/downloads/${LIBTCOD}.tbz2

# Extract archive
tar -xjvf ${LIBTCOD}.tbz2

# Build libtcod

CURRENT_FOLDER=`pwd`

cd $LIBTCOD/build/autotools
autoreconf -i
./configure
make -j4

# Back to project root folder
cd $CURRENT_FOLDER

# Copy python package, data folder and compiled libs
cp -dr \
	$LIBTCOD/data \
	$LIBTCOD/python/libtcodpy \
	./

# Put .so files in python package folder
cp $LIBTCOD/build/autotools/.libs/libtcod.so* libtcodpy/

# Remove archive
rm $LIBTCOD.tbz2
