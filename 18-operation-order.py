import time
import lib
import functools
import math
import re
from math import ceil, floor
from itertools import product
import operator

def read_input():
    # input = lib.remove_empty(lib.readfile('inputs/18-input-sample.txt'))
    input = lib.remove_empty(lib.readfile('inputs/18-input.txt'))
    return input

def parse_expr(input):
    """
        builds the expression tree from the input.
        there are 3 types of syntax elements:
        - single numbers 0-9
        - operators: +, *
        - sub-expressions: returned as sub-list
        returns a list with parsed syntax elements
    """
    tree = []
    state = None
    brace_count = 0
    expr = ""
    # simple state machine for parsing the string:
    for i in range(0, len(input)):
        c = input[i]
        if state == 'expr':
            if c == '(':
                brace_count += 1
                expr = expr + c
            elif c == ')':
                brace_count -= 1
                if brace_count == 0:
                    tree.append(parse_expr(expr))
                    expr = ""
                    state = None
                else:
                    expr = expr + c
            else:
                expr = expr + c
        else:
            if re.match(r"[0-9]", c):
                tree.append(int(c))
            elif c in ['+', '*']:
                tree.append(c)
            elif c == '(':
                state = 'expr'
                brace_count = 1
    return tree

def evaluate(tree):
    """
    evaluates the syntax tree without operator precedence:
    """
    res = 0
    op = None
    for expr in tree:
        if isinstance(expr, list):
            expr = evaluate(expr)
        if isinstance(expr, int):
            if not op:
                res = expr
            elif op == '+':
                res += expr
            elif op == '*':
                res *= expr
            op = None
        elif expr in ['+','*']:
            op = expr
    return res

def evaluate_2(tree):
    """
    evaluates the syntax tree with '+' as operator precedence
    """
    if isinstance(tree, int):
        return tree

    # Step 1: evaluate all '+' operators:
    while '+' in tree:
        pi = tree.index('+')
        res = evaluate_2(tree[pi-1]) + evaluate_2(tree[pi+1])
        # replace a + b with res(a+b)
        left = tree[:pi-1]
        right = tree[pi+2:]
        left.append(res)
        tree = left + right
    
    # now, evaluate the rest:
    res = 0
    op = None
    for expr in tree:
        if isinstance(expr, list):
            expr = evaluate_2(expr)
        if isinstance(expr, int):
            if not op:
                res = expr
            elif op == '*':
                res *= expr
            op = None
        elif expr == '*':
            op = expr
    return res



def problem1(input):

    total = 0
    for l in input:
        tree = parse_expr(l)
        total += evaluate(tree)

    solution = total
    print("Solution 1: {}".format(solution))

def problem2(input):
    total = 0
    for l in input:
        tree = parse_expr(l)
        total += evaluate_2(tree)

    solution = total
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