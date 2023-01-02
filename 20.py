INPUT_FILE = "input_20"

SAMPLE = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""

def decode(algorithm, seed, i, j, fill):
    n = 0
    b = 8
    for l in range(j - 1, j + 2):
        for k in range(i - 1, i + 2):
            if 0 <= k < len(seed[0]) and 0 <= l < len(seed):
                if seed[l][k] == "#":
                    n += 2**b
            else:
                if fill == "#":
                    n += 2**b

            b -= 1

    assert b == -1

    return algorithm[n]

def decode_image(algorithm, seed, fill):
    nrows = len(seed) + 2
    ncols = len(seed[0]) + 2

    output = [[fill] * ncols for _ in range(nrows)]

    for j in range(nrows):
        for i in range(ncols):
            output[j][i] = decode(algorithm, seed, i - 1, j - 1, fill)

    return output

def print_grid(grid):
    print("\n".join("".join(row) for row in grid))

def count_pixels(grid):
    return "".join("".join(row) for row in grid).count("#")

if __name__ == "__main__":
    input_image = []

    with open(INPUT_FILE) as f:
        # f = iter(SAMPLE.splitlines())

        algorithm = next(f).strip()
        next(f)

        for line in f:
            input_image.append(list(line.strip()))

    print(len(algorithm))
    print(len(input_image), len(input_image[0]))

    image = input_image
    for i in range(50):
        if algorithm[0] == "#" and i % 2 == 1:
            fill = "#"
        else:
            fill = "."

        image = decode_image(algorithm, image, fill)

        if i == 1:
            print(count_pixels(image))

    print(count_pixels(image))
