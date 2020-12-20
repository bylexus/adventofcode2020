import time
import lib
from functools import reduce
import math
import re
from math import ceil, floor
from itertools import product
import operator

###########
# Some ideas how to solve this:
# - I create flipped / rotated versions for all tiles.
# - for each tile, there are 8 versions, 4 rotations for each flip.
#
# - then to test / fill in, I will use a back-tracking algorithm.

class Tile:
    def __init__(self):
        self.pixels = []
        self.nr = 0
        self.versions = []
        self.matching_version = None


    def calc_versions(self):
        self.versions = []
        self.versions.append(rot_right(self.pixels))
        self.versions.append(rot_right(self.versions[-1]))
        self.versions.append(rot_right(self.versions[-1]))
        self.versions.append(rot_right(self.versions[-1]))

        self.versions.append(flip(self.pixels))
        self.versions.append(rot_right(self.versions[-1]))
        self.versions.append(rot_right(self.versions[-1]))
        self.versions.append(rot_right(self.versions[-1]))

def rot_right(matrix):
    out = [[0 for j in range(0,len(matrix))] for i in range(0,len(matrix))]
    for row in range(0, len(matrix)):
        for col in range(0,len(matrix)):
            new_row = col
            new_col = len(matrix)-1-row
            out[new_row][new_col] = matrix[row][col]

    return out

def flip(matrix):
    out = [[0 for j in range(0,len(matrix))] for i in range(0,len(matrix))]
    for row in range(0, len(matrix)):
        for col in range(0,len(matrix)):
            new_row = row
            new_col = len(matrix)-1-col
            out[new_row][new_col] = matrix[row][col]

    return out

def read_input():
    input = lib.readfile('inputs/20-input.txt')
    # input = lib.readfile('inputs/20-input-sample.txt')

    tiles = []
    act_tile = None
    m = re.compile(r'Tile (\d+):')
    for l in input:
        if len(l.strip()):
            g = m.match(l)
            if g:
                if act_tile:
                    tiles.append(act_tile)
                act_tile = Tile()
                act_tile.nr = int(g.group(1))
            else:
                act_tile.pixels.append(list(l))
    tiles.append(act_tile)
    return tiles

def prt_matrix(matrix):
    for l in matrix:
        print("".join(l))

def check_tile(tiles, tiles_in_use, tile_matrix, row, col, edge_len):
    """
    Backtracking algorithm to arrange tiles:
    1. this function works on an ACTUAL tile row/col.
    2. find a next free (not in tiles_in_use) tile
    3. register tile in tiles_in_use
    4. check if any of the tile's versions fits in to left / top edges:
       - go through all tile versions
       - check if the actual version fit to left/top
       - if yes, start recursive backtrack on NEXT (right, bottom) tile, see if there is an arrangement that matches
         - if yes, wow! that's it --> enter in tile_matrix, and register which version was used
         - if no, check next version
       - if no match, remove from tiles_in_use, unregister used version, go to 2.
    5. if no matching tile could be found, remove from tiles_in_use, return a fail

    - tiles_in_use is a set with all tiles that are involved in the actual backtrack check
    - tile_matrix is the final nxm grid of tiles in the correct order, filled in while backtracking
    - row/col is the actual tile's row/col in the final matrix
    - edge_len is the tile_matrix size
    """

def problem1(input):
    print(len(input))
    edge_length = int(math.sqrt(len(input)))

    # start backtracking:

    solution = 0
    print("Solution 1: {}".format(solution))


def problem2(input):
    solution = 0
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
