import time
import lib
import functools
import math
import re
from math import ceil, floor
import itertools

found = 0

def read_input():
    # input = [int(x) for x in lib.readfile('inputs/09-input-sample.txt')]
    input = [int(x) for x in lib.readfile('inputs/09-input.txt')]
    # input = lib.readfile('inputs/09-input.txt')

    return input


def check_sum(valid_list, nr):
    """
    checks if 2 unique numbers in valid_list sum up to nr.
    True for yes, False for no :-)
    """
    valid_list = list(set(valid_list))

    for i in range(0, len(valid_list)-1):
        for j in range(i+1, len(valid_list)):
            if (valid_list[i]+valid_list[j] == nr):
                return True
    return False

def problem1(input):
    global found

    preamble = 25
    act_pos = preamble

    # look for the first previous n numbers that not 2 sum up to the actual nr:
    for i in range(preamble, len(input)):
        nr = input[i]
        checklist = input[i-preamble:i]
        if not check_sum(checklist, nr):
            break

    solution = nr
    # save input as a global var for problem 2:
    found = nr
    print("Solution 1: {}".format(solution))


def find_sum(input, start_pos, check):
    """
    finds a contiguous range of numbers in input that sum up to check.
    begin at start_pos (and down).
    """
    total = 0
    nrs = []
    for i in range(start_pos, len(input)):
        total += input[i]
        nrs.append(input[i])
        if total == check:
            return nrs
    return False

def problem2(input):
    global found
    res = None
    # start looking for a contiguous sum at pos 0, then 1, ....
    for i in range(0,len(input)):
        res = find_sum(input, i, found)
        if res:
            break
        
    solution = min(res) + max(res)
    print("Solution 2: {}".format(solution))


def main():
    title = "Advent of Code 2020!"
    print("{title}\n{line}\n\n".format(title=title, line="="*len(title)))

    input = read_input()

    t1 = lib.measure(lambda: problem1(input))
    print("Problem 1 took {:.4f}s to solve.\n\n".format(t1))

    t2 = lib.measure(lambda: problem2(input))
    print("Problem 2 took {:.4f}s to solve.".format(t2))


if __name__ == "__main__":
    main()
