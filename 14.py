from collections import defaultdict

INPUT_FILE = "input_14"

SAMPLE = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

def transform(state, rules):
    new_state = ""
    for i in range(len(state) - 1):
        pair = state[i : i + 2]

        if pair in rules:
            new_state = new_state + pair[0] + rules[pair]
        else:
            new_state = new_state + pair[0]

    new_state = new_state + state[-1]

    return new_state

def transform2(state, rules):
    new_state = defaultdict(int)

    for k, v in state.items():
        p1, p2 = rules[k]
        new_state[p1] += v
        new_state[p2] += v

    return new_state

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        # f = iter(SAMPLE.splitlines())

        rules = dict()
        initial_state = next(f).strip()
        next(f)

        for line in f:
            a, b = map(lambda s: s.strip(), line.split("->"))
            rules[a] = b

    # Part 1
    state = initial_state
    for _ in range(10):
        state = transform(state, rules)

    counts = {}
    for c in set(state):
        counts[c] = state.count(c)

    print(max(counts.values()) - min(counts.values()))

    # Part 2
    rules2 = dict()
    for k, v in rules.items():
        rules2[k] = (k[0] + v, v + k[1])

    state = defaultdict(int)
    for i in range(len(initial_state) - 1):
        state[initial_state[i : i + 2]] += 1

    for _ in range(40):
        state = transform2(state, rules2)

    counts = defaultdict(int)
    for c in set("".join(state.keys())):
        for k, v in state.items():
            counts[c] += k.count(c) * v

    for k, v in counts.items():
        if v % 2 == 0:
            counts[k] = v // 2
        else:
            counts[k] = (v + 1) // 2

    # TODO: off by one
    print(max(counts.values()) - min(counts.values()))
