import time
import lib
import functools
import math
import re
from math import ceil, floor
import itertools

class CPU:
    def __init__(self, prg):
        self.acc = 0
        self.iptr = 0
        self.run = 1

        # prg_mem consists of [ op, offset, count ]
        # op: op code, e.g. 'jmp'
        # offset: incr/decr value for op
        # count: nr of times this instruction was called (incremented internally)
        self.prg_mem = []
        self.orig_mem = prg
        self.reset()

    def reset(self):
        self.acc = 0
        self.iptr = 0
        self.run = 1
        # copy original memory into program memory (deep copy)
        # self.prg_mem = [[i for i in p] for p in self.orig_mem]
        self.prg_mem = []
        for i in range(0, len(self.orig_mem)):
            m = self.orig_mem[i]
            self.prg_mem.append([m[0], m[1], 0])

    def exec_next(self):
        if self.iptr >= 0 and self.iptr < len(self.prg_mem):
            instr = self.prg_mem[self.iptr]
            if instr[2] > 0:
                # already executed, stop here
                return False
            instr[2] += 1
            op = instr[0]
            incr = instr[1]
            if op == 'nop':
                self.iptr += 1
            elif op == 'acc':
                self.acc += incr
                self.iptr += 1
            elif op == 'jmp':
                self.iptr += incr
            return True
        else:
            self.run = 0
            return False

def read_input():
    # input = lib.readfile('inputs/08-input-sample.txt')
    input = lib.readfile('inputs/08-input.txt')
    m = re.compile(r"(\w+)\s+([+-]\d+)+")

    mem = []
    for line in input:
        g = m.match(line)
        if g:
            instr = [g.group(1), int(g.group(2)), 0]
            mem.append(instr)

    return CPU(mem)



def problem1(cpu):
    while cpu.exec_next():
        # noop
        pass

    solution = cpu.acc
    print("Solution 1: {}".format(solution))


def problem2(cpu):
    solution = 0
    for idx in range(0,len(cpu.prg_mem)):
        cpu.reset()
        instr = cpu.prg_mem[idx][0]
        if instr == 'nop':
            cpu.prg_mem[idx][0] = 'jmp'
        elif instr == 'jmp':
            cpu.prg_mem[idx][0] = 'nop'
        while cpu.exec_next():
            # noop
            pass
        if cpu.run == 0:
            solution = cpu.acc
            break

    print("Solution 2: {}".format(solution))


def main():
    title = "Advent of Code 2020!"
    print("{title}\n{line}\n\n".format(title=title, line="="*len(title)))

    input = read_input()

    t1 = lib.measure(lambda: problem1(input))
    print("Problem 1 took {:.4f}s to solve.\n\n".format(t1))

    t2 = lib.measure(lambda: problem2(input))
    print("Problem 2 took {:.4f}s to solve.".format(t2))


if __name__ == "__main__":
    main()
