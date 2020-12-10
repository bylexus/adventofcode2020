import time
import lib
import functools
import math
import re
from math import ceil, floor
import itertools


def read_input():
    input = []
    for x in lib.readfile('inputs/10-input.txt'):
    # for x in lib.readfile('inputs/10-input-sample-2.txt'):
        if len(x.strip()):
            input.append(int(x))

    return input


def problem1(input):
    """
    1. Sort the list, as we need to collect them all in order
    2. sum up the diff to the next one, count the diffs
       in a dict per diff amount (we need to know how many times the diffs 1,2,3 occured)
    """
    adapters = sorted(input)
    act_output = 0
    diffs = dict()
    for adapter in adapters:
        # print("act: {}, adapter: {}".format(act_output, adapter))
        if act_output >= (adapter - 3) and act_output < adapter:
            diff = adapter - act_output
            diffs[diff] = diffs.get(diff, 0) + 1
            act_output = adapter
        else:
            print("Oops, cannot use next adapter!")
            return
    diffs[3] += 1


    solution = diffs[1] * diffs[3]
    print("Solution 1: {}".format(solution))

def walk_adapters(adapters, start, target, seen_adapters):
    """
    Tree walking: span a tree, and count the valid paths,
    remembering the valid sub-paths per adapter in seen_adapters.
    Return immediately if we know already how many valid sub-paths
    are there for an adapter.
    """
    # we were here already:
    if start in seen_adapters.keys():
        return seen_adapters[start]

    # return if we have reached the target device:
    if target > start and target <= start + 3:
        return 1

    # span the sub-tree for each possible next adapter,
    # and count the valid sub-paths
    possible_next = [start + 1, start + 2, start + 3]
    valid_paths = 0
    for n in possible_next:
        if n in adapters:
            res = walk_adapters(adapters, n, target, seen_adapters)
            valid_paths += res
    seen_adapters[start] = valid_paths
    return valid_paths

def problem2(input):
    """
    'Walk the tree': All possibilities span a tree of possible paths.
    Only paths that end to the end device (max(input)) are valid.
    So walk the tree recursively (breath-first). On each node,
    we note the valid nr of sub-paths. If we encounter a node
    a 2nd time (from another tree branch), we immediately return.
    This way, walking the tree is muuuuuuuuuch faster than walking it
    through each time for full.
    """
    adapters = sorted(input)
    seen_adapters = dict()
    end = max(adapters) + 3

    solution = walk_adapters(adapters, 0, end, seen_adapters)

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
