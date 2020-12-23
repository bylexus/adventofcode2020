import time
import lib
from functools import reduce
import math
import re
from math import ceil, floor
from itertools import product
from collections import deque
import operator

class Node:
    def __init__(self, nr, next = None):
        self.nr = nr
        self.next = next

def read_input():
    # input = lib.remove_empty(lib.readfile('inputs/23-input.txt'))
    # input = lib.remove_empty(lib.readfile('inputs/23-input-sample.txt'))

    input = list(map(int, list('583976241')))
    test_input = list(map(int, list('389125467')))

    # return input
    return test_input

def rotate(l, k):
    return l[k:] + l[:k]

def extract_pickups(first):
    pickup = [
        first.next.nr,
        first.next.next.nr,
        first.next.next.next.nr
    ]
    first.next = first.next.next.next.next
    return pickup

def print_ring(first_node):
    act_node = first_node
    
    while act_node.next != first_node:
        print("{} ".format(act_node.nr),end="")
        act_node = act_node.next
    print("{} ".format(act_node.nr))
    
def find_node(first_node, value):
    act_node = first_node
    while True:
        if act_node.nr == value:
            return act_node
        act_node = act_node.next
        if act_node == first_node:
            break;
    return None
    

def problem1(input):
    cards = input[:]
    max_nr = max(cards)
    prev_node = None
    first_node = None

    # build a ring of nodes:
    for card in cards:
        node = Node(card)
        if prev_node:
            prev_node.next = node
        else:
            first_node = node
        prev_node = node
    prev_node.next = first_node

    for i in range(0, 100):
        # extract pickup cards:
        pickup = extract_pickups(first_node)

        # find insert node:
        dest_nr = first_node.nr - 1
        while dest_nr == 0 or dest_nr in pickup:
            dest_nr = (dest_nr - 1) % (max_nr + 1)
        insert_node = find_node(first_node,dest_nr)

        # insert pickups after insert node:
        n3 = Node(pickup[2], insert_node.next)
        n2 = Node(pickup[1], n3)
        n1 = Node(pickup[0], n2)
        insert_node.next = n1

        # move first node:
        first_node = first_node.next

    # build result
    act_node = first_node.next
    res = ""
    while act_node != first_node:
        res += str(act_node.nr)
        act_node = act_node.next

    solution = res
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
