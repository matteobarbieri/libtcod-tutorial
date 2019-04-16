#!/bin/bash

python create_map.py \
	maps_txt/m.txt \
	--seed 8254736048118751350 \
	-w 80 --height 80

python preview_map.py \
	maps_txt/m.txt maps_txt/m.png

#INFO:root:Trying to connect a Junction and a Room (from (45, 48) to (56, 44))
#INFO:root:Trying to connect a Junction and a Room (from (68, 48) to (64, 59))
