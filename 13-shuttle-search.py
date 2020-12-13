import time
import lib
import functools
import math
import re
from math import ceil, floor
import itertools


def read_input():
    # return list(lib.remove_empty(lib.readfile('inputs/12-input-sample.txt')))

    # input = list(lib.remove_empty(lib.readfile('inputs/13-input-sample.txt')))
    input = list(lib.remove_empty(lib.readfile('inputs/13-input.txt')))
    depart = int(input[0])
    buses = input[1].split(',')
    final_buses = []
    for b in buses:
        if b == 'x':
            final_buses.append(b)
        else:
            final_buses.append(int(b))
    return (depart, final_buses)


def problem1(input):
    depart = input[0]
    buses = input[1]
    min_dist = 10000000000
    min_id = 0

    for b in buses:
        if b == 'x':
            continue
        bus_arr = (depart // b) * b + b
        if bus_arr < min_dist:
            min_dist = bus_arr
            min_id = b

    solution = (min_dist - depart) * min_id
    print("Solution 1: {}".format(solution))


def extgcd(a, b):
    """
    https://de.wikipedia.org/wiki/Erweiterter_euklidischer_Algorithmus
    erweiterter euklidscher Algorithmus, für Chinese Remainder Theorem genutzt:
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, s, t = extgcd(b % a, a)
        return (g, t - (b // a) * s, s)


def chinesischer_restsatz(nn, rr):
    """
    Quelle: https://www.inf.hs-flensburg.de/lang/krypto/algo/chinese-remainder.htm
    Wir suchen x in den Gleichungen:
    x kongruent a  (mod m)   und
    x kongruent b  (mod n). 

    x ist dabei die erste "Abfahrtszeit", m,n unsere Inputs (Primzahlen),
      a, b die korrigierten Reste.
    """
    if len(nn) == 1:
        return nn[0], rr[0]
    else:
        k = len(nn)//2
        m, a = chinesischer_restsatz(nn[:k], rr[:k])
        n, b = chinesischer_restsatz(nn[k:], rr[k:])
        g, u, v = extgcd(m, n)
        x = (b-a)*u % n*m+a
        return m*n, x


def problem2(input):
    """
    Chinesisches Restsatz-Problem, siehe chinesischer_restsatz()
    """
    buses = input[1]
    modulos = []
    reste = []

    # Aufbereiten Modulos (die Input-Primzahlen) und der Reste
    # von bus[0] % akt_prim relativ zum verschobenen Index

    for i, x in enumerate(buses):
        if x == "x":
            continue
        modulos.append(x)
        reste.append(x-i)  # rest von 1. Zahl % x

    res = chinesischer_restsatz(modulos, reste)
    solution = res[1]
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
