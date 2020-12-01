import time
import lib
import functools
import math

numbers = [int(nr.strip()) for nr in lib.readfile('inputs/01-input.txt')]

def problem1():
    prod = 0
    for outer in range(0,len(numbers)-1):
        outnr = numbers[outer]
        for inner in range(outer+1, len(numbers)):
            innr = numbers[inner]
            if outnr + innr == 2020:
                prod = outnr * innr
                break

    print("Solution 1: The product is {}".format(prod))


def prod():
    for i in range(0,len(numbers)-2):
        n1 = numbers[i]
        for j in range(i+1, len(numbers)-1):
            n2 = numbers[j]
            for k in range(j+1, len(numbers)):
                n3 = numbers[k]
                if n1 + n2 + n3 == 2020:
                    return n1 * n2 * n3


def problem2():
    p = prod()

    print("Solution 2: The product is {}".format(p))


def main():
    title = "Advent of Code 2020!"
    print("{title}\n{line}\n\n".format(title=title, line="="*len(title)))

    t1 = lib.measure(problem1)
    print("Problem 1 took {:.4f}s to solve.\n\n".format(t1))

    t2 = lib.measure(problem2)
    print("Problem 2 took {:.4f}s to solve.".format(t2))


if __name__ == "__main__":
    main()
