import time
import lib
import functools
import math
import re
from math import ceil, floor
import itertools


def read_input():
    # return list(map(list,lib.remove_empty(lib.readfile('inputs/11-input-sample.txt'))))
    # return a 2d array of all seats:
    return list(map(list,lib.remove_empty(lib.readfile('inputs/11-input.txt'))))


def can_see(seats, x, y, dirs, view_seat, whole_line=True):
    """
    Checks if a given view_seat can see the specified seat (view_seat) in a specific direction (dirs).
    either directly beneath it, or in the whole line.

    seats: the 2d array of seats[row][col]
    x, y: the coordinate of the seat to check
    dirs: a direction vector to look in (e.g. (-1,0) means: look left)
    view_seat: the char to look for (e.g. '#')
    whole_line: If true, we look further in the given direction than only one seat: we look
      the whole line for a seat, as long as sight is not blocked
    """
    dx = dirs[1]
    dy = dirs[0]
    x = x + dx
    y = y + dy

    while y >= 0 and y < len(seats) and x >= 0 and x < len(seats[y]):
        if seats[y][x] == view_seat:
            return True
        # if another thing (but not the empty floor) is found, sight is blocked
        if seats[y][x] not in ['.', view_seat]:
            return False

        # if we only look one block in this direction, we stop here already:
        if not whole_line:
            return False
        # move further down the line:
        x = x + dx
        y = y + dy
    # reached the end, not any seat here:
    return False


def calc_seat(result, seats, x, y, whole_line=False, occupy_threshold=4):
    """
    calcs the new value of a single seat, using an array for READ, and an other array
    for WRITE (aka double buffering), so that we can first change the full state based on the
    old state, before applying the new state.
    """
    s = seats[y][x]
    tot = 0
    dirs = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
        (1, 1)
    ]
    if s == 'L':
        for d in dirs:
            if can_see(seats, x, y, d, '#', whole_line=whole_line):
                return False
        result[y][x] = '#'
        return True
    elif s == '#':
        for d in dirs:
            if can_see(seats, x, y, d, '#', whole_line=whole_line):
                tot += 1
        if tot >= occupy_threshold:
            result[y][x] = 'L'
            return True
    return False


def prt(seats):
    for i in seats:
        print("{}".format("".join(i)))
    print()


def copy_seats(seats):
    return [row[:] for row in seats]


def count_seats(seats, s):
    return sum([row.count(s) for row in seats])


def problem1(seats):
    changed = True
    while changed == True:
        changed = False
        # double-buffer approach: we need to set the new state on a separate array,
        # as the actual state is fact for calculating the new seats:
        cpy = copy_seats(seats)
        for y in range(0, len(seats)):
            for x in range(0, len(seats[y])):
                res = calc_seat(cpy, seats, x, y,
                                whole_line=False, occupy_threshold=4)
                if res:
                    changed = True
        # now apply the new state from the double-buffered copy:
        seats = copy_seats(cpy)

    solution = count_seats(seats, '#')
    print("Solution 1: {}".format(solution))


def problem2(seats):
    changed = True
    while changed == True:
        changed = False
        # double-buffer approach: we need to set the new state on a separate array,
        # as the actual state is fact for calculating the new seats:
        cpy = copy_seats(seats)
        for y in range(0, len(seats)):
            for x in range(0, len(seats[y])):
                res = calc_seat(cpy, seats, x, y,
                                whole_line=True, occupy_threshold=5)
                if res:
                    changed = True
        # now apply the new state from the double-buffered copy:
        seats = copy_seats(cpy)

    solution = count_seats(seats, '#')
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
