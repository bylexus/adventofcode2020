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
# - then to test / fill in, I will use a back-tracking algorithm.

class Tile:
    def __init__(self):
        self.pixels = []
        self.nr = 0
        self.versions = []
        self.matching_version_index = None
        self.actual_version_index = None


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
    for t in tiles:
        t.calc_versions()
    return tiles

def prt_matrix(matrix):
    for l in matrix:
        print("".join(l))

def check_left_fit(left_tile, right_tile):
    left_version = left_tile.versions[left_tile.actual_version_index]
    right_version = right_tile.versions[right_tile.actual_version_index]
    length = len(left_version[0])
    for ri in range(0, length):
        if left_version[ri][length-1] != right_version[ri][0]:
            return False
    return True

def check_top_fit(top_tile, bottom_tile):
    top_version = top_tile.versions[top_tile.actual_version_index]
    bottom_version = bottom_tile.versions[bottom_tile.actual_version_index]
    length = len(top_version[0])
    for ci in range(0, length):
        if top_version[length-1][ci] != bottom_version[0][ci]:
            return False
    return True

def check_tile(tiles, tiles_in_use, tile_matrix, row, col, edge_len):
    """
    Backtracking algorithm to arrange tiles:
    This function works on an ACTUAL tile row/col.
    1. find a next free (not in tiles_in_use) tile
    2. register tile in tiles_in_use, and in tile_matrix
    3. check if any of the tile's versions fits in to left / top edges:
       - go through all tile versions
       - check if the actual version fit to left/top
       - if yes, start recursive backtrack on NEXT (right, bottom) tile, see if there is an arrangement that matches
         - if yes, wow! that's it --> enter in tile_matrix, and register which version was used
         - if no, check next version
       - if no match, remove from tiles_in_use, remove from tile_matrix, unregister used version, go to 1.
    4. if no matching tile could be found, remove from tiles_in_use and tile_matrix return a fail (backtrack)

    - tiles_in_use is a set with all tiles that are involved in the actual backtrack check
    - tile_matrix is the final nxm grid of tiles in the correct order, filled in while backtracking
    - row/col is the actual tile's row/col in the final matrix
    - edge_len is the tile_matrix size
    """

    if row >= edge_len or col >= edge_len:
        return True

    # 1. for each free tile:
    for tile in tiles:
        if tile.nr in tiles_in_use:
            continue
        # 2. ok, found one, register in use:
        tiles_in_use.add(tile.nr)
        tile_matrix[row][col] = tile

        # 3. loop through all versions:
        for vi,version in enumerate(tile.versions):
            # check if the actual tile version fits to the left neightbour:
            tile.actual_version_index = vi
            left_fit = True
            top_fit = True
            if col > 0:
                left_fit = check_left_fit(tile_matrix[row][col-1], tile)
            if row > 0:
                top_fit = check_top_fit(tile_matrix[row-1][col], tile)
            # print("{}:{}: fit in: {}".format(tile.nr, tile.actual_version_index, left_fit and top_fit))

            if left_fit and top_fit:
                # ok, we found a matching version, now check recursively for the next tiles:
                next_col = (col + 1) % edge_len
                next_row = (edge_len*row + col + 1) // edge_len
                if check_tile(tiles, tiles_in_use, tile_matrix, next_row, next_col, edge_len):
                    tile.matching_version_index = vi
                    return True
            # no fit for version, check next version:
            tile.actual_version_index = None
        # no version could be found, reset/backtrack:
        tile_matrix[row][col] = None
        tiles_in_use.remove(tile.nr)


    # if all else failed:
    return False

def problem1(input):
    print(len(input))
    tiles = input

    edge_length = int(math.sqrt(len(input)))
    tile_matrix = [[None for j in range(0,edge_length)] for i in range(0,edge_length)]
    tiles_in_use = set()

    # start backtracking:
    ret = check_tile(tiles, tiles_in_use, tile_matrix, 0, 0, edge_length)
    for ri,row in enumerate(tile_matrix):
        for ci, tile in enumerate(row):
            print("{} ".format(tile.nr), end="")
        print()
    print(ret)

    solution = reduce(operator.mul, [
        tile_matrix[0][0].nr,
        tile_matrix[0][edge_length-1].nr,
        tile_matrix[edge_length-1][0].nr,
        tile_matrix[edge_length-1][edge_length-1].nr,
    ])
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
