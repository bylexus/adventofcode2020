import time
import lib
import functools
import math
import re
from math import ceil, floor
import itertools

globals = dict({
    'lines': None,
    'seat_ids': list()
})


def bisect(input, nr):
    min = 0
    max = nr
    res = 0
    for i in input:
        if i == 0:
            min = ceil((min + max) / 2)
            res = min
        else:
            max = floor((min + max) / 2)
            res = max
    return res


def convert_input_line(input_line):
    l = input_line.replace('F', '1').replace(
        'B', '0').replace('L', '1').replace('R', '0')
    return list(map(lambda i: int(i), list(l)))


def read_input():
    # input comes as binary texts: F/B, R/L. So first thing to do:
    # create int arrays of each line: [0,1,0,0,....]
    lines = list(filter(lambda l: len(l) > 1,
                        lib.readfile('inputs/05-input.txt')))
    res = list()
    for l in lines:
        res.append(convert_input_line(l))

    return res


def list_to_str(lst):
    return "".join(map(str, lst))


def extract_rows(input):
    return input[0:7]


def extract_cols(input):
    return input[7:]


def seat_row(input):
    return bisect(extract_rows(input), 127)


def seat_col(input):
    return bisect(extract_cols(input), 7)


def seat_id(row, col):
    return 8*row + col


def problem1():
    # input = 'FBFBBFFRLR' # row 44, col 5
    # input = 'BFFFBBFRRR' # row 70 col 7
    # input = 'FFFBBBFRRR' # row 14 col 7
    # input = 'BBFFBBFRLL' # row 102 col 4
    max_id = 0

    # each line is an array with ints, representing a boarding card nr
    for line in globals['lines']:
        # find row/col of boarding card nr:
        rows = seat_row(line)
        cols = seat_col(line)

        # remember the max seat ID, as this is the solution 1:
        sid = seat_id(rows, cols)
        max_id = max(max_id, sid)
        # and also store all seat IDs, as this is needed for solution 2:
        globals['seat_ids'].append(sid)
    solution = max_id
    print("Solution 1: Solution: {}".format(solution))


def problem2():
    # generate a list from 0000000000 - 1111111111:
    all_tickets = [list_to_str(l)
                   for l in itertools.product([0, 1], repeat=10)]

    # create strings from the binary values - to better diff the two sets:
    available_tickets = [list_to_str(l) for l in globals['lines']]

    # diff: all tix - available_tix = missing tix:
    missing = set(all_tickets) - set(available_tickets)

    # loop through all missing tickets, and find one that HAS a ticket id + 1 / - 1 in the orig list:
    solution = 0
    for m in missing:
        m_list = convert_input_line(m)
        my_row = seat_row(m_list)
        my_col = seat_col(m_list)
        my_id = seat_id(my_row, my_col)

        if my_id - 1 in globals['seat_ids'] and my_id + 1 in globals['seat_ids']:
            solution = my_id
            break

    print("Solution 2: Solution: {}".format(solution))


def main():
    title = "Advent of Code 2020!"
    print("{title}\n{line}\n\n".format(title=title, line="="*len(title)))

    globals['lines'] = read_input()

    t1 = lib.measure(problem1)
    print("Problem 1 took {:.4f}s to solve.\n\n".format(t1))

    t2 = lib.measure(problem2)
    print("Problem 2 took {:.4f}s to solve.".format(t2))


if __name__ == "__main__":
    main()
