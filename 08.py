from collections import defaultdict

INPUT_FILE = "input_08"

SAMPLE = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

SAMPLE2 = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""

segment_counts = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}

def decode(signal_patterns):
    patterns_by_length = defaultdict(list)

    for pattern in signal_patterns:
        patterns_by_length[len(pattern)].append(set(pattern))

    patterns_by_digit = dict()
    patterns_by_digit[1] = patterns_by_length[2][0]
    patterns_by_digit[4] = patterns_by_length[4][0]
    patterns_by_digit[7] = patterns_by_length[3][0]
    patterns_by_digit[8] = patterns_by_length[7][0]

    for pat in patterns_by_length[5]:
        if len(pat.intersection(patterns_by_digit[7])) == 3:
            patterns_by_digit[3] = pat
        elif len(pat.intersection(patterns_by_digit[4])) == 3:
            patterns_by_digit[5] = pat
        else:
            patterns_by_digit[2] = pat

    for pat in patterns_by_length[6]:
        if len(pat.intersection(patterns_by_digit[4])) == 4:
            patterns_by_digit[9] = pat
        elif len(pat.intersection(patterns_by_digit[5])) == 5:
            patterns_by_digit[6] = pat
        else:
            patterns_by_digit[0] = pat

    mapping = {"".join(sorted(v)): k for k, v in patterns_by_digit.items()}

    return mapping

if __name__ == "__main__":
    signal_patterns = []
    output_values = []

    with open(INPUT_FILE) as f:
        for line in f:
        # for line in SAMPLE.splitlines():
        # for line in SAMPLE2.splitlines():
            line = line.strip()
            signal_part, output_part = line.split("|")

            signal_patterns.append(signal_part.strip().split())
            output_values.append(output_part.strip().split())

    # Part 1
    res = sum(sum(len(v) in (2, 3, 4, 7) for v in output) for output in output_values)
    print(res)

    # Part 2
    res = 0
    for signal, output in zip(signal_patterns, output_values):
        mapping = decode(signal)
        nums = [mapping["".join(sorted(out))] for out in output]
        res += int("".join(str(n) for n in nums))

    print(res)

