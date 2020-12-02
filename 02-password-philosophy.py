import time
import lib
import functools
import math
import re

# inputs = lib.readfile('inputs/02-input-sample.txt')
inputs = lib.readfile('inputs/02-input.txt')


def problem1():
    valid = 0
    for line in inputs:
        # find format: '(nr)-(nr) (char): (*)'
        m = re.compile("(\d+)-(\d+)\s+(.):\s+(.*)")
        g = m.match(line)
        if g:
            nrMin = int(g.group(1))
            nrMax = int(g.group(2))
            letter = str(g.group(3))
            pw = str(g.group(4))
            countNr = pw.count(letter)
            if countNr >= nrMin and countNr <= nrMax:
                valid = valid + 1
    print("Solution 1: Valid passwords: {}".format(valid))



def problem2():
    valid = 0
    for line in inputs:
        # find format: '(nr)-(nr) (char): (*)'
        m = re.compile("(\d+)-(\d+)\s+(.):\s+(.*)")
        g = m.match(line)
        count = 0
        if g:
            nrMin = int(g.group(1)) - 1
            nrMax = int(g.group(2)) - 1
            letter = str(g.group(3))
            pw = str(g.group(4))
            if pw[nrMin] == letter:
                count = count + 1
            if pw[nrMax] == letter:
                count = count + 1
            if count == 1:
                valid = valid + 1
    print("Solution 2: Valid passwords: {}".format(valid))


def main():
    title = "Advent of Code 2020!"
    print("{title}\n{line}\n\n".format(title=title, line="="*len(title)))

    t1 = lib.measure(problem1)
    print("Problem 1 took {:.4f}s to solve.\n\n".format(t1))

    t2 = lib.measure(problem2)
    print("Problem 2 took {:.4f}s to solve.".format(t2))


if __name__ == "__main__":
    main()
