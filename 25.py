INPUT_FILE = "input_25"

SAMPLE1 = """...>>>>>..."""

SAMPLE2 = """..........
.>v....v..
.......>..
.........."""

SAMPLE3 = """...>...
.......
......>
v.....>
......>
.......
..vvv.."""

SAMPLE4 = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

def print_map(east, south, size):
    positions = east.union(south)

    xmax, ymax = size
    xmin, ymin = 0, 0

    for yy in range(ymin, ymax):
        line = ""
        for xx in range(xmin, xmax):
            if (xx, yy) in south:
                line += "v"
            elif (xx, yy) in east:
                line += ">"
            else:
                line += "."

        print(line)

def move(east, south, direction, size):
    positions = east.union(south)

    dx, dy = direction
    ncols, nrows = size

    moved = 0
    new_east = set()
    for xx, yy in east:
        nxx, nyy = (xx + dx) % ncols, (yy + dy) % nrows
        if (nxx, nyy) in positions:
            new_east.add((xx, yy))
        else:
            new_east.add((nxx, nyy))
            moved += 1

    return new_east, south, moved

if __name__ == "__main__":
    south = set()
    east = set()

    nrows = 0
    ncols = 0

    with open(INPUT_FILE) as f:
        # for yy, line in enumerate(SAMPLE4.splitlines()):
        for yy, line in enumerate(f):
            for xx, c in enumerate(line.strip()):
                match c:
                    case ">": east.add((xx, yy))
                    case "v": south.add((xx, yy))
                    case ".": continue

            ncols = max(xx + 1, ncols)

        nrows = yy + 1
        size = (ncols, nrows)

    print_map(east, south, size)
    print()
    k = 0
    while True:
        east, south, moved1 = move(east, south, (+1, 0), size)
        south, east, moved2 = move(south, east, (0, +1), size)

        if moved1 == 0 and moved2 == 0:
            print(k + 1)
            break

        k += 1

