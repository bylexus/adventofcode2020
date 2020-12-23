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
    def __init__(self, nr, next=None):
        self.nr = nr
        self.next = next


def read_input():
    # input = lib.remove_empty(lib.readfile('inputs/23-input.txt'))
    # input = lib.remove_empty(lib.readfile('inputs/23-input-sample.txt'))

    input = list(map(int, list('583976241')))
    test_input = list(map(int, list('389125467')))

    return input
    # return test_input


def extract_pickups(first):
    pickup_values = [
        first.next.nr,
        first.next.next.nr,
        first.next.next.next.nr
    ]
    pickup_nodes = [
        first.next,
        first.next.next,
        first.next.next.next
    ]
    first.next = pickup_nodes[2].next
    return (pickup_values, pickup_nodes)


def print_ring(first_node):
    act_node = first_node

    while act_node.next != first_node:
        print("{} ".format(act_node.nr), end="")
        act_node = act_node.next
    print("{} ".format(act_node.nr))


def find_node(first_node, value):
    act_node = first_node
    while True:
        if act_node.nr == value:
            return act_node
        act_node = act_node.next
        if act_node == first_node:
            break
    return None


def play(cards_list, nodes_dict, rounds, fill_to=0):
    cards = cards_list[:] + list(range(max(cards_list)+1, fill_to + 1))
    max_nr = max(cards)
    prev_node = None
    first_node = None

    # build a ring of nodes:
    for card in cards:
        node = Node(card)
        nodes_dict[card] = node
        if prev_node:
            prev_node.next = node
        else:
            first_node = node
        prev_node = node
    prev_node.next = first_node

    for i in range(0, rounds):
        # extract pickup cards:
        pickup_values, pickup_nodes = extract_pickups(first_node)

        # find insert node:
        dest_nr = first_node.nr - 1
        while dest_nr == 0 or dest_nr in pickup_values:
            dest_nr = (dest_nr - 1) % (max_nr + 1)
        insert_node = nodes_dict[dest_nr]

        # insert the 3 pickups after insert node:
        pickup_nodes[2].next = insert_node.next
        insert_node.next = pickup_nodes[0]

        # move first node:
        first_node = first_node.next
    return first_node


def problem1(input):
    cards = input[:]
    nodes_dict = dict()
    first_node = play(cards, nodes_dict, 100)

    # build result
    act_node = first_node.next
    res = ""
    while act_node != first_node:
        res += str(act_node.nr)
        act_node = act_node.next

    solution = res
    print("Solution 1: {}".format(solution))


def problem2(input):
    cards = input[:]
    nodes_dict = dict()
    play(cards, nodes_dict, 10000000, 1000000)

    # build result
    node_1 = nodes_dict[1]

    solution = node_1.next.nr * node_1.next.next.nr
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
