INPUT_FILE = "input_13"

SAMPLE = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

def fold(dots, line):
    which, n = line.split("=")
    n = int(n)

    new_dots = set()

    if which == "y":
        for xx, yy in dots:
            if yy < n:
                new_dots.add((xx, yy))
            else:
                new_dots.add((xx, n - (yy - n)))

    elif which == "x":
        for xx, yy in dots:
            if xx < n:
                new_dots.add((xx, yy))
            else:
                new_dots.add((n - (xx - n), yy))

    return new_dots

def print_dots(dots):
    xmax = max(xx for xx, yy in dots)
    ymax = max(yy for xx, yy in dots)

    for yy in range(ymax + 1):
        for xx in range(xmax + 1):
            if (xx, yy) in dots:
                print("#", end="")
            else:
                print(".", end="")

        print()

if __name__ == "__main__":
    dots_done = False
    dots = set()
    folds = []

    with open(INPUT_FILE) as f:
        for line in f:
        # for line in SAMPLE.splitlines():
            line = line.strip()

            if line == "":
                dots_done = True
                continue

            if dots_done:
                folds.append(line.split()[2])
            else:
                dots.add(tuple(map(int, line.split(","))))

    print(len(fold(dots, folds[0])))

    out = dots.copy()
    for f in folds:
        out = fold(out, f)

    print_dots(out)
