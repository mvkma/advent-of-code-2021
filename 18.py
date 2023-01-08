from functools import reduce
from operator import add

INPUT_FILE = "input_18"

L1 = """[1,1]
[2,2]
[3,3]
[4,4]"""

L2 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]"""

L3 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]"""

L4 = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""

L5 = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

class SnailfishNumber:
    def __init__(self, left, right):
        self.left = left
        self.right = right

        if isinstance(left, SnailfishNumber) and isinstance(right, SnailfishNumber):
            self.left.parent = self
            self.right.parent = self
        elif isinstance(left, SnailfishNumber) and isinstance(right, int):
            self.left.parent = self
        elif isinstance(right, SnailfishNumber) and isinstance(left, int):
            self.right.parent = self

        self.parent = None

    def __repr__(self):
        return f"[{str(self.left)}, {str(self.right)}]"

    def __add__(self, other):
        if not isinstance(other, SnailfishNumber):
            raise ValueError(f"{other} is not a SnailfishNumber")

        return SnailfishNumber(self, other)

    @property
    def depth(self):
        left = self.left
        right = self.right

        if isinstance(left, SnailfishNumber) and isinstance(right, SnailfishNumber):
            return max(left.depth, right.depth) + 1
        elif isinstance(left, SnailfishNumber) and isinstance(right, int):
            return left.depth + 1
        elif isinstance(right, SnailfishNumber) and isinstance(left, int):
            return right.depth + 1
        else:
            return 1

    @classmethod
    def from_list(cls, lst):
        left, right = lst

        if isinstance(left, list):
            left = cls.from_list(left)

        if isinstance(right, list):
            right = cls.from_list(right)

        return cls(left, right)

    @property
    def is_explodable(self):
        if self.depth > 4:
            return True

        return False

    @property
    def is_splittable(self):
        if isinstance(self.left, SnailfishNumber):
            left = self.left.is_splittable
        else:
            left = self.left >= 10

        if isinstance(self.right, SnailfishNumber):
            right = self.right.is_splittable
        else:
            right = self.right >= 10

        return left or right

    def as_list(self):
        left = self.left
        if isinstance(self.left, SnailfishNumber):
            left = left.as_list()

        right = self.right
        if isinstance(self.right, SnailfishNumber):
            right = right.as_list()

        return [left, right]            

    def magnitude(self):
        left = self.left
        right = self.right

        if isinstance(left, SnailfishNumber) and isinstance(right, SnailfishNumber):
            return 3 * left.magnitude() + 2 * right.magnitude()
        elif isinstance(left, SnailfishNumber) and isinstance(right, int):
            return 3 * left.magnitude() + 2 * right
        elif isinstance(right, SnailfishNumber) and isinstance(left, int):
            return 3 * left + 2 * right.magnitude()
        else:
            return 3 * left + 2 * right

    def split(self):
        if not self.is_splittable:
            return self

        new = SnailfishNumber.from_list(self.as_list())

        cur = new
        while isinstance(cur, SnailfishNumber):
            if isinstance(cur.left, int) and cur.left >= 10:
                is_left = True
                break

            if isinstance(cur.left, SnailfishNumber) and cur.left.is_splittable:
                cur = cur.left
                continue

            if isinstance(cur.right, int) and cur.right >= 10:
                is_left = False
                break

            if isinstance(cur.right, SnailfishNumber) and cur.right.is_splittable:
                cur = cur.right
                continue

        if is_left:
            cur.left = SnailfishNumber(cur.left // 2, (cur.left + 1) // 2)
        else:
            cur.right = SnailfishNumber(cur.right // 2, (cur.right + 1) // 2)

        return new

    def explode(self):
        if not self.is_explodable:
            return self

        new = SnailfishNumber.from_list(self.as_list())

        d = new.depth
        s = new
        s_is_right = None
        while d > 1:

            if isinstance(s.right, int):
                s = s.left
                s_is_right = False
                d = d - 1
                continue

            if isinstance(s.left, int):
                s = s.right
                s_is_right = True
                d = d - 1
                continue

            if s.right.depth > s.left.depth:
                s = s.right
                s_is_right = True
                d = d - 1
            else:
                s = s.left
                s_is_right = False
                d = d - 1

        lval, lprev, lnew = None, None, None
        rval, rprev, rnew = None, None, None

        cur = s
        while cur.parent is not None:
            if lval is not None and rval is not None:
                break

            prev = cur.parent
            if prev.left is not cur and lval is None:
                lval = prev.left
                lprev = prev
                lval_is_left = True
                while not isinstance(lval, int):
                    lprev = lval
                    lval = lval.right
                    lval_is_left = False

            if prev.right is not cur and rval is None:
                rval = prev.right
                rprev = prev
                rval_is_right = True
                while not isinstance(rval, int):
                    rprev = rval
                    rval = rval.left
                    rval_is_right = False

            cur = prev

        if lprev is not None:
            if lval_is_left:
                lprev.left = lprev.left + s.left
            else:
                lprev.right = lprev.right + s.left

        if rprev is not None:
            if rval_is_right:
                rprev.right = rprev.right + s.right
            else:
                rprev.left = rprev.left + s.right

        if s_is_right:
            s.parent.right = 0
        else:
            s.parent.left = 0

        return new

    def reduce(self):
        num = self
        while True:
            if num.is_explodable:
                num = num.explode()
                continue

            if num.is_splittable:
                num = num.split()
                continue

            break

        return num


def snailfish_sum(numlist):
    num = numlist[0]
    num = num.reduce()

    for i in range(len(numlist) - 1):
        num = num + numlist[i + 1]
        num = num.reduce()

    return num

if __name__ == "__main__":
    S1 = SnailfishNumber.from_list([[[[[9,8],1],2],3],4])
    S2 = SnailfishNumber.from_list([7,[6,[5,[4,[3,2]]]]])
    S3 = SnailfishNumber.from_list([[6,[5,[4,[3,2]]]],1])
    S4 = SnailfishNumber.from_list([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
    S5 = SnailfishNumber.from_list([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])
    S6 = SnailfishNumber.from_list([[[[0,7],4],[15,[0,13]]],[1,1]])

    S7 = SnailfishNumber.from_list([[[[4,3],4],4],[7,[[8,4],9]]])
    S8 = SnailfishNumber.from_list([1,1])

    L1nums = [SnailfishNumber.from_list(eval(l.strip())) for l in L1.splitlines()]
    L2nums = [SnailfishNumber.from_list(eval(l.strip())) for l in L2.splitlines()]
    L3nums = [SnailfishNumber.from_list(eval(l.strip())) for l in L3.splitlines()]
    L4nums = [SnailfishNumber.from_list(eval(l.strip())) for l in L4.splitlines()]
    L5nums = [SnailfishNumber.from_list(eval(l.strip())) for l in L5.splitlines()]

    nums = []
    with open(INPUT_FILE) as f:
        for line in f:
            line = line.strip()
            nums.append(SnailfishNumber.from_list(eval(line)))

    # Part 1
    res = snailfish_sum(nums).magnitude()
    print(res)

    # Part 2
    best = 0
    for i in range(len(nums)):
        for j in range(len(nums)):
            res = (nums[i] + nums[j]).reduce().magnitude()
            best = max(best, res)

    print(best)
