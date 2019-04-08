#!/usr/bin/env python

import argparse

# from map_objects.game_map import GameMap
from map_objects.generators.dungeon import generate_dungeon_level

def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'map_file', type=str)

    parser.add_argument(
        '--width', '-w', type=int, default=100)

    parser.add_argument(
        '--height', type=int, default=80)


    return parser.parse_args()

def main():

    args = parse_args()

    newmap = generate_dungeon_level(args.width, args.height, 10, 20)
    newmap.export_txt(args.map_file)
    

if __name__ == '__main__':
    main()
