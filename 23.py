from collections import deque
from heapq import heappop, heappush

INPUT_FILE = "input_23"

SAMPLE = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

ENERGIES = {"A": 1, "B": 10, "C": 100, "D": 1000}

ROOMS = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

HALLWAY = (0, 1, 3, 5, 7, 9, 10)

def print_map(state):
    print("#" * 13)
    print("#" + state[:11] + "#")
    p = 11
    print("##" + "".join(a + b for a, b in zip("#" * 4, state[p : p + 4])) + "###")
    p = 15

    while p < len(state):
        print("  " + "".join(a + b for a, b in zip("#" * 4, state[p : p + 4])) + "#  ")
        p += 4
    print("  " + "#" * 9 + "  ")

def can_move(start, end, state):
    if start < end:
        s = 1
    else:
        s = -1

    for pos in range(start + s, end + s, s):
        if state[pos] != ".":
            return False

    return True

def can_move_into_target(item, state, targets):
    steps = 0
    dest = None

    for target in targets[item]:
        if state[target - 11] == ".":
            dest = target
            steps += 1
            continue

        if state[target - 11] != item:
            dest = None
            break

    return dest, steps

def can_move_out_of_room(room, state, targets):
    steps = 0

    for pos in targets[room]:
        item = state[pos - 11]
        steps += 1

        if item == ".":
            continue

        item_targets = targets[item]
        if pos in item_targets:
            correct = True
            ix = item_targets.index(pos)
            for other in item_targets[ix + 1:]:
                if other != item:
                    correct = False
                    break

            if correct:
                continue

        return pos, steps

    return None, steps

def get_moves(state, targets):
    moves = list()

    # First try to move from the hallway into the rooms
    # Can we move from the hallway into the target?
    positions_hallway = [pos for pos in HALLWAY if state[pos] != "."]

    for pos in positions_hallway:
        item = state[pos]
        energy = ENERGIES[item]

        target, steps = can_move_into_target(item, state[11:], targets)

        if target is not None and can_move(pos, ROOMS[item], state):
            cost = (steps + abs(ROOMS[item] - pos)) * energy
            yield pos, target, cost

    # Can we move out?
    for room in ROOMS.keys():

        source, steps = can_move_out_of_room(room, state[11:], targets)

        if source is None:
            continue

        item = state[source]

        energy = ENERGIES[item]

        # Moves into the hallway
        for pos in HALLWAY:
            if can_move(ROOMS[room], pos, state):
                cost = (abs(ROOMS[room] - pos) + steps) * energy
                yield source, pos, cost

        target, nsteps = can_move_into_target(item, state[11:], targets)

        if target is not None and can_move(ROOMS[room], ROOMS[item], state):
            cost = (abs(ROOMS[room] - ROOMS[item]) + steps + nsteps) * energy
            yield source, target, cost

def find_solution(initial_state, final_state):
    targets = {item: tuple(pos for pos, c in enumerate(final_state) if c == item) for item in "ABCD"}

    q = []
    heappush(q, (0, initial_state))

    hist = {initial_state: 0}
    best = 100_000_000

    while len(q) > 0:

        energy, state = heappop(q)

        if state == final_state:
            best = min(best, energy)

        for s, e, cost in get_moves(state, targets):
            if s < e:
                nstate = state[:s] + state[e] + state[s + 1 : e] + state[s] + state[e + 1:]
            else:
                nstate = state[:e] + state[s] + state[e + 1 : s] + state[e] + state[s + 1:]

            nenergy = cost + energy

            if nstate in hist and hist[nstate] <= nenergy:
                continue

            hist[nstate] = nenergy
            heappush(q, (nenergy, nstate))

    return best

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        initial_state = "".join([c for c in f.read() if c in "ABCD."])

    # initial_state = "".join([c for c in SAMPLE if c in "ABCD."])
    # print_map(initial_state)

    # Part 1
    final_state = "." * 11 + "ABCDABCD"
    print(find_solution(initial_state, final_state))

    # Part 2
    bigger_initial_state = initial_state[:15] + "DCBADBAC" + initial_state[15:]
    # print_map(bigger_initial_state)

    bigger_final_state = "." * 11 + "ABCDABCDABCDABCD"
    print(find_solution(bigger_initial_state, bigger_final_state))
