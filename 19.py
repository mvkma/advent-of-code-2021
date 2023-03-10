from itertools import combinations

INPUT_FILE = "input_19"

SAMPLE = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""

ORIENTATIONS = [
    [[ 1,  0,  0], [ 0,  1,  0], [ 0,  0,  1]],
    [[-1,  0,  0], [ 0, -1,  0], [ 0,  0,  1]],
    [[ 0,  1,  0], [-1,  0,  0], [ 0,  0,  1]],
    [[ 0, -1,  0], [ 1,  0,  0], [ 0,  0,  1]],
    [[ 1,  0,  0], [ 0, -1,  0], [ 0,  0, -1]],
    [[-1,  0,  0], [ 0,  1,  0], [ 0,  0, -1]],
    [[ 0,  1,  0], [ 1,  0,  0], [ 0,  0, -1]],
    [[ 0, -1,  0], [-1,  0,  0], [ 0,  0, -1]],
    [[ 1,  0,  0], [ 0,  0, -1], [ 0,  1,  0]],
    [[-1,  0,  0], [ 0,  0,  1], [ 0,  1,  0]],
    [[ 0,  0,  1], [ 1,  0,  0], [ 0,  1,  0]],
    [[ 0,  0, -1], [-1,  0,  0], [ 0,  1,  0]],
    [[ 1,  0,  0], [ 0,  0,  1], [ 0, -1,  0]],
    [[-1,  0,  0], [ 0,  0, -1], [ 0, -1,  0]],
    [[ 0,  0,  1], [-1,  0,  0], [ 0, -1,  0]],
    [[ 0,  0, -1], [ 1,  0,  0], [ 0, -1,  0]],
    [[ 0,  1,  0], [ 0,  0,  1], [ 1,  0,  0]],
    [[ 0, -1,  0], [ 0,  0, -1], [ 1,  0,  0]],
    [[ 0,  0,  1], [ 0, -1,  0], [ 1,  0,  0]],
    [[ 0,  0, -1], [ 0,  1,  0], [ 1,  0,  0]],
    [[ 0,  1,  0], [ 0,  0, -1], [-1,  0,  0]],
    [[ 0, -1,  0], [ 0,  0,  1], [-1,  0,  0]],
    [[ 0,  0,  1], [ 0,  1,  0], [-1,  0,  0]],
    [[ 0,  0, -1], [ 0, -1,  0], [-1,  0,  0]],
]

class Vec():
    def __init__(self, *data):
        self.data = tuple(data)

    def __hash__(self):
        return hash(self.data)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, i):
        return self.data[i]

    def __repr__(self):
        return f"V{repr(self.data)}"

    def __add__(self, other):
        return Vec(*[s + t for s, t in zip(self, other)])

    def __sub__(self, other):
        return Vec(*[s - t for s, t in zip(self, other)])

    def __eq__(self, other):
        return all(s == t for s, t in zip(self, other))

    def __lt__(self, other):
        return self.data < other.data

    def __mul__(self, a):
        return Vec(*[a * s for s in self])

    def norm(self):
        return sum(a**2 for a in self.data)

    def rotate(self, matrix):
        nrows = len(matrix)
        ncols = len(matrix[0])

        return Vec(*[sum(matrix[i][j] * self[j] for j in range(ncols)) for i in range(nrows)])

def transpose(matrix):
    nrows = len(matrix)
    ncols = len(matrix[0])

    new_matrix = [[0] * nrows for _ in range(ncols)]
    for i in range(nrows):
        for j in range(ncols):
            new_matrix[j][i] = matrix[i][j]

    return new_matrix

def matmul(mat1, mat2):
    nrows1 = len(mat1)
    ncols1 = len(mat1[0])

    nrows2 = len(mat2)
    ncols2 = len(mat2[0])

    assert nrows1 == ncols2

    new_mat = [[0] * ncols2 for _ in range(nrows1)]
    for j in range(nrows1):
        for i in range(ncols2):
            new_mat[j][i] = sum(mat1[j][k] * mat2[k][i] for k in range(nrows1))

    return new_mat

def get_overlap(scanners, i, j):
    shared_distances = scanners[i]["distances"].intersection(scanners[j]["distances"])

    shared_beacons = set()
    for d in shared_distances:
        shared_beacons.update(scanners[i]["distance_map"][d])

    return shared_beacons

def match_beacons(scanners, i, j):
    shared_distances = scanners[i]["distances"].intersection(scanners[j]["distances"])

    beacon_map = {k: get_overlap(scanners, j, i) for k in get_overlap(scanners, i, j)}

    for d in shared_distances:
        b1, b2 = scanners[i]["distance_map"][d]
        other_beacons = set(scanners[j]["distance_map"][d])
        beacon_map[b1] = beacon_map[b1].intersection(other_beacons)
        beacon_map[b2] = beacon_map[b2].intersection(other_beacons)

    new_beacon_map = dict()
    for k, v in beacon_map.items():
        if len(v) > 1:
            continue
        new_beacon_map[k] = list(v)[0]

    return new_beacon_map

def get_relative_position(beacon_map):
    if len(beacon_map) < 12:
        raise ValueError(f"Beacon map only has {len(beacon_map)} entries")

    for s in (-1, +1):
        for mat in ORIENTATIONS:
            ds = {k + v.rotate(mat) * s for k, v in beacon_map.items()}
            if len(ds) == 1:
                break

        if len(ds) == 1:
            break

    assert len(ds) == 1

    rel = ds.pop()
    mat = [[-s * n for n in row] for row in mat]

    return rel, mat

if __name__ == "__main__":
    scanners = []

    with open(INPUT_FILE) as f:
        for line in f:
        # for line in SAMPLE.splitlines():
            line = line.strip()

            if line == "":
                continue

            if line.startswith("---"):
                scanner = {
                    "beacons": [],
                    "orientation": None,
                    "location": None,
                    "distances": set(),
                    "distance_map": dict(),
                }
                scanners.append(scanner)
                continue

            x1, x2, x3 = map(int, line.split(","))
            scanner["beacons"].append(Vec(x1, x2, x3))

    for s in scanners:
        for p1, p2 in combinations(s["beacons"], 2):
            dist = (p1 - p2).norm()
            s["distances"].add(dist)
            s["distance_map"][dist] = (p1, p2)

    scanners[0]["location"] = Vec(0, 0, 0)
    scanners[0]["orientation"] = ORIENTATIONS[0]

    # Determine the relative positions between pairs or scanners
    rpos = dict()
    for i, j in combinations(range(len(scanners)), 2):
        beacon_map = match_beacons(scanners, i, j)

        if len(beacon_map) < 12:
            continue

        pos, rot = get_relative_position(beacon_map)

        rpos[(i, j)] = (pos, rot)

    # Compute positions relative to the origin (scanner 0)
    while any(s["location"] is None for s in scanners):
        for i, j in combinations(range(len(scanners)), 2):
            if (i, j) not in rpos:
                continue

            pos, rot = rpos[(i, j)]

            if scanners[i]["location"] is not None:
                scanners[j]["location"] = scanners[i]["location"] + pos.rotate(scanners[i]["orientation"])
                scanners[j]["orientation"] = matmul(scanners[i]["orientation"], rot)
            elif scanners[j]["location"] is not None:
                scanners[i]["orientation"] = matmul(scanners[j]["orientation"], transpose(rot))
                scanners[i]["location"] = scanners[j]["location"] - pos.rotate(scanners[i]["orientation"])
            else:
                continue

    # Part 1
    all_beacons = set()
    for s in scanners:
        all_beacons.update([s["location"] + b.rotate(s["orientation"]) for b in s["beacons"]])

    print(len(all_beacons))

    # Part 2
    max_dist = 0
    for s1, s2 in combinations(scanners, 2):
        d = sum(abs(n) for n in (s1["location"] - s2["location"]))
        max_dist = max(d, max_dist)

    print(max_dist)

