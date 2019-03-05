# libtcod-tutorial
Tutorial on the use of libtcod for roguelike development

## Prerequisites

### SDL2

`sudo apt install libsdl2-dev`

### libtcod

(requires SDL2)

`wget https://bitbucket.org/libtcod/libtcod/downloads/20171127-libtcod-1.6.4.tbz2`

extract archive

Install required package: `sudo apt install libtool`

Navigate to build/autotools folder

`cd build/autotools`

`autoreconf -i`

`./configure`

`make`

Copy all required files in project root folder

`cp -dr build/autotools/.libs/libtcod.so* data ./`

