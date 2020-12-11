import time
import lib
import functools
import math
import re
from math import ceil, floor
import itertools


def read_input():
    lines = list(lib.remove_empty(lib.readfile('inputs/11-input-sample.txt')))
    lines = list(lib.remove_empty(lib.readfile('inputs/11-input.txt')))
    ret = []
    for i in lines:
        ret.append(list(i))
    return ret


def calc_seat(result, seats, x, y):
    s = seats[y][x]
    tot = 0
    if s == 'L':
        #up
        if y > 0 and seats[y-1][x] == '#':
            return False
        # down
        if y < len(seats)-1 and seats[y+1][x] == '#':
            return False
        # left
        if x > 0 and seats[y][x-1] == '#':
            return False
        # right
        if x < len(seats[y])-1 and seats[y][x+1] == '#':
            return False
        # top left
        if y > 0 and x > 0  and seats[y-1][x-1] == '#':
            return False
        # top right
        if y > 0 and x < len(seats[y])-1  and seats[y-1][x+1] == '#':
            return False
        # bottom left
        if y < len(seats)-1 and x > 0  and seats[y+1][x-1] == '#':
            return False
        # bottom left
        if y < len(seats)-1 and x < len(seats[y])-1  and  seats[y+1][x+1] == '#':
            return False
        result[y][x] = '#'
        return True
    elif s == '#':
        #up
        if y > 0 and seats[y-1][x] == '#':
            tot += 1 
        # down
        if y < len(seats)-1 and seats[y+1][x] == '#':
            tot += 1 
        # left
        if x > 0 and seats[y][x-1] == '#':
            tot += 1 
        # right
        if x < len(seats[y])-1 and seats[y][x+1] == '#':
            tot += 1 
        # top left
        if y > 0 and x > 0  and seats[y-1][x-1] == '#':
            tot += 1 
        # top right
        if y > 0 and x < len(seats[y])-1  and seats[y-1][x+1] == '#':
            tot += 1 
        # bottom left
        if y < len(seats)-1 and x > 0  and seats[y+1][x-1] == '#':
            tot += 1 
        # bottom left
        if y < len(seats)-1 and x < len(seats[y])-1  and  seats[y+1][x+1] == '#':
            tot += 1 
        if tot >= 4:
            result[y][x] = 'L'
            return True
    return False

def can_see(seats, x, y, dirs, seat):
    dx = dirs[1]
    dy = dirs[0]
    x = x + dx
    y = y + dy
    while y >= 0 and y < len(seats) and x >= 0 and x < len(seats[y]):
        if seats[y][x] == seat:
            return True
        if seats[y][x] not in ['.',seat]:
            return False
        x = x + dx
        y = y + dy
    return False

def calc_seat2(result, seats, x, y):
    s = seats[y][x]
    tot = 0
    if s == 'L':
        #up
        if can_see(seats, x, y, (-1,0), '#'):
            return False
        # down
        if can_see(seats, x, y, (1,0), '#'):
            return False
        # left
        if can_see(seats, x, y, (0,-1), '#'):
            return False
        # right
        if can_see(seats, x, y, (0,1), '#'):
            return False
        # top left
        if can_see(seats, x, y, (-1,-1), '#'):
            return False
        # top right
        if can_see(seats, x, y, (-1,1), '#'):
            return False
        # bottom left
        if can_see(seats, x, y, (1,-1), '#'):
            return False
        # bottom left
        if can_see(seats, x, y, (1,1), '#'):
            return False
        result[y][x] = '#'
        return True
    elif s == '#':
        #up
        if can_see(seats, x, y, (-1,0), '#'):
            tot += 1 
        # down
        if can_see(seats, x, y, (1,0), '#'):
            tot += 1 
        # left
        if can_see(seats, x, y, (0,-1), '#'):
            tot += 1 
        # right
        if can_see(seats, x, y, (0,1), '#'):
            tot += 1 
        # top left
        if can_see(seats, x, y, (-1, -1), '#'):
            tot += 1 
        # top right
        if can_see(seats, x, y, (-1, 1), '#'):
            tot += 1 
        # bottom left
        if can_see(seats, x, y, (1, -1), '#'):
            tot += 1 
        # bottom left
        if can_see(seats, x, y, (1, 1), '#'):
            tot += 1 
        if tot >= 5:
            result[y][x] = 'L'
            return True
    return False

def prt(seats):
    for i in seats:
        print("{}".format("".join(i)))
    print()

def copy_sets(seats):
    new_seats = []
    for l in seats:
        row = [s for s in l]
        new_seats.append(row)
    return new_seats

def count_seats(seats, s):
    sum = 0
    for l in seats:
        for seat in l:
            if seat == s:
                sum += 1
    return sum

def problem1(input):
    changed = True
    while changed == True:
    # for i in range(0,4):
        changed = False
        cpy = copy_sets(input)
        for y in range(0, len(input)):
            for x in range(0, len(input[y])):
                res = calc_seat(cpy, input, x, y)
                if res:
                    changed = True
        input = copy_sets(cpy)
        # prt(input)

    solution = count_seats(input, '#')
    print("Solution 1: {}".format(solution))


def problem2(input):
    changed = True
    while changed == True:
    # for i in range(0,4):
        changed = False
        cpy = copy_sets(input)
        for y in range(0, len(input)):
            for x in range(0, len(input[y])):
                res = calc_seat2(cpy, input, x, y)
                if res:
                    changed = True
        input = copy_sets(cpy)
        # prt(input)

    solution = count_seats(input, '#')
    print("Solution 2: {}".format(solution))


def main():
    title = "Advent of Code 2020!"
    print("{title}\n{line}\n\n".format(title=title, line="="*len(title)))

    input = read_input()

    # t1 = lib.measure(lambda: problem1(input))
    # print("Problem 1 took {:.6f}s to solve.\n\n".format(t1))

    t2 = lib.measure(lambda: problem2(input))
    print("Problem 2 took {:.6f}s to solve.".format(t2))


if __name__ == "__main__":
    main()
