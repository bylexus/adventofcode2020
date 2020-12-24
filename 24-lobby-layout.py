import time
import lib
from functools import reduce
import math
import re
from math import ceil, floor
from itertools import product
from collections import deque
import operator


tile_coords = dict()
walk_offsets = {
    'w': (-2, 0),
    'e': (2, 0),
    'nw': (-1, -1),
    'ne': (1, -1),
    'sw': (-1, 1),
    'se': (1, 1),
}


def read_input():
    input = lib.remove_empty(lib.readfile('inputs/24-input.txt'))
    # input = lib.remove_empty(lib.readfile('inputs/24-input-sample.txt'))

    return input


def walk(start_coord, dirs):
    global walk_offsets

    # see:
    # https://www.redblobgames.com/grids/hexagons/#coordinates-doubled
    # I use the doubled coordinate system, easier to calculate
    # (0,0) is (x, y)
    # we have a horizontal layout, means we have the dirs:
    # w, nw, ne, e, se, sw
    act_coord = (0, 0)

    for d in dirs:
        act_coord = (
            act_coord[0] + walk_offsets[d][0],
            act_coord[1] + walk_offsets[d][1],
        )
    return act_coord


def problem1(input):
    global tile_coords

    m = re.compile(r"(ne|nw|se|sw|e|w)")
    tile_coords = dict()
    for i in input:
        dirs = m.findall(i)
        tile_coord = walk((0, 0), dirs)
        tile = tile_coords.get(tile_coord, 1)  # 1 means white, 0 means black
        tile_coords[tile_coord] = (tile + 1) % 2  # flip

    solution = list(tile_coords.values()).count(0)
    print("Solution 1: {}".format(solution))


def flip_tile(coord, value, input_tiles):
    global walk_offsets
    black_count = 0
    for nc in walk_offsets.values():
        ncoord = (coord[0] + nc[0], coord[1] + nc[1])
        if input_tiles.get(ncoord, 1) == 0:
            black_count += 1
    if value == 0 and (black_count == 0 or black_count > 2):
        return 1
    if value == 1 and black_count == 2:
        return 0
    return value


def problem2(input):
    global tile_coords
    global walk_offsets

    for i in range(0, 100):  # a loop is a day
        new_coords = dict()
        # process all black tiles
        for coords, val in tile_coords.items():
            if val == 0:
                new_coords[coords] = flip_tile(coords, val, tile_coords)

        # then process all white neighbours of black tiles:
        for coords, val in tile_coords.items():
            if val == 0:
                # go through all neightbours of the black tile:
                for nc in walk_offsets.values():
                    ncoord = (coords[0] + nc[0], coords[1] + nc[1])
                    if ncoord in new_coords.keys():
                        continue
                    # if the neighbour is white, process:
                    if tile_coords.get(ncoord, 1) == 1:
                        new_coords[ncoord] = flip_tile(ncoord, 1, tile_coords)

        # then switch coords dict:
        tile_coords = new_coords

    solution = list(tile_coords.values()).count(0)
    print("Solution 2: {}".format(solution))


def main():
    title = "Advent of Code 2020!"
    print("{title}\n{line}\n\n".format(title=title, line="="*len(title)))

    input = read_input()

    t1 = lib.measure(lambda: problem1(input))
    print("Problem 1 took {:.6f}s to solve.\n\n".format(t1))

    t2 = lib.measure(lambda: problem2(input))
    print("Problem 2 took {:.6f}s to solve.".format(t2))


if __name__ == "__main__":
    main()
