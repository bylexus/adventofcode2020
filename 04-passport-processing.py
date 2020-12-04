import time
import lib
import functools
import math
import re

passports = []
needed_keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']


def check_extended_rules(passport):
    """
    Check extended passwort rules - one by one, some regex magic here :-)
    """

    if not (re.match(r"^\d\d\d\d$", passport['byr']) and (int(passport['byr']) >= 1920 and int(passport['byr']) <= 2002)):
        return False
    if not (re.match(r"^\d\d\d\d$", passport['iyr']) and (int(passport['iyr']) >= 2010 and int(passport['iyr']) <= 2020)):
        return False
    if not (re.match(r"^\d\d\d\d$", passport['eyr']) and (int(passport['eyr']) >= 2020 and int(passport['eyr']) <= 2030)):
        return False

    # height
    m = re.compile("(\d+)(cm|in)")
    g = m.match(passport['hgt'])
    if g:
        unit = g.group(2)
        if unit == 'cm':
            if not (int(g.group(1)) >= 150 and int(g.group(1)) <= 193):
                return False
        if unit == 'in':
            if not (int(g.group(1)) >= 59 and int(g.group(1)) <= 76):
                return False
    else:
        return False

    # hcl:
    if not re.match(r"^#([0-9]|[a-f]){6}$", passport['hcl']):
        return False

    if not passport['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return False
    
    if not re.match(r"^([0-9]){9}$", passport['pid']):
        return False

    return True


def read_input():
    # lines = lib.readfile('inputs/04-input-sample.txt')
    lines = lib.readfile('inputs/04-input.txt')

    act_pass = dict()
    for line in lines:
        if len(line.strip()) == 0:
            passports.append(act_pass)
            act_pass = dict()
        else:
            pieces = line.split(' ')
            for piece in pieces:
                key_val = piece.split(':')
                act_pass[key_val[0]] = key_val[1]

    passports.append(act_pass)
    return lines


def problem1():
    valid = 0
    # find valid passwords:
    for passport in passports:
        keys = passport.keys()
        if set(needed_keys).issubset(set(keys)):
            valid = valid + 1

    solution = valid
    print("Solution 1: Solution: {}".format(solution))


def problem2():
    valid = 0
    # find valid passwords:
    for passport in passports:
        keys = passport.keys()
        if set(needed_keys).issubset(set(keys)):
            if check_extended_rules(passport):
                valid = valid + 1

    solution = valid
    print("Solution 2: Solution: {}".format(solution))


def main():
    title = "Advent of Code 2020!"
    print("{title}\n{line}\n\n".format(title=title, line="="*len(title)))

    read_input()

    t1 = lib.measure(problem1)
    print("Problem 1 took {:.4f}s to solve.\n\n".format(t1))

    t2 = lib.measure(problem2)
    print("Problem 2 took {:.4f}s to solve.".format(t2))


if __name__ == "__main__":
    main()
