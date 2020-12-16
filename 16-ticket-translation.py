import time
import lib
import functools
import math
import re
from math import ceil, floor
import itertools

valid_tickets = []

def read_input():
    # input = list(lib.remove_empty(lib.readfile('inputs/16-input-sample.txt')))
    # input = list(lib.remove_empty(lib.readfile('inputs/16-input-sample-2.txt')))
    input = list(lib.remove_empty(lib.readfile('inputs/16-input.txt')))
    return input

def is_valid(ticket, rules_dict):
    errors = []
    for nr in ticket:
        valid = False
        for rules in rules_dict.values():
            for r in rules:
                bounds = r.split('-')
                low = int(bounds[0])
                up = int(bounds[1])
                if nr >= low and nr <= up:
                    valid = True
        if not valid:
            errors.append(nr)
    return errors


def problem1(input):
    global valid_tickets

    rules_dict = dict()
    rules = input[:input.index('your ticket:')]
    m = re.compile(r"(.*):\s+(.*) or (.*)")
    for r in rules:
        g = m.match(r)
        if g:
            rules_dict[g.group(1)] = [g.group(2), g.group(3)]
    nearby = [list(map(int,l.split(','))) for l in input[input.index('nearby tickets:')+1:]]

    error_rate = 0
    for n in nearby:
        err = is_valid(n, rules_dict)
        if len(err) == 0:
            valid_tickets.append(n)
        error_rate += sum(err)

    solution = error_rate
    print("Solution 1: {}".format(solution))

def is_valid_rule(nrs, rule):
    valid_count = 0
    for n in nrs:
        valid = False
        for r in rule:
            bounds = r.split('-')
            low = int(bounds[0])
            up = int(bounds[1])
            if n >= low and n <= up:
                valid = True
        if valid:
            valid_count += 1

    return valid_count == len(nrs)

def problem2(input):
    global valid_tickets

    rules_dict = dict()
    rules = input[:input.index('your ticket:')]
    m = re.compile(r"(.*):\s+(.*) or (.*)")
    for r in rules:
        g = m.match(r)
        if g:
            rules_dict[g.group(1)] = [g.group(2), g.group(3)]
    my_ticket = list(map(int, input[input.index('your ticket:')+1].split(',')))

    # re-arrange nearby tickets so that we have
    # an array of 1st fields, 2nd fields, etc...
    fields = len(my_ticket)
    fields_all_tix = []
    for i in range(0, fields):
        f_arr = []
        for v in valid_tickets:
            f_arr.append(v[i])
        fields_all_tix.append(f_arr)

    # now do the following:
    # determine the field that hat only 1 matching rule. 
    # this rule must be for this field. assign and remove from rule list.
    # repeat for every rule until all fields have a rule assigned.
    fields_to_determine = list(range(0,len(my_ticket)))
    rule_for_field = dict()
    processed_rules = []
    
    while len(fields_to_determine) > 0:
        for i, f_arr in enumerate(fields_all_tix):
            if i not in fields_to_determine:
                continue
            matching_rules = []
            for rule_name, rule in rules_dict.items():
                if rule_name in processed_rules:
                    continue
                if is_valid_rule(f_arr, rule):
                    matching_rules.append((rule_name, rule))
            if len(matching_rules) == 1:
                fields_to_determine.remove(i)
                rule_for_field[i] = matching_rules[0]
                processed_rules.append(matching_rules[0][0])

    # OK, rule found for every field, now calculate the end result:
    fields = []
    prod = 1
    for field, rule in rule_for_field.items():
        if re.match(r"^departure", rule[0]):
            prod *= my_ticket[field]
    
    solution = prod

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