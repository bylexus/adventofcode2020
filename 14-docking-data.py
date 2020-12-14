import time
import lib
import functools
import math
import re
from math import ceil, floor
import itertools

mem = dict()
mem2 = dict()

def read_input():
    # input = list(lib.remove_empty(lib.readfile('inputs/14-input-sample.txt')))
    # input = list(lib.remove_empty(lib.readfile('inputs/14-input-sample2.txt')))
    input = list(lib.remove_empty(lib.readfile('inputs/14-input.txt')))
    return input

def apply_mask(mask, nr):
    """
    applies the 36bit mask ('00110xx011...') to the given decimal
    number, and returns the new decimal.
    Mask is applied as follows:
    0: clears bit
    1: sets bit
    X: leave bit unchanged
    """
    nr_str = list("{:036b}".format(int(nr)))
    for i in range(0,len(nr_str)):
        if mask[i] in ['0','1']:
            nr_str[i] = mask[i]
    return int("".join(nr_str),2)


def problem1(input):
    global mem
    mask = 36*'X'
    for l in input:
        if l[0:4] == 'mask':
            mask = l.split('=')[1].strip()
            # print(mask)
        else:
            pieces = l.split('=')
            value = int(pieces[1])
            addr = int(re.match(r"mem\[(\d+)\]", l.strip()).group(1))
            # print(value)
            # print(addr)
            # print(apply_mask(mask, value))
            mem[addr] = apply_mask(mask, value)
            # print()
    
    solution = sum(mem.values())
    print("Solution 1: {}".format(solution))


def write_mem(mem, mask, value, addr ):
    """
    1. apply mask to addr:
       1: sets bit
       2: leaves bit
       X: also set as x, and later permuted over
    2. permute all possible values of addr (now with x):
       replace all x by all possible 0/1 values
       this each gives a memory address
    3. write value (unchanged) to this memory adresses (many)
    """

    # create bit permutations:
    x_count = mask.count('X')
    bit_perms = itertools.product('01', repeat=x_count)

    addr_str = "{:036b}".format(addr)
    addr_list = list(addr_str)

    # apply mask to address, with X:
    for i in range(0,len(addr_str)):
        if mask[i] in ['1', 'X']:
            addr_list[i] = mask[i]
    # process for each possible permutation:
    for bits in bit_perms:
        act_addr = [c for c in addr_list]
        # replace addr X with actual permutation 0/1:
        for i in bits:
            act_addr[act_addr.index('X')] = i
        # write to mem (use string addr as memory addr hash)
        act_addr = "".join(act_addr)
        mem[act_addr] = int(value)




def problem2(input):
    global mem
    mask = 36*'0'
    for l in input:
        if l[0:4] == 'mask':
            mask = l.split('=')[1].strip()
            # print(mask)
        else:
            pieces = l.split('=')
            value = int(pieces[1])
            addr = int(re.match(r"mem\[(\d+)\]", l.strip()).group(1))
            # print(value)
            # print(addr)
            # print(apply_mask(mask, value))
            write_mem(mem2, mask, value, addr)
            # print()
    
    solution = sum(mem2.values())
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
