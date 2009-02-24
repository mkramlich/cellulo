#!/usr/bin/env python2.5

from __future__ import with_statement

import random


def old_plus_one(dex, cells):
    return cells[dex] + 1

def neighborhood_sum(dex, cells):
    sum = cells[dex]
    if dex - 1 >= 0:
        sum += cells[dex-1]
    if dex + 1 < len(cells):
        sum += cells[dex+1]
    return sum

def neighborhood_avg(dex, cells):
    sum = cells[dex]
    num = 1
    if dex - 1 >= 0:
        sum += cells[dex-1]
        num += 1
    if dex + 1 < len(cells):
        sum += cells[dex+1]
        num += 1
    avg = sum / num
    return int(avg)

def hood_avg_plus_one(dex, cells):
    v = neighborhood_avg(dex,cells)
    return v + 1

def hood_sum_sometimes_resets(dex, cells):
    v = neighborhood_sum(dex,cells)
    if v >= 9:
        r = random.randint(0,4)
        if r == 0:
            v = 0
    return v

def sum_mapped(dex, cells):
    trans = {
        0:1,
        1:1,
        8:6,
        24:3,
        3:2,
        4:5,
        27:0
        }

    v = neighborhood_sum(dex,cells)
    if v in trans:
        return trans[v]
    else:
        return v # identity, if not found in trans

def clamp(val, minval, maxval):
    v = val
    if v > maxval:
        v = maxval
    if v < minval:
        v = minval
    return v

def filter(val):
    return clamp(val,0,9)

def generate(data_fname, evolve_fn_name, iters):
    cells = []
    with open(data_fname) as f:
        data = f.read().strip()
        for d in data:
            cells.append(int(d))

    def render(cells):
        return ''.join(map(lambda x: str(x), cells))

    results = []

    # first, print the cells as they appear in the starting state
    line = render(cells)
    results.append(line)

    # next, do <iters> iterations, updating the world state each time, and rendering and accumulating the output

    for i in range(iters):
        newcells = []
        evolve_fn = globals()[evolve_fn_name]
        for c in range(len(cells)):
            v = evolve_fn(c,cells)
            v = filter(v)
            newcells.append(v)
        cells = newcells
        line = render(cells)
        results.append(line)
    return results

def main(args):
    print 'Cellulo\n'

    data_fname     = len(args) > 1 and args[1]      or 'data/40_with_some_ones_and_twos'
    evolve_fn_name = len(args) > 2 and args[2]      or 'sum_mapped'
    iters          = len(args) > 3 and int(args[3]) or 20

    lines = generate(data_fname,evolve_fn_name,iters)
    for ln in lines:
        print ln

if __name__ == '__main__':
    import sys

    main(sys.argv)
