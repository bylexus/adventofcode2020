import time
import lib
import functools
import math

def calc_fuel(mass):
    res = math.floor(int(mass) / 3) - 2
    if res > 0:
        res += calc_fuel(res)
    return res if res > 0 else 0


def problem1():
    lines = [math.floor(int(nr) / 3) - 2 for nr in lib.readfile('inputs/00-input.txt')]
    sum_energy = functools.reduce(lambda a,b: a+b, lines)

    print("Solution 1: The sum is {}".format(sum_energy))



def problem2():
    lines = [calc_fuel(nr) for nr in lib.readfile('inputs/00-input.txt')]
    sum_energy = functools.reduce(lambda a,b: a+b, lines)

    print("Solution 2: The sum is {}".format(sum_energy))


def main():
    title = "Advent of Code 2020!"
    print("{title}\n{line}\n\n".format(title=title, line="="*len(title)))

    t1 = lib.measure(problem1)
    print("Problem 1 took {:.3f}s to solve.\n\n".format(t1))

    t2 = lib.measure(problem2)
    print("Problem 2 took {:.3f}s to solve.".format(t2))


if __name__ == "__main__":
    main()
