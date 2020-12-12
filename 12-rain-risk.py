import time
import lib
import functools
import math
import re
from math import ceil, floor
import itertools


def read_input():
    # return list(map(list,lib.remove_empty(lib.readfile('inputs/12-input-sample.txt'))))
    # return a 2d array of all seats:
    # return list(lib.remove_empty(lib.readfile('inputs/12-input-sample.txt')))
    return list(lib.remove_empty(lib.readfile('inputs/12-input.txt')))


def problem1(input):
    # coordinates are pairs of [y, x]:
    # y for N/S (-1 means up north, 1 means down south)
    # x for E/W (-1 means west, 1 means east)
    heading_map = {
        'N': (-1,0),
        'S': (1,0),
        'W': (0,-1),
        'E': (0,1)
    }

    coord = [0,0]
    # heading is a vector with max +/- 1, indicating the dir
    heading = [0, 1]
    for i in input:
        instr = i[0]
        nr = int(i[1:])
        if instr in ['N','S','E','W']:
            coord[0] += heading_map[instr][0] * nr
            coord[1] += heading_map[instr][1] * nr
        elif instr == 'L':
            for r in range(0,nr // 90):
                tmp_y = heading[0]
                tmp_x = heading[1]
                # x becomes y
                heading[1] = tmp_y
                # y becomes negative x
                heading[0] = -tmp_x
        elif instr == 'R':
            for r in range(0,nr // 90):
                tmp_y = heading[0]
                tmp_x = heading[1]
                # x becomes negative y
                heading[1] = -tmp_y
                # y becomes x
                heading[0] = tmp_x
        elif instr == 'F':
            coord[0] += heading[0] * nr
            coord[1] += heading[1] * nr
    
    print(coord)


    solution = sum(map(abs,coord))
    print("Solution 1: {}".format(solution))


def problem2(input):
    # coordinates are pairs of [y, x]:
    # y for N/S (-1 means up north, 1 means down south)
    # x for E/W (-1 means west, 1 means east)
    heading_map = {
        'N': (-1,0),
        'S': (1,0),
        'W': (0,-1),
        'E': (0,1)
    }

    coord_ship = [0,0]
    coord_wp = [-1,10]
    for i in input:
        instr = i[0]
        nr = int(i[1:])
        if instr in ['N','S','E','W']:
            # move the waypoint:
            vec = heading_map[instr]
            coord_wp[0] += vec[0] * nr
            coord_wp[1] += vec[1] * nr
        elif instr == 'L':
            # rotate the waypoint to the left:
            for r in range(0,nr // 90):
                tmp_y = coord_wp[0]
                tmp_x = coord_wp[1]
                # x becomes y
                coord_wp[1] = tmp_y
                # y becomes negative x
                coord_wp[0] = -tmp_x
        elif instr == 'R':
            # rotate the waypoint to the right:
            for r in range(0,nr // 90):
                tmp_y = coord_wp[0]
                tmp_x = coord_wp[1]
                # x becomes negative y
                coord_wp[1] = -tmp_y
                # y becomes x
                coord_wp[0] = tmp_x
        elif instr == 'F':
            # forward the ship n times the waypoint vector
            coord_ship[0] += coord_wp[0] * nr
            coord_ship[1] += coord_wp[1] * nr
    
    print(coord_ship)

    solution = sum(map(abs,coord_ship))
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
