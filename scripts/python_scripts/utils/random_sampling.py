#!/usr/bin/env python
import sys
import fileinput
import random

if len(sys.argv) != 2:
    print("usage:\t" + sys.argv[0] + " <N>")
    exit(1)

N = int(sys.argv[1])

S = []

i = 0

for line in sys.stdin:
    if i < N:
        S.append(line)
    else:
        j = random.randint(0,i)
        if j < N:
            S[j] = line
    i += 1

for line in S:
    print(line.rstrip())
