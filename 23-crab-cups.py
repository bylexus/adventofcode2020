import time
import lib
from functools import reduce
import math
import re
from math import ceil, floor
from itertools import product
from collections import deque
import operator


def read_input():
    # input = lib.remove_empty(lib.readfile('inputs/23-input.txt'))
    # input = lib.remove_empty(lib.readfile('inputs/23-input-sample.txt'))

    input = list(map(int, list('583976241')))
    test_input = list(map(int, list('389125467')))

    # return input
    return test_input

def rotate(l, k):
    return l[k:] + l[:k]

def problem1(input):
    cards = input[:]
    dest_nr = 0
    # current must be always 0 at the end (rotate when needed)
    for i in range(0,100):
        pickup = cards[1:4]
        cards = [cards[0]] + cards[4:]
        dest_nr = cards[0] - 1
        max_nr = max(cards)
        while dest_nr not in cards:
            dest_nr = (dest_nr - 1) % (max_nr + 1)
        dest_index = cards.index(dest_nr)
        cards = cards[:dest_index + 1] + pickup + cards[dest_index + 1:]
        cards = rotate(cards,1)
        print(cards)
        # print(pickup)
        # print(dest_nr)
    
    index_1 = cards.index(1)
    final = cards[index_1 + 1:] + cards[:index_1]

    solution = "".join(map(str,final))
    print("Solution 1: {}".format(solution))


def problem2(input):
    cards = input[:] + list(range(max(input)+1,1000001))
    dest_nr = 0
    return
    # current must be always 0 at the end (rotate when needed)
    for i in range(0, 10000000):
        pickup = cards[1:4]
        cards = [cards[0]] + cards[4:]
        dest_nr = cards[0] - 1
        max_nr = max(cards)
        while dest_nr not in cards:
            dest_nr = (dest_nr - 1) % (max_nr + 1)
        dest_index = cards.index(dest_nr)
        cards = cards[:dest_index + 1] + pickup + cards[dest_index + 1:]
        cards = rotate(cards,1)
        # print(cards)
        # print(pickup)
        # print(dest_nr)
    
    index_1 = cards.index(1)
    final_cards = (
        cards[(index_1 + 1) % len(cards)] + cards[(index_1 + 2) % len(cards)]
    )
    print(final_cards)

    solution = final_cards[0] * final_cards[1]
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
