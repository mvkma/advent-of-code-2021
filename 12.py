from collections import defaultdict

INPUT_FILE = "input_12"

SAMPLE1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

SAMPLE2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

SAMPLE3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

if __name__ == "__main__":
    graph = defaultdict(list)

    with open(INPUT_FILE) as f:
        # for line in SAMPLE1.splitlines():
        for line in f:
            line = line.strip()
            a, b = line.split("-")

            graph[a].append(b)
            graph[b].append(a)

    # Part 1
    q = [("start",)]
    paths = []

    while len(q) > 0:
        cur = q.pop()

        if cur[-1] == "end":
            paths.append(cur)
            continue

        if cur[-1].islower() and cur[-1] in cur[:-1]:
            continue

        for neighbor in graph[cur[-1]]:
            q.append(cur + (neighbor,))

    print(len(paths))

    # Part 2
    q = [(("start",), False)]
    paths = []

    while len(q) > 0:
        cur, small_twice = q.pop()

        if cur[-1] == "end":
            paths.append(cur)
            continue

        for neighbor in graph[cur[-1]]:
            if neighbor == "start":
                continue

            if neighbor.islower() and neighbor in cur:
                if small_twice:
                    continue

                q.append((cur + (neighbor,), True))
            else:
                q.append((cur + (neighbor,), small_twice))

    print(len(paths))
