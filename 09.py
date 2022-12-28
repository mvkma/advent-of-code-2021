from functools import reduce

INPUT_FILE = "input_09"

SAMPLE = """2199943210
3987894921
9856789892
8767896789
9899965678"""

def get_neighbors(xx, yy, ncols, nrows):
    ns = set()

    for dx, dy in ((-1, 0), (+1, 0), (0, -1), (0, +1)):
        nxx = xx + dx
        nyy = yy + dy

        if 0 <= nxx < ncols and 0 <= nyy < nrows:
            ns.add((nxx, nyy))

    return ns

def find_low_points(grid):
    nrows = len(grid)
    ncols = len(grid[0])

    low_points = set()

    for yy in range(nrows):
        for xx in range(ncols):
            if all(grid[nyy][nxx] > grid[yy][xx] for nxx, nyy in get_neighbors(xx, yy, ncols, nrows)):
                low_points.add((xx, yy))

    return low_points

def basin_size(grid, point):
    nrows = len(grid)
    ncols = len(grid[0])

    q = []
    q.append(point)
    seen = set()

    while len(q) > 0:
        xx, yy = q.pop()

        if grid[yy][xx] == 9:
            continue

        seen.add((xx, yy))

        for nxx, nyy in get_neighbors(xx, yy, ncols, nrows):
            if (nxx, nyy) in seen:
                continue

            q.append((nxx, nyy))

    return len(seen)

if __name__ == "__main__":
    grid = []

    with open(INPUT_FILE) as f:
        for line in f:
        # for line in SAMPLE.splitlines():
            line = line.strip()
            grid.append([int(c) for c in line])

    low_points = find_low_points(grid)
    risk = sum(grid[yy][xx] + 1 for xx, yy in low_points)
    print(risk)

    basin_sizes = []
    for p in low_points:
        basin_sizes.append(basin_size(grid, p))

    res = reduce(lambda a, b: a * b, sorted(basin_sizes)[-3:])
    print(res)
