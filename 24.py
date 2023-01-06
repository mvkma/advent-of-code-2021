from itertools import product

INPUT_FILE = "input_24"

SAMPLE1 = """inp x
mul x -1"""

SAMPLE2 = """inp z
inp x
mul z 3
eql z x"""

SAMPLE3 = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""

SAMPLE4 = """inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y"""

SAMPLE5 = """inp w
mul x 0
add x z
mod x 26
div z 26
add x 0
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 3
mul y x
add z y"""

def run_alu(program, input_function, w0=0, x0=0, y0=0, z0=0):
    if isinstance(input_function, (tuple, list)):
        digits = iter(input_function)
        input_function = lambda: next(digits)

    var = {"w": w0, "x": x0, "y": y0, "z": z0}

    for cmd, args in program:
        match cmd:
            case "inp":
                var[args[0]] = input_function()
            case "add":
                var[args[0]] += args[1] if isinstance(args[1], int) else var[args[1]]
            case "mul":
                var[args[0]] *= args[1] if isinstance(args[1], int) else var[args[1]]
            case "div":
                var[args[0]] //= args[1] if isinstance(args[1], int) else var[args[1]]
            case "mod":
                var[args[0]] %= args[1] if isinstance(args[1], int) else var[args[1]]
            case "eql":
                if isinstance(args[1], int) and args[1] == var[args[0]]:
                    var[args[0]] = 1
                elif isinstance(args[1], str) and var[args[1]] == var[args[0]]:
                    var[args[0]] = 1
                else:
                    var[args[0]] = 0

    return var
            
def parse_line(line):
    cmd = line[:3]
    args = []
    for c in line[4:].strip().split():
        try:
            args.append(int(c))
        except ValueError:
            args.append(c)

    return (cmd, tuple(args))

if __name__ == "__main__":
    program = [parse_line(line) for line in SAMPLE1.splitlines()]
    program = [parse_line(line) for line in SAMPLE2.splitlines()]
    program = [parse_line(line) for line in SAMPLE3.splitlines()]

    with open(INPUT_FILE) as f:
        program = [parse_line(line) for line in f.readlines()]

    prog1 = [parse_line(line) for line in SAMPLE4.splitlines()]
    prog26 = [parse_line(line) for line in SAMPLE5.splitlines()]

    digits_largest = [0] * 14
    digits_smallest = [0] * 14
    q = []
    for i in range(0, len(program), 18):
        if program[i + 4][1][1] == 1:
            add_y = program[i + 15][1][1]
            q.append((i // 18, add_y))
        else:
            add_x = program[i + 5][1][1]
            j, add_y = q.pop()
            t = add_x + add_y
            if t > 0:
                digits_largest[i // 18] = 9
                digits_largest[j] = 9 - t
                digits_smallest[i // 18] = 1 + t
                digits_smallest[j] = 1
            else:
                digits_largest[i // 18] = 9 + t
                digits_largest[j] = 9
                digits_smallest[i // 18] = 1
                digits_smallest[j] = 1 - t

    assert run_alu(program, digits_largest)["z"] == 0
    assert run_alu(program, digits_smallest)["z"] == 0

    print("".join(str(d) for d in digits_largest))
    print("".join(str(d) for d in digits_smallest))

# inp w

# mul x 0    x = 0
# add x z    x = x + z
# mod x 26   x = x % 26             (z % 26, y, z)

# div z 1    z = z // 1             (z % 26, y, z // 1)
# add x 10   x = x + 10
# eql x w    1 if x == w else 0
# eql x 0    1 if x == 0 else 0     (1, y, z // 1)

# mul y 0    y = 0
# add y 25   y = y + 25
# mul y x    y = y * x
# add y 1    y = y + 1
# mul z y    z = z * y              (1, 26, (z // 1) * 26)

# mul y 0    y = 0
# add y w    y = y + w
# add y 12   y = y + 12
# mul y x    y = y * x
# add z y    z = z + y              (1, (w + 12) * 1, (z // 1) * 26 + (w + 12) * 1)



# inp w

# mul x 0    x = 0
# add x z    x = x + z
# mod x 26   x = x % 26             (z % 26, y, z)

# div z 26   z = z // 26
# add x 0    x = x + 0
# eql x w    1 if x == w else 0
# eql x 0    1 if x == 0 else 0     (s, y, z // 26)

# mul y 0    y = 0
# add y 25   y = y + 25
# mul y x    y = y * x
# add y 1    y = y + 1
# mul z y    z = z * y              (s, s * 25 + 1, (z // 26) * (s * 25 + 1))

# mul y 0    y = 0
# add y w    y = y + w
# add y 3    y = y + 3
# mul y x    y = y * x
# add z y    z = z + y              (s, (w + 3) * s, (z // 26) * (s * 25 + 1) + (w + 3) * s)
