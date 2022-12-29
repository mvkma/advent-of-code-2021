INPUT_FILE = "input_10"

SAMPLE = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

OPENING = ("(", "[", "{", "<")
CLOSING = (")", "]", "}", ">")

BRACKETS = {
    "(": 0, ")": 0,
    "[": 1, "]": 1,
    "{": 2, "}": 2,
    "<": 3, ">": 3,
}

POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

def check_line(line):
    stack = []

    for c in line:
        if c in OPENING:
            stack.append(BRACKETS[c])
            continue

        if c in CLOSING:
            if not BRACKETS[c] == stack.pop():
                return False, c

    return True, ""

def complete_line(line):
    stack = []

    for c in line:
        if c in OPENING:
            stack.append(BRACKETS[c])
            continue

        if c in CLOSING:
            stack.pop()

    rest = "".join(CLOSING[c] for c in reversed(stack))

    return rest

if __name__ == "__main__":
    lines = []

    with open(INPUT_FILE) as f:
        # for line in SAMPLE.splitlines():
        for line in f:
            line = line.strip()
            lines.append(line)

    incomplete_lines = []

    score = 0
    for line in lines:
        okay, c = check_line(line)
        if not okay:
            score += POINTS[c]
        else:
            incomplete_lines.append(line)

    print(score)

    scores = []

    for line in incomplete_lines:
        rest = complete_line(line)
        score = 0
        for c in rest:
            score *= 5
            score += CLOSING.index(c) + 1

        scores.append(score)

    print(sorted(scores)[len(scores) // 2])
