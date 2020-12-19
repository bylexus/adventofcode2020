import time
import lib
from functools import reduce
import math
import re
from math import ceil, floor
from itertools import product
import operator

string_lists = dict()

def read_input():
    input = lib.readfile('inputs/19-input.txt')
    # input = lib.readfile('inputs/19-input-sample.txt')
    # input = lib.readfile('inputs/19-input-sample-2.txt')
    rules = []
    messages = []
    for l in input:
        if re.match(r"\d+:.*", l):
            rules.append(l)
        elif len(l.strip()):
            messages.append(l)

    return (rules, messages)

def combine_string_lists(list1, list2, max_str_len):
    new_list= []
    for l1 in list1:
        for l2 in list2:
            new_str = l1 + l2
            if len(new_str) <= max_str_len:
                new_list.append(new_str)
    return new_list

def to_str_list(rules_dict, rule_nr, parent_nr_list = [], max_str_len = 0):
    """
    idea: build a complete string list with all possible strings for this rule.
    build the rules recursively, and store them per rule nr in the global
    string_lists dict for reference.
    """

    global string_lists

    # invalid rule, if it is a too deep loop:
    if parent_nr_list.count(rule_nr) > 2:
        return None

    # 'a', 'b' itself form a single string list:
    if rule_nr in ['a', 'b']:
        return [rule_nr]

    if rule_nr in string_lists.keys():
        return string_lists[rule_nr]

    rule = rules_dict[rule_nr]
    parent_nr_list = parent_nr_list[:]
    parent_nr_list.append(rule_nr)
    # print(parent_nr_list)

    # for each OR part, process the parts separately and fill a
    # shared string list:
    str_list = []
    for and_list in rule:
        # for each item of the and_list, form a string list, 
        # then combine all lists (n*m*o....)
        and_str_list = []
        for single_rule in and_list:
            res = to_str_list(rules_dict, single_rule, parent_nr_list, max_str_len)
            if (res and len(res)):
                and_str_list.append(list(set(res)))
            else:
                # whole rule cannot be used, as a sub-list is empty:
                and_str_list = []
                break
        if len(and_str_list):
            str_list += list(reduce(lambda a,b: combine_string_lists(a,b, max_str_len),and_str_list))

    string_lists[rule_nr] = list(set(str_list))
    return str_list
                

def problem1(input):
    rules, messages = input
    rules_dict = dict()
    for r in rules:
        g = re.match(r'^(\d+):\s+\"([a-z])\"', r)
        if g:
            rules_dict[g.group(1)] = g.group(2)
        else:
            g = re.match(r"^(\d+):\s(.*)", r)
            if g:
                nr = g.group(1)
                ors = g.group(2).split(' | ')
                ors = [e.split(' ') for e in ors]
                rules_dict[nr] = ors
    max_len = max(map(len, messages))
    print(rules_dict, '0')
    str_list = to_str_list(rules_dict, '0', max_str_len=max_len)
    print(len(str_list))

    in_count = 0
    for m in messages:
        if m in str_list:
            in_count += 1
    solution = in_count
    print("Solution 1: {}".format(solution))

def problem2(input):
    global string_lists
    string_lists = dict()

    rules, messages = input
    rules_dict = dict()
    for r in rules:
        g = re.match(r'^(\d+):\s+\"([a-z])\"', r)
        if g:
            rules_dict[g.group(1)] = g.group(2)
        else:
            g = re.match(r"^(\d+):\s(.*)", r)
            if g:
                nr = g.group(1)
                ors = g.group(2).split(' | ')
                ors = [e.split(' ') for e in ors]
                rules_dict[nr] = ors

    max_len = max(map(len, messages))
    rules_dict['8'] = [['42'], ['42','8']]
    rules_dict['11'] = [['42', '31'], ['42','11','31']]


    print(rules_dict, '0')
    str_list = to_str_list(rules_dict, '0', max_str_len=max_len)
    print(len(str_list))

    in_count = 0
    for m in messages:
        if m in str_list:
            in_count += 1
    solution = in_count
    print("Solution 2: {}".format(solution))


def main():
    title = "Advent of Code 2020!"
    print("{title}\n{line}\n\n".format(title=title, line="="*len(title)))

    input = read_input()

    t1 = lib.measure(lambda: problem1(input))
    print("Problem 1 took {:.6f}s to solve.\n\n".format(t1))

    # t2 = lib.measure(lambda: problem2(input))
    # print("Problem 2 took {:.6f}s to solve.".format(t2))


if __name__ == "__main__":
    main()