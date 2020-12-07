Advent of Code 2020
====================

My year 2020 solutions for [ Advent of Code ](https://adventofcode.com/2020). 

This year I will try Python as language,
first because it is simple and has a lot of "batteries included" for number-crunching tasks, 2nd because my
Python skills are somewhat rusty.

## Diary

### Day Zero - Setup

Today I just set up my env, did a proof-of-concept implementation ([ Puzzle #1 from last year ](https://adventofcode.com/2019/day/1)),
and organized my files.

First outcome: a lib with:

* `fn measure(Function)`: executes the given function and returns its time needed to run
* `fn readfile(file, sep)`: reads a file, returns a list with its lines, or a split version of a line.


### Day 01 - Report Repair

As always, that one was easy - double loop through some list and find some that match a criteria -
nice for setting all things up and to get warm.

Just used a O(n^2) / O(n^3) loop structure, which didn't need optimization, as the list was short enough:

Solution 1 took 2.5ms, Solution 2 took 87ms with python 3 on my MacBook Pro 2014.

### Day 02 - Password Philosophy

A simple string count / regex excercise. One nice thing I learned with python today:

- it's super-simple to count nr of chars / substrings in a string: `str.count(substr)`
- working with grouped regex also is extremely simple:
```python
import re
# find format: '(nr)-(nr) (char): (*)'
# matches something like: 1-3 a: abcde
m = re.compile("(\d+)-(\d+)\s+(.):\s+(.*)")
g = m.match(str)
if g:
    group1 = g.group(1)
```

So python makes things really simple


### Day 03 - Toboggan Trajectory

A modulo exercise - move within a wrapping plane (a cylinder, if you want), and count
occurences of values. Trivial finger-excercise :-)


### Day 04 - Passport Processing

This day was all about string parsing / matching:

* Split entries by newline separator (as in http header/body, e.g.)
* split single entry into key/value
* match entries against a set of rules

... and some book-keeping of all the matched rules. This excercise was simple in the end, but required a bit of typing / exact rule definition.

What I learned in python today:

* check if an array is contained in another array: `set(small_arr).issubset(set(large_arr))` --> Attention: this checks only for unique entries (e.g. in `[1,1,2,3,3,3,4]` it only checks if `1,2,3,4` is present)
* check if value is in array/set: `x in arr`
* pattern matching / regular expression matching, the simple way:
  just check if a string matches a pattern: `re.match(r"pattern", string)`

### Day 05 - Binary Boarding

Solution 1 was all about bisect - I converted the input ticket strings into int arrays (e.g. `FFBBBFFLRL` became `[1,1,0,0,0,1,1,1,0,1]` ), then to find the
row / col was just a bisect in a number range - aka binary search in the number range. So far, so simple.

For the 2nd part, we had to find one missing ticket by 1) find the set of missing
tickets from all possible tickets (that is, from the set from `0000000000` to `1111111111`). This is where things got ugly:

I created both sets as string representations, diffed the two sets to get the missing entries, then converted them back to int arrays to calc the ticket ids.

all in all it took only about 100ms, but sill... somehow there has to be a
better, more numeric solution than to diff strings...

==> **First Iteration**: I found a more elegant solution now:

I did not convert the input into int arrays, but only replaced the chars with
number strings - (e.g. `FFBBBFFLRL` became `1100011101` ). This way I didn't
have to convert it from/to int arrays.

It became much faster through this - both solutions together take only 66ms now.

==> **Second Iteration**: I now do NOT convert the strings - I just use the
original chars - this way I don't neet to convert to ints - and I do not need
to convert my full list, I can just use the `itertools.product` from python to 
generate full list.

speed gain: again - a lot: runs in 36ms now.

==> **Third Iteration**: Ah, crap! there is a MUCH SIMPLER solution for this problem: There is no need to create full ticket lists, calculate its ids etc...

Just look for a gap in the already taken ID list (sort id list, check for a distance of 2), then the missing ID is already there....

With this approach, it took 30ms in total...


I learned in python:

* diff 2 lists is super-easy: `list(set(list1) - set(list2))`
* create full combinations of a set of chars, here: (0,1) for length 10: `itertools.product([0,1], repeat = 10)`

I learned in general:

Think twice!

### Day 06 - Custom Customs

All about counting groups - so a lookup table exercise - I used python's `dict()`
and `set()` to achieve this. Form groups (keys) and count the answers either
in sum or per member.

Nothing new so far for me in python.

### Day 07 - Handy Haversacks

This day was about Graphs and graph travel, in this case, a directed graph
which forced you to do loop detection:

Bags ( aka Graph Nodes ) can contain other bags, which again can contain other
bags etc. This spans a nice directed graph.


Problem 1 + 2 both required you to travel the graph, with slighly different
tasks. So I implemented 2 `visit()` methods which
did the graph traversal with loop detection.

The problems now become more tense, as days go by ...
