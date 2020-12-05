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
    """
    input is a string with chars, representing upper/lower bound directions - 
    F / L means: half upper bound
    B / R means: half lower bound
    """
    min = 0
    max = nr
    res = 0
    for i in input:
        if i in ['B', 'R']:
            min = ceil((min + max) / 2)
            res = min
        else:
            max = floor((min + max) / 2)
            res = max
    return res


def read_input():
    return lib.remove_empty(lib.readfile('inputs/05-input.txt'))


def list_to_str(lst):
    """
    concats all elements of a list into a string
    e.g. [1,2,3] ==> '123'
    """
    return "".join(lst)


def extract_rows(input):
    """
    returns the row part of the input: first 7 nrs
    """
    return input[0:7]


def extract_cols(input):
    """
    returns the col part of the input: last 3 nrs
    """
    return input[7:]


def seat_row(input):
    """
    find the seat row by bisecting within a range of 128,
    using the row inputs as 'directions' (take upper or lower part on each bisect step)
    """
    return bisect(extract_rows(input), 127)


def seat_col(input):
    """
    find the seat row by bisecting within a range of 8
    using the col inputs as 'directions' (take upper or lower part on each bisect step)
    """
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
    ids = sorted(globals['seat_ids'])
    solution = 0
    for i in range(0,len(ids)-1):
        if ids[i+1] - ids[i] == 2:
            solution = ids[i] + 1

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
