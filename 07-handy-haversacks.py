import time
import lib
import functools
import math
import re
from math import ceil, floor
import itertools


class Bag:
    name: None
    # tuple list of child nodes: (nr, name)
    bag_list: []

# node name:object list:
bags = dict()


def read_input():
    global bags

    # input = lib.readfile('inputs/07-input-sample.txt')
    # input = lib.readfile('inputs/07-input-sample2.txt')
    input = lib.readfile('inputs/07-input.txt')
    m = re.compile(r"(\d+)\s+(.*)")

    # sanitize input: clean plural forms (bags -> bag), remove sentence chars.
    # then split and create Bag objects
    for line in input:
        # sanitize:
        line = line.replace('bags', 'bag').replace('.','')
        # split name from contents:
        spl = line.split('contain')
        bag = spl[0].strip()
        contents = spl[1].split(',')

        # create bag objects (aka graph nodes):
        bag_obj = Bag()
        bag_obj.name = bag
        bag_obj.bag_list = []

        # create a bag list (aka node list): name -> object
        bags[bag] = bag_obj

        # create a child node list for each bag, including bag count (weights)
        for c in contents:
            c = c.strip()
            g = m.match(c)
            if g:
                (nr, name) = g.group(1, 2)
                bag_obj.bag_list.append((nr, name))

    return bags


def visit(bag, visited, found_0, search):
    """
    graph traversal for problem 1:
    we get a graph node (bag), and look if we can
    find a way to the target bag (search).
    Because it's a (directed) graph, we need to detect loops.
    All visited nodes are stored in visited.
    All nodes that link to the target bag are noted in found_0.
    """
    global bags

    # are we on the target bag? Yes, return here:
    if bag.name == search:
        return True

    # already there once? so return what we already know:
    if bag.name in visited:
        return bag.name in found_0

    # mark actual node as visited:
    visited.add(bag.name)

    # now visit all child nodes (recursively): If one of it
    # links to the target node, then add THIS node to the list of
    # nodes that link (indirectly) to the target node:
    for child in bag.bag_list:
        child = bags[child[1]]
        if visit(child, visited, found_0, search):
            found_0.add(bag.name)

    # finally, return if our node links to the target:
    return bag.name in found_0

def visit2(bag, visited, contents):
    """
    graph traversal for problem 2:
    we travel the graph by the given start node, and
    count how many bags (childs) can this bag carry (recursively).
    Because it's a (directed) graph, we need to detect loops.
    All visited nodes are stored in visited.
    All known bag contents are stored in contents
    """
    global bags

    # we already examined this bag, and know how many bags it can contain:
    if bag.name in visited:
        return contents[bag.name]

    # mark visited:
    visited.add(bag.name)

    # initialize content counter:
    if not contents.get(bag.name):
        contents[bag.name] = 0

    cnt = 0
    # recursively travel childs and count the child plus its content bags:
    for child in bag.bag_list:
        nr = int(child[0])
        child = bags[child[1]]
        cnt += nr + nr * visit2(child, visited, contents)
    # update the bag counter:
    contents[bag.name] = cnt
    return cnt


def problem1(bags):
    found_0 = set()
    visited = set()

    for bag in bags.values():
        visit(bag, visited, found_0, 'shiny gold bag')

    solution = len(found_0)

    print("Solution 1: Solution: {}".format(solution))


def problem2(bags):
    visited = set()
    counts = dict()

    bag = bags['shiny gold bag']

    solution = visit2(bag, visited, counts)
    print("Solution 2: Solution: {}".format(solution))


def main():
    title = "Advent of Code 2020!"
    print("{title}\n{line}\n\n".format(title=title, line="="*len(title)))

    bags = read_input()

    t1 = lib.measure(lambda: problem1(bags))
    print("Problem 1 took {:.4f}s to solve.\n\n".format(t1))

    t2 = lib.measure(lambda: problem2(bags))
    print("Problem 2 took {:.4f}s to solve.".format(t2))


if __name__ == "__main__":
    main()
