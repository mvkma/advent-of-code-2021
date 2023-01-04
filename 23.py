from collections import deque
from functools import reduce, cache
from heapq import heappop, heappush
import math

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

TARGETS = {
    "A": (11, 15, 19, 23),
    "B": (12, 16, 20, 24),
    "C": (13, 17, 21, 25),
    "D": (14, 18, 22, 26),
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

@cache
def can_move(start, end, state):
    if start < end:
        s = 1
    else:
        s = -1

    for pos in range(start + s, end + s, s):
        if state[pos] != ".":
            return False

    return True

@cache
def can_move_into_target(item, state):
    steps = 0
    dest = None

    for target in TARGETS[item]:
        if state[target - 11] == ".":
            dest = target
            steps += 1
            continue

        if state[target - 11] != item:
            dest = None
            break

    return dest, steps

@cache
def can_move_out_of_room(room, state):
    steps = 0

    for pos in TARGETS[room]:
        item = state[pos - 11]
        steps += 1

        if item == ".":
            continue

        targets = TARGETS[item]
        if pos in targets:
            correct = True
            ix = targets.index(pos)
            for other in targets[ix + 1:]:
                if other != item:
                    correct = False
                    break

            if correct:
                continue

        return pos, steps

    return None, steps

def get_moves(state):
    moves = list()

    # First try to move from the hallway into the rooms
    # Can we move from the hallway into the target?
    positions_hallway = [pos for pos in HALLWAY if state[pos] != "."]

    for pos in positions_hallway:
        item = state[pos]
        energy = ENERGIES[item]

        target, steps = can_move_into_target(item, state[11:])

        if target is not None and can_move(pos, ROOMS[item], state):
            cost = (steps + abs(ROOMS[item] - pos)) * energy
            # print(f"{item} at {pos} can move into target at {target} cost {cost}")
            # moves.append((pos, target, cost))
            yield pos, target, cost

    # Can we move out?
    for room in ROOMS.keys():

        source, steps = can_move_out_of_room(room, state[11:])

        if source is None:
            continue

        item = state[source]

        energy = ENERGIES[item]

        # Moves into the hallway
        for pos in HALLWAY:
            if can_move(ROOMS[room], pos, state):
                cost = (abs(ROOMS[room] - pos) + steps) * energy
                # print(f"{item} at {source} can move out to {pos} cost {cost}")
                # moves.append((source, pos, cost))
                yield source, pos, cost

        target, nsteps = can_move_into_target(item, state[11:])

        if target is not None and can_move(ROOMS[room], ROOMS[item], state):
            cost = (abs(ROOMS[room] - ROOMS[item]) + steps + nsteps) * energy
            # print(f"{item} at {source} can move into target at {target} cost {cost}")
            # moves.append((source, target, cost))
            yield source, target, cost

def find_solution(initial_state, final_state):
    q = []
    heappush(q, (0, initial_state))

    hist = {initial_state: 0}
    best = 100_000_000

    k = 0
    while len(q) > 0:
        if k % 100_000 == 0:
            print(k, len(q), len(hist), best)
        k += 1

        energy, state = heappop(q)

        if state == final_state:
            best = min(best, energy)

        for s, e, cost in get_moves(state):
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

tmp = """#############
#.B.........#
###A#.#C#D###
  #A#B#C#D#  
  #########"""

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        initial_state = "".join([c for c in f.read() if c in "ABCD."])

    # initial_state = "".join([c for c in SAMPLE if c in "ABCD."])
    print_map(initial_state)

    final_state = "." * 11 + "ABCDABCD"

    bigger_initial_state = initial_state[:15] + "DCBADBAC" + initial_state[15:]
    print_map(bigger_initial_state)

    bigger_final_state = "." * 11 + "ABCDABCDABCDABCD"
