from itertools import cycle, product
from functools import cache

INPUT_FILE = "input_21"

DICE_OUTCOMES = (
    (3, 1),
    (4, 3),
    (5, 6),
    (6, 7),
    (7, 6),
    (8, 3),
    (9, 1),
)

def mmod(m, n):
    if m % n == 0:
        return n
    else:
        return m % n

def play_round(pos_a, score_a, pos_b, score_b, dice, k):
    n1, n2, n3 = dice(), dice(), dice()
    k += 3

    pos_a = mmod(pos_a + n1 + n2 + n3, 10)
    score_a = score_a + pos_a

    return pos_a, score_a, pos_b, score_b, k

@cache
def num_wins(pos_a, score_a, pos_b, score_b):
    wins_a = 0
    wins_b = 0

    for n, mul in DICE_OUTCOMES:
        pos_a_new = mmod(pos_a + n, 10)
        score_a_new = score_a + pos_a_new

        if score_a_new >= 21:
            wins_a += mul
        else:
            wb, wa = num_wins(pos_b, score_b, pos_a_new, score_a_new)
            wins_a += wa * mul
            wins_b += wb * mul

    return wins_a, wins_b

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        initial_pos_a = int(next(f).strip()[-1])
        score_a = 0
        initial_pos_b = int(next(f).strip()[-1])
        score_b = 0

    # Part 1
    pos_a = initial_pos_a
    pos_b = initial_pos_b

    detdice = cycle(range(1, 101))
    dice = lambda: next(detdice)

    k = 0
    while True:
        pos_a, score_a, pos_b, score_b, k = play_round(pos_a, score_a, pos_b, score_b, dice, k)
        if score_a >= 1000:
            print(k * score_b)
            break

        pos_b, score_b, pos_a, score_a, k = play_round(pos_b, score_b, pos_a, score_a, dice, k)
        if score_b >= 1000:
            print(k * score_a)
            break

    # Part 2
    print(max(num_wins(initial_pos_a, 0, initial_pos_b, 0)))
