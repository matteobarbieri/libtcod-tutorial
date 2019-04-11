#!/usr/bin/env python

import argparse

import random
import sys

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

    parser.add_argument(
        '--seed', type=int)


    return parser.parse_args()

def main():

    args = parse_args()

    if args.seed is None:
        args.seed = random.randrange(sys.maxsize)

    # Initialize random number generator
    print("Seed was:", args.seed)
    random.seed(args.seed)

    newmap = generate_dungeon_level(args.width, args.height, 10, 20)
    newmap.export_txt(args.map_file)
    

if __name__ == '__main__':
    main()
