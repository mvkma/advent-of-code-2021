from collections import deque, defaultdict
from heapq import heappop, heappush
from functools import cache
import math

INPUT_FILE = "input_15"

SAMPLE = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

@cache
def get_neighbors(xx, yy, ncols, nrows):
    ns = []

    for dx, dy in ((+1, 0), (-1, 0), (0, +1), (0, -1)):
        nxx = xx + dx
        nyy = yy + dy

        if 0 <= nxx < ncols and 0 <= nyy < nrows:
            ns.append((nxx, nyy))

    return ns

def min_risk_path(start, end, grid):
    nrows = len(grid)
    ncols = len(grid[0])

    q = []
    heappush(q, (0, start))
    seen = dict()
    seen[start] = 0

    k = 0
    while len(q) > 0:

        risk, cur = heappop(q)

        for ncur in get_neighbors(*cur, ncols, nrows):
            if ncur in seen.keys():
                continue

            nrisk = min(risk + grid[ncur[1]][ncur[0]], seen.get(ncur, math.inf))

            seen[ncur] = nrisk
            heappush(q, (nrisk, ncur))

    return seen[end]

def mmod(n, m):
    r = n % m
    if r == 0:
        return m
    else:
        return r

if __name__ == "__main__":
    grid = []

    with open(INPUT_FILE) as f:
        for line in f:
        # for line in SAMPLE.splitlines():
            line = line.strip()
            grid.append([int(c) for c in line])

    best = min_risk_path((0, 0), (len(grid[0]) - 1, len(grid) - 1), grid)
    print(best)

    large_grid = []
    for j in range(5):
        for row in grid:
            new_row = []
            for i in range(5):
                new_row += [mmod(n + i + j, 9) for n in row]
            large_grid.append(new_row)

    best = min_risk_path((0, 0), (len(large_grid[0]) - 1, len(large_grid) - 1), large_grid)
    print(best)
