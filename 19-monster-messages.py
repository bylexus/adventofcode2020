import time
import lib
from functools import reduce
import math
import re
from math import ceil, floor
from itertools import product
import operator

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


def get_expr_str(rules_dict, rule_nr):
    """
    form a (recursively built) regular expression pattern
    for the given rule
    """
    rule = rules_dict[rule_nr]
    if rule in ['a', 'b']:
        return rule
    else:
        rule = rules_dict[rule_nr]
        or_list = []
        for and_list in rule:
            and_str = "("
            for item in and_list:
                and_str += get_expr_str(rules_dict, item)
            and_str += ')'
            or_list.append(and_str)
        s = "|".join(or_list)
    return '(' + s + ')'

def create_rule_dict(rule_lines):
    """
       create a dictionnary of rules:
       key: rule-nr
       value: list of OR parts for regex: 1 2 | 3 4 ==> [[1,2], [3,4]]
    """
    rules_dict = dict()
    for r in rule_lines:
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
    return rules_dict



def problem1(input):
    rules, messages = input
    rules_dict = create_rule_dict(rules)

    # form a single regex for the rules:
    exprs = get_expr_str(rules_dict, '0')
    cm = re.compile('^' + exprs + '$')
    in_count = 0
    for m in messages:
        if cm.match(m):
            in_count += 1
    solution = in_count
    print("Solution 1: {}".format(solution))


def problem2(input):
    rules, messages = input
    rules_dict = create_rule_dict(rules)

    # modify rule 8 and 11: resolve the recursive rule reference manually, *hopefully* deep enough
    # (here: 10 recursions for rule 8, 7 recursions for rule 11)
    # [42,8] becomes [42,42], [42,42,42] ... as the '8' is replaced with the rule again
    rules_dict['8'] = [
        ['42'], 
        ['42', '42'], 
        ['42', '42', '42'], 
        ['42', '42', '42', '42'], 
        ['42', '42', '42', '42', '42'], 
        ['42', '42', '42', '42', '42', '42'],
        ['42', '42', '42', '42', '42', '42', '42'],
        ['42', '42', '42', '42', '42', '42', '42', '42'],
        ['42', '42', '42', '42', '42', '42', '42', '42', '42'],
        ['42', '42', '42', '42', '42', '42', '42', '42', '42', '42'],
    ]
    # [42,11,31] becomes [42,31], [42,42,31,31], [42,42,42,31,31,31] ... as the '11' is replaced with the rule again
    rules_dict['11'] = [
        ['42', '31'], 
        ['42', '42', '31', '31'],
        ['42', '42', '42', '31', '31', '31'],
        ['42', '42', '42', '42', '31', '31', '31', '31'],
        ['42', '42', '42', '42', '42', '31', '31', '31', '31', '31'],
        ['42', '42', '42', '42', '42', '42', '31', '31', '31', '31', '31', '31'],
        ['42', '42', '42', '42', '42', '42', '42', '31', '31', '31', '31', '31', '31', '31']
    ]
    exprs = get_expr_str(rules_dict, '0')
    cm = re.compile('^' + exprs + '$')
    in_count = 0
    for m in messages:
        if cm.match(m):
            in_count += 1
    solution = in_count

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
