import time
import lib
from functools import reduce
import math
import re
from math import ceil, floor
from itertools import product
import operator

tile_matrix = None

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
        """
        calc all possible rotated / flipped versions of the initial pixel image:
        """
        self.versions = []
        self.versions.append(rot_right(self.pixels))
        self.versions.append(rot_right(self.versions[-1]))
        self.versions.append(rot_right(self.versions[-1]))
        self.versions.append(rot_right(self.versions[-1]))

        self.versions.append(flip(self.pixels))
        self.versions.append(rot_right(self.versions[-1]))
        self.versions.append(rot_right(self.versions[-1]))
        self.versions.append(rot_right(self.versions[-1]))

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


def rot_right(matrix):
    """
    Rotates a square (!) matrix right, returns a NEW matrix
    """
    out = [[0 for j in range(0,len(matrix))] for i in range(0,len(matrix))]
    for row in range(0, len(matrix)):
        for col in range(0,len(matrix)):
            new_row = col
            new_col = len(matrix)-1-row
            out[new_row][new_col] = matrix[row][col]

    return out

def flip(matrix):
    """
    Flips a square(!) matrix left/right, returns a NEW matrix
    """
    out = [[0 for j in range(0,len(matrix))] for i in range(0,len(matrix))]
    for row in range(0, len(matrix)):
        for col in range(0,len(matrix)):
            new_row = row
            new_col = len(matrix)-1-col
            out[new_row][new_col] = matrix[row][col]

    return out

def prt_matrix(matrix):
    """
    pretty-prints a matrix
    """
    for l in matrix:
        print("".join(l))

def check_left_fit(left_tile, right_tile):
    """
    check if the right/left border of the given pixel arrays match
    """
    left_version = left_tile.versions[left_tile.actual_version_index]
    right_version = right_tile.versions[right_tile.actual_version_index]
    length = len(left_version[0])
    for ri in range(0, length):
        if left_version[ri][length-1] != right_version[ri][0]:
            return False
    return True

def check_top_fit(top_tile, bottom_tile):
    """
    check if the top/bottom border of the given pixel arrays match
    """
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
    global tile_matrix

    tiles = input

    edge_length = int(math.sqrt(len(input)))
    tile_matrix = [[None for j in range(0,edge_length)] for i in range(0,edge_length)]
    tiles_in_use = set()

    # start backtracking:
    check_tile(tiles, tiles_in_use, tile_matrix, 0, 0, edge_length)

    solution = reduce(operator.mul, [
        tile_matrix[0][0].nr,
        tile_matrix[0][edge_length-1].nr,
        tile_matrix[edge_length-1][0].nr,
        tile_matrix[edge_length-1][edge_length-1].nr,
    ])
    print("Solution 1: {}".format(solution))

def mark_sea_monsters(image, sea_monster):
    """
    search for the sea monster pattern in the given image.
    marks all sea monster tiles with 'O' in the original image,
    and returns the monster count.
    sea_monster is a list of relative coordinate tuples that marks the
    sea monsters body.
    """
    monster_count = 0
    for r in range(0,len(image)):
        for c in range(0,len(image[r])):
            found = True
            for coords in sea_monster:
                offset_r = r + coords[0]
                offset_c = c + coords[1]
                if offset_r >= len(image) or offset_c >= len(image[r]):
                    found = False
                    break
                if image[offset_r][offset_c] != '#':
                    found = False
                    break
            if found:
                monster_count += 1
                for coords in sea_monster:
                    offset_r = r + coords[0]
                    offset_c = c + coords[1]
                    image[offset_r][offset_c] = 'O'
    return monster_count

def count_roughness(image):
    """
    counts all '#' tiles in the image
    """
    return sum([l.count('#') for l in image])

def problem2(input):
    global tile_matrix
    matrix_len = len(tile_matrix)

    # we need a full "image" array, that has the following side length:
    # n tiles matrix length with m-2 pixels each (a tile has 10x10 pixels in the input, so it would be 8)
    # --> matrix_len * (len(matrix[0].pixels)-2) --> 12 * 8 = 96 for the final input
    img_width = matrix_len * (len(tile_matrix[0][0].pixels) - 2)
    image = [[None for j in range(0,img_width)] for i in range(0,img_width)]
    # create a full image with all (seam-less) tiles in one big image:
    for ri,row in enumerate(tile_matrix):
        for ci,tile in enumerate(row):
            pixels = tile.versions[tile.matching_version_index]
            plen = len(pixels) - 2
            for pri in range(1,len(pixels)-1):
                for pci in range(1,len(pixels)-1):
                    px = pixels[pri][pci]
                    dest_row = ri * plen + pri - 1
                    dest_col = ci * plen + pci - 1
                    image[dest_row][dest_col] = px

    # define sea monster's coordinates:
    sea_monster = [
        (0,18),
        (1,0),(1,5),(1,6),(1,11),(1,12),(1,17),(1,18),(1,19),
        (2,1),(2,4),(2,7),(2,10),(2,13),(2,16)
    ]

    # find the one rotation / flip position that actually HAS sea monsters:
    monster_count = 0
    rot_count = 0
    solution = 0
    while not monster_count:
        monster_count = mark_sea_monsters(image, sea_monster)
        if not monster_count:
            if rot_count < 4:
                image = rot_right(image)
                rot_count += 1
            else:
                rot_count = 0
                image = flip(image)
        else:
            solution = count_roughness(image)
            prt_matrix(image)
            print("Booh! {} sea monsters found in that rough waters!".format(monster_count))
            break

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
