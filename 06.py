INPUT_FILE = "input_06"

SAMPLE = """3,4,3,1,2"""

def evolve(state):
    for i in range(len(state)):
        v = state[i]

        if v == 0:
            state[i] = 6
            state.append(8)
        else:
            state[i] = v - 1

    return state

def evolve2(state):
    new_state = {k: 0 for k, n in state.items()}

    for v, n in state.items():
        if v == 0:
            new_state[8] += n
            new_state[6] += n
        else:
            new_state[v - 1] += n

    return new_state

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        for line in f:
        # for line in SAMPLE.splitlines():
            line = line.strip()
            initial_state = list(map(int, line.split(",")))

    # Part 1
    state = initial_state.copy()
    for _ in range(80):
        state = evolve(state)

    print(len(state))

    # Part 2
    nfish = {k: initial_state.count(k) for k in range(9)}

    for _ in range(256):
        nfish = evolve2(nfish)

    print(sum(nfish.values()))

