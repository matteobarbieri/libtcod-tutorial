#!/usr/bin/env python

import argparse

from PIL import Image, ImageDraw

def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'map_file', type=str)

    parser.add_argument(
        'image_file', type=str)

    return parser.parse_args()

def main():

    args = parse_args()

    map_array = list()

    with open(args.map_file, 'r') as mf:
        # map_row = mf.readline().strip()
        map_row = mf.readline().strip("\n")

        while(len(map_row) > 0):
            map_array.append(map_row)
            # map_row = mf.readline().strip()
            map_row = mf.readline().strip("\n")

    map_width = len(map_array[0])
    map_heigth = len(map_array)

    tile_size = 10

    img = Image.new(
        'RGB', (map_width*tile_size, map_heigth*tile_size), 
        color = 'black')
    
    draw = ImageDraw.Draw(img)

    for y in range(map_heigth):
        for x in range(map_width):

            img_x1 = x * tile_size
            img_x2 = (x + 1) * tile_size
            img_y1 = y * tile_size
            img_y2 = (y + 1) * tile_size

            c = map_array[y][x]
            if c == '.':
                draw.rectangle(
                    [img_x1, img_y1, img_x2, img_y2], 'white')
            elif c == '#':
                draw.rectangle(
                    [img_x1, img_y1, img_x2, img_y2], '#777777')
            elif c == '+':
                draw.rectangle(
                    [img_x1, img_y1, img_x2, img_y2], '#FF9800')

    img.save(args.image_file)

if __name__ == '__main__':
    main()
