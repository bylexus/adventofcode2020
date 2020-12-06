import time
import lib
import functools
import math
import re
from math import ceil, floor
import itertools

globals = dict({
    'lines': None,
})


def read_input():
    return lib.readfile('inputs/06-input.txt')



def problem1(input):
    sum = 0
    group_questions = dict()
    group = 1
    group_questions[1] = set()

    for line in input:
        if len(line.strip()) == 0:
            sum += len(group_questions[group])
            group += 1
            group_questions[group] = set()
        else:
            questions = list(line)
            for q in questions:
                group_questions[group].add(q)
    sum += len(group_questions[group])

    solution = sum
    print("Solution 1: Solution: {}".format(solution))


def problem2(input):
    group_questions = dict()
    group = 1
    group_questions[1] = dict()
    group_members = dict()
    group_members[1] = 0

    # create a dict for all groups and their nr of members
    # as well a dict for all groups and the number of times a question was answered by a user
    for line in input:
        if len(line.strip()) == 0:
            group += 1
            group_members[group] = 0
            group_questions[group] = dict()
        else:
            group_members[group] = group_members[group] + 1
            questions = list(line)
            for q in questions:
                group_questions[group][q] = group_questions[group].get(q,0) + 1
    
    sum = 0
    for (group, members) in group_members.items():
        # find question counts for the group that matches the group members:
        all_q = 0
        for (q, count) in group_questions[group].items():
            if count == members:
                all_q += 1
        sum += all_q

    solution = sum
    print("Solution 2: Solution: {}".format(solution))


def main():
    title = "Advent of Code 2020!"
    print("{title}\n{line}\n\n".format(title=title, line="="*len(title)))

    lines = read_input()

    t1 = lib.measure(lambda: problem1(lines))
    print("Problem 1 took {:.4f}s to solve.\n\n".format(t1))

    t2 = lib.measure(lambda: problem2(lines))
    print("Problem 2 took {:.4f}s to solve.".format(t2))


if __name__ == "__main__":
    main()
