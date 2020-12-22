import time
import lib
from functools import reduce
import math
import re
from math import ceil, floor
from itertools import product
from collections import deque
import operator


def read_input():
    input = lib.remove_empty(lib.readfile('inputs/22-input.txt'))
    # input = lib.remove_empty(lib.readfile('inputs/22-input-sample.txt'))

    players = [deque(),deque()]
    p = -1
    for line in input:
        if re.match(r"Player", line):
            p += 1
        else:
            players[p].append(int(line))
    return players


def problem1(input):
    player1, player2 = deque(input[0]), deque(input[1])

    while len(player1) and len(player2):
        drawn = (player1.popleft(), player2.popleft())
        if drawn[0] > drawn[1]:
            player1.append(drawn[0])
            player1.append(drawn[1])
        else:
            player2.append(drawn[1])
            player2.append(drawn[0])

    winner = player1 if len(player1) else player2
    score = 0
    for i,nr in enumerate(winner):
        score += nr * (len(winner)-i)

    solution = score
    print("Solution 1: {}".format(solution))

def play_recursive(player1, player2):
    
    seen_cards = set()

    while len(player1) and len(player2):

        # check if aready played:
        h = hash((str(player1),str(player2)))
        if h in seen_cards:
            return 0 # player1 wins
        seen_cards.add(h)

        drawn = ( player1.popleft(), player2.popleft())
        if len(player1) >= drawn[0] and len(player2) >= drawn[1]:
            res = play_recursive(deque(list(player1)[:drawn[0]]), deque(list(player2)[:drawn[1]]))
            if res == 0:
                player1.append(drawn[0])
                player1.append(drawn[1])
            else:
                player2.append(drawn[1])
                player2.append(drawn[0])
        else:
            if drawn[0] > drawn[1]:
                player1.append(drawn[0])
                player1.append(drawn[1])
            else:
                player2.append(drawn[1])
                player2.append(drawn[0])
    res = 0 if len(player1) else 1
    return res


def problem2(input):
    player1, player2 = deque(input[0]), deque(input[1])
    res = play_recursive(player1, player2)

    winner = player1 if res == 0 else player2
    score = 0
    for i,nr in enumerate(winner):
        score += nr * (len(winner)-i)

    solution = score
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
