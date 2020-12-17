import time
import lib
import functools
import math
import re
from math import ceil, floor
from itertools import product
import operator

def read_input():
    # input = list(map(list,lib.remove_empty(lib.readfile('inputs/17-input-sample.txt'))))
    input = list(map(list,lib.remove_empty(lib.readfile('inputs/17-input.txt'))))
    return input

def calc_coord_state(coords, coord, dims = 3):
    neighbours = list(product([0,1,-1],repeat=dims))
    state = coords.get(coord, '.')
    active_neighbours = 0
    zero_tuple = (0,)*dims
    for nc in neighbours:
        if nc == zero_tuple:
            continue
        # neighbour coordinates:
        real_nc = tuple(map(operator.add, coord, nc))
        neighbour_state = coords.get(real_nc, '.')
        if neighbour_state == '#':
            active_neighbours += 1
    if state == '#' and active_neighbours not in [2,3]:
        state = '.'
    elif active_neighbours == 3:
        state = '#'
    return state

def calc_new_state(coords, dims = 3):
    new_state = coords.copy()
    neighbours = list(product([0,1,-1],repeat=dims))
    for c,state in coords.items():
        # calc new value of act coord
        new_state[c] = calc_coord_state(coords, c, dims)
        # ... and also new value of all neighbour coords, if not
        # yet present:
        for nc in neighbours:
            # neighbour coordinates:
            real_nc = tuple(map(operator.add, c, nc))
            if not coords.get(real_nc):
                new_state[real_nc] = calc_coord_state(coords, real_nc, dims)
    return new_state

def problem1(input):
    # coords are stored in a dict()
    # key: tuple of coords: (x,y,z)
    # value: state ('.', '#')
    # unknown coords: inactive ('.')
    coords = dict()
    for y,line in enumerate(input):
        for x,col in enumerate(line):
            coords[(x,y,0)] = col

    # do the calc cycles:
    for i in range(0, 6):
        coords = calc_new_state(coords)

    # count active:
    active = 0
    for state in coords.values():
        if state == '#':
            active += 1
    
    solution = active

    print("Solution 1: {}".format(solution))

def problem2(input):
    # coords are stored in a dict():
    # key: tuple of coords: (x,y,z,w)
    # value: state ('.', '#')
    # unknown coords: inactive ('.')
    coords = dict()
    for y,line in enumerate(input):
        for x,col in enumerate(line):
            coords[(x,y,0,0)] = col

    for i in range(0, 6):
        coords = calc_new_state(coords, dims=4)

    # count active:
    active = 0
    for state in coords.values():
        if state == '#':
            active += 1
    
    solution = active

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