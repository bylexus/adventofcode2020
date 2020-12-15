import time
import lib
import functools
import math
import re
from math import ceil, floor
import itertools


def read_input():
    # input = list(map(int,list(lib.remove_empty(lib.readfile('inputs/15-input-sample.txt')))[0].split(',')))
    input = list(map(int,list(lib.remove_empty(lib.readfile('inputs/15-input.txt')))[0].split(',')))
    # input = list(map(int,list(lib.remove_empty(lib.readfile('inputs/15-input-sample-7.txt')))[0].split(',')))
    # input = list(map(int,list(lib.remove_empty(lib.readfile('inputs/15-input-sample-5.txt')))[0].split(',')))
    return input

def calc_last_spoken_word(input, rounds):
    spoken_on = dict()
    step = 1
    last_spoken = 0
    # first round:
    for i in input:
        last_spoken = i
        spoken_on[i] = [step]
        step += 1

    # now, repeat:
    while step <= rounds:
        last_spoken_on = spoken_on[last_spoken]
        if len(last_spoken_on) == 1:
            spoken_arr = spoken_on.get(0, [])
            spoken_arr.append(step)
            spoken_on[0] = spoken_arr
            last_spoken = 0
        else:
            away = last_spoken_on[-1] - last_spoken_on[-2]
            spoken_arr = spoken_on.get(away, [])
            spoken_arr.append(step)
            spoken_on[away] = spoken_arr
            last_spoken = away
        step += 1
    return last_spoken

def problem1(input):

    solution = calc_last_spoken_word(input, 2020)
    print("Solution 1: {}".format(solution))


def problem2(input):
    solution = calc_last_spoken_word(input, 30000000)
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
