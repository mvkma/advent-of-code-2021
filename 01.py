INPUT_FILE = "input_01"

SAMPLE = """199
200
208
210
200
207
240
269
260
263"""

if __name__ == "__main__":
    depths = []

    with open(INPUT_FILE) as f:
        for line in f:
        # for line in SAMPLE.splitlines():
            line = line.strip()
            depths.append(int(line))

    # Part 1
    k = 0
    for i in range(len(depths) - 1):
        if depths[i + 1] > depths[i]:
            k += 1

    print(k)

    # Part 2
    k = 0
    for i in range(len(depths) - 3):
        a = sum(depths[i : i + 3])
        b = sum(depths[i + 1 : i + 4])
        if b > a:
            k += 1

    print(k)
