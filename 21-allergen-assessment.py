import time
import lib
from functools import reduce
import math
import re
from math import ceil, floor
from itertools import product
import operator


def read_input():
    input = lib.readfile('inputs/21-input.txt')
    # input = lib.remove_empty(lib.readfile('inputs/21-input-sample.txt'))
    foods = []
    ingredients = dict()
    allergens = set()
    m = re.compile(r"(.*)\s+\(contains (.*)\)")
    for l in input:
        g = m.match(l)
        if g:
            ingr = g.group(1).split(' ')
            allergs = g.group(2).split(', ')
            foods.append((ingr, allergs))
            for i in ingr:
                ingredients[i] = set()
            for a in allergs:
                allergens.add(a)
    return (foods, ingredients, allergens)


def problem1(input):
    foods, ingredients, allergens = input

    # build a list of ingredients with their *possible* allergens:
    for (ingrs, allergs) in foods:
        for i in ingrs:
            for a in allergs:
                ingredients[i].add(a)


    # loop through all ingredients, check if we can eliminate an allergen:
    changed = True
    while changed:
        changed = False
        for i,a in ingredients.items():
            mark_for_removal = set()
            for act_a in a:
                # check if we can find the actual ingredient in a food which contains the allergen
                # if not, that ingredient cannot have that allergen:
                for (foreign_ingredients, foreign_allergen) in foods:
                    if act_a in foreign_allergen and i not in foreign_ingredients:
                        mark_for_removal.add(act_a)
                        changed = True
            if len(mark_for_removal):
                for rem in mark_for_removal:
                    a.remove(rem)

    # count how many times an allergy-free ingredient occurs:
    allergen_free_ingredients = []
    allergen_free_counter = 0
    for i,a in ingredients.items():
        if not len(a):
            allergen_free_ingredients.append(i)
            for (ingrs, allergs) in foods:
                if i in ingrs:
                    allergen_free_counter += 1

    solution = allergen_free_counter
    print("Solution 1: {}".format(solution))

def problem2(input):
    foods, ingredients, allergens = input

    # now, the ingredient map already contains only the possible allergens.
    # eliminate possibilities to search for an ingredient with only one allergen, eliminate
    # on all other ingredients:
    allerg_ingr_map = dict()
    while True:
        ingr = None
        # find the one with only 1 allergen:
        for act_ingredient,act_allergens in ingredients.items():
            if len(act_allergens) == 1:
                ingr = act_ingredient
                allerg = act_allergens.pop()
                allerg_ingr_map[allerg] = ingr
                # remove that allergen from all ingredients:
                for a in ingredients.values():
                    if allerg in a:
                        a.remove(allerg)
                break
        if not ingr:
            break
    # now, get a list of ingredients from their allergenes,
    # sort by allergene key first:
    solution = ",".join([i for i in map(lambda k: allerg_ingr_map[k], sorted(allerg_ingr_map.keys()))])
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
