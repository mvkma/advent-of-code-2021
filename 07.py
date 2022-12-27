INPUT_FILE = "input_07"

SAMPLE = "16,1,2,0,4,2,7,1,2,14"

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        # hpos = list(map(int, SAMPLE.split(",")))
        hpos = list(map(int, f.readline().strip().split(",")))

    hmin = min(hpos)
    hmax = max(hpos)

    # Part 1
    best = sum(abs(pos - hmin) for pos in hpos)
    best_pos = hmin

    for target in range(hmin, hmax):
        cost = sum(abs(pos - target) for pos in hpos)
        if cost < best:
            best_pos = target
            best = cost

    print(best_pos, best)
            
    # Part 2
    best = sum(sum(range(1, abs(pos - hmin) + 1)) for pos in hpos)
    best_pos = hmin

    for target in range(hmin, hmax):
        cost = sum(sum(range(1, abs(pos - target) + 1)) for pos in hpos)
        if cost < best:
            best_pos = target
            best = cost

    print(best_pos, best)
            
