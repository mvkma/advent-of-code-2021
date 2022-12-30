import re

INPUT_FILE = "input_17"

SAMPLE = """target area: x=20..30, y=-10..-5"""

def step(pos, vel):
    xx, yy = pos
    vx, vy = vel

    xx = xx + vx
    yy = yy + vy

    if vx > 0:
        vx = vx - 1
    elif vx < 0:
        vx = vx + 1
    else:
        vx = 0

    vy = vy - 1

    return (xx, yy), (vx, vy)

def hits_target(pos, vel, target):
    xmin, xmax, ymin, ymax = target

    hit = False
    max_height = pos[1]

    t = 0
    while True and t < 1000:
        if xmin <= pos[0] <= xmax and ymin <= pos[1] <= ymax:
            hit = True
            break

        if pos[0] > xmax and vel[0] > 0:
            break

        if pos[1] < ymin and vel[1] < 0:
            break

        pos, vel = step(pos, vel)            
        max_height = max(max_height, pos[1])
        t += 1

    return hit, t, max_height

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        # line = SAMPLE
        line = f.readline().strip()

    xmin, xmax, ymin, ymax = map(int, re.findall("[-]*\d+", line))
    target = (xmin, xmax, ymin, ymax)

    highest = 0
    best = None
    possible_velocities = []

    for vx in range(400):
        for vy in range(-400, 400):
            hit, t, max_height = hits_target((0, 0), (vx, vy), target)
            if hit:
                possible_velocities.append((vx, vy))
                if max_height >= highest:
                    best = (vx, vy)
                    highest = max_height

    print(highest, best)
    print(len(possible_velocities))
