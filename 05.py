import re
from collections import defaultdict

INPUT_FILE = "input_05"

SAMPLE = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

if __name__ == "__main__":
    lines = []

    with open(INPUT_FILE) as f:
        # for line in SAMPLE.splitlines():
        for line in f:
            x1, y1, x2, y2 = map(int, re.findall("\d+", line))

            lines.append(((x1, y1), (x2, y2)))

    # Part 1
    covered = defaultdict(int)

    for start, end in lines:
        x1, y1 = start
        x2, y2 = end

        if x1 != x2 and y1 != y2:
            continue

        if y1 == y2 and x1 > x2:
            x2, x1 = x1, x2

        if x1 == x2 and y1 > y2:
            y2, y1 = y1, y2

        for xx in range(x1, x2 + 1):
            for yy in range(y1, y2 + 1):
                covered[(xx, yy)] += 1

    print(sum(int(v > 1) for v in covered.values()))

    # Part 2
    covered = defaultdict(int)

    for start, end in lines:
        x1, y1 = start
        x2, y2 = end

        if x1 == x2:
            dx = 0
        elif x1 > x2:
            dx = -1
        else:
            dx = +1

        if y1 == y2:
            dy = 0
        elif y1 > y2:
            dy = -1
        else:
            dy = +1

        xx, yy = start
        covered[(xx, yy)] += 1
        while (xx, yy) != end:
            xx, yy = xx + dx, yy + dy
            covered[(xx, yy)] += 1

    print(sum(int(v > 1) for v in covered.values()))

