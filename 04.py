INPUT_FILE = "input_04"

SAMPLE = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

class Bingo:
    def __init__(self, fields):
        self.nrows = len(fields)
        self.ncols = len(fields[0])

        self.has_won = False
        self.values = dict()
        self.positions = dict()
        self.marked = set()

        for j in range(self.nrows):
            for i in range(self.ncols):
                val = fields[j][i]
                self.values[val] = (i, j)
                self.positions[(i, j)] = val

    def __repr__(self):
        s = ""

        for j in range(self.nrows):
            for i in range(self.ncols):
                val = self.positions[(i, j)]
                if (i, j) in self.marked:
                    s += "\033[91m" + str(val).rjust(5) + "\033[0m"
                else:
                    s += str(val).rjust(5)
            s += "\n"

        return s

    def mark(self, val):
        if val in self.values:
            self.marked.add(self.values[val])

        for j in range(self.nrows):
            if all((i, j) in self.marked for i in range(self.ncols)):
                self.has_won = True
                break

        for i in range(self.ncols):
            if all((i, j) in self.marked for j in range(self.nrows)):
                self.has_won = True
                break

        return self.has_won

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        # f = iter(SAMPLE.splitlines())
        random_nums = list(map(int, next(f).strip().split(",")))
        next(f)

        boards = []

        rows = []
        for line in f:
            line = line.strip()
            if line == "":
                boards.append(Bingo(rows))
                rows = []
                continue

            rows.append([int(n) for n in line.split()])

        boards.append(Bingo(rows))

    scores = []
    for num in random_nums:
        for b in boards:
            if (not b.has_won) and b.mark(num):
                score = sum(val for pos, val in b.positions.items() if not pos in b.marked)
                scores.append(score * num)

    print(scores[0])
    print(scores[-1])

