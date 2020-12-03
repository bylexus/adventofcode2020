import time
import lib
import functools
import math
import re

# lines = list(filter(lambda l: len(l.strip()) > 0, lib.readfile('inputs/03-input-sample.txt')))
lines = list(filter(lambda l: len(l.strip()) > 0, lib.readfile('inputs/03-input.txt')))

def slope_down(dx, dy):
    """
    sleigh down the hill: for each step, move act pos + dy/dy
    and check if it's a tree or not
    return the number of trees encountered until the end is reached
    """
    trees = 0
    x = 0
    y = 0
    while y < len(lines):
        actLine = lines[y]
        if actLine[x] == '#':
            trees = trees + 1
        y = y+dy
        x = (x + dx) % len(actLine)
    return trees


def problem1():
    trees = slope_down(3, 1)
    print("Solution 1: # of trees: {}".format(trees))



def problem2():
    slopes = [(1,1),(3,1), (5,1), (7,1), (1,2)]
    trees = 1
    for slope in slopes:
        trees = trees * slope_down(slope[0], slope[1])

    print("Solution 2: # of trees: {}".format(trees))


def main():
    title = "Advent of Code 2020!"
    print("{title}\n{line}\n\n".format(title=title, line="="*len(title)))

    t1 = lib.measure(problem1)
    print("Problem 1 took {:.4f}s to solve.\n\n".format(t1))

    t2 = lib.measure(problem2)
    print("Problem 2 took {:.4f}s to solve.".format(t2))


if __name__ == "__main__":
    main()
