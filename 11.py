INPUT_FILE = "input_11"

SAMPLE1 = """11111
19991
19191
19991
11111"""

SAMPLE2 = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

def get_neighbors(xx, yy, ncols, nrows):
    ns = set()

    for dx, dy in ((+1, 0), (-1, 0), (0, +1), (0, -1),
                   (+1, +1), (+1, -1), (-1, +1), (-1, -1)):
        nxx = xx + dx
        nyy = yy + dy
        if 0 <= nxx < ncols and 0 <= nyy < nrows:
            ns.add((nxx, nyy))

    return ns

def step(grid):
    nrows = len(grid)
    ncols = len(grid[0])

    for yy in range(nrows):
        for xx in range(ncols):
            grid[yy][xx] += 1

    flashed = set()

    done = False
    while not done:
        done = True

        for yy in range(nrows):
            for xx in range(ncols):
                if grid[yy][xx] <= 9 or (xx, yy) in flashed:
                    continue

                done = False
                flashed.add((xx, yy))

                for nxx, nyy in get_neighbors(xx, yy, ncols, nrows):
                    grid[nyy][nxx] += 1

    for nxx, nyy in flashed:
        grid[nyy][nxx] = 0

    return len(flashed)

def print_grid(grid):
    print("\n".join("".join(str(c) for c in row) for row in grid))
    print()

if __name__ == "__main__":
    grid = []

    with open(INPUT_FILE) as f:
        # for line in SAMPLE1.splitlines():
        # for line in SAMPLE2.splitlines():
        for line in f:
            line = line.strip()
            grid.append([int(c) for c in line])

    nflashes = 0
    k = 0
    while True:
        n = step(grid)
        nflashes += n

        if k == 99:
            print(nflashes)

        if n == 100:
            print(k + 1)
            break

        k += 1

