import time
import lib
import functools
import math
import re
from math import ceil, floor
import itertools


def read_input():
    return list(map(int, lib.remove_empty(lib.readfile('inputs/10-input.txt'))))


def problem1(input):
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
