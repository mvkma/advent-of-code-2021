INPUT_FILE = "input_02"

SAMPLE = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""

if __name__ == "__main__":
    commands = []

    with open(INPUT_FILE) as f:
        for line in f:
        # for line in SAMPLE.splitlines():
            line = line.strip()
            cmd, n = line.split()
            commands.append((cmd, int(n)))

    # Part 1
    hpos = 0
    depth = 0

    for cmd, n in commands:
        match cmd:
            case "forward":
                hpos += n
            case "down":
                depth += n
            case "up":
                depth -= n
            case _:
                raise ValueError(f"Unknown command: {cmd}")

    print(hpos, depth, hpos * depth)

    # Part 2
    aim = 0
    hpos = 0
    depth = 0

    for cmd, n in commands:
        match cmd:
            case "forward":
                hpos += n
                depth += aim * n
            case "down":
                aim += n
            case "up":
                aim -= n
            case _:
                raise ValueError(f"Unknown command: {cmd}")

    print(aim, hpos, depth, hpos * depth)
