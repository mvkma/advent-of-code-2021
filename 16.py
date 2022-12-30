from functools import reduce
from operator import mul

INPUT_FILE = "input_16"

SAMPLE1 = """D2FE28"""

SAMPLE2 = """38006F45291200"""

SAMPLE3 = """EE00D40C823060"""

SAMPLE4 = """8A004A801A8002F478"""

SAMPLE5 = """620080001611562C8802118E34"""

SAMPLE6 = """C0015000016115A2E0802F182340"""

SAMPLE7 = """A0016C880162017C3686B18A3D4780"""

SAMPLE8 = """C200B40A82"""

SAMPLE9 = """04005AC33890"""

SAMPLE10 = """880086C3E88112"""

SAMPLE11 = """CE00C43D881120"""

SAMPLE12 = """D8005AC2A8F0"""

SAMPLE13 = """F600BC2D8F"""

SAMPLE14 = """9C005AC2F8F0"""

SAMPLE15 = """9C0141080250320F1802104A08"""

def hex_to_bin(msg: str):
    binlist = []

    for c in msg:
        n = int(c, 16)
        b = [0] * 4
        for i in range(4):
            b[3 - i] = n % 2
            n = n >> 1

        binlist.extend(b)

    return binlist

def bin_to_dec(binlist: list):
    return sum(b * 2**n for n, b in enumerate(reversed(binlist)))

def parse(binlist: list, max_packets: int = None):
    packets = []
    pkg_done = len(binlist) > 5
    version = None
    typeid = None

    pos = 0
    while True:
        if pos >= len(binlist):
            break

        if max_packets is not None and len(packets) >= max_packets:
            break

        if pkg_done:
            version = bin_to_dec(binlist[pos : pos + 3])
            typeid = bin_to_dec(binlist[pos + 3 : pos + 6])

            pos += 6
            pkg_done = False
            continue

        if typeid == 4:
            done = False
            value = []

            while not done:
                done = not binlist[pos]
                value.extend(binlist[pos + 1 : pos + 5])
                pos += 5

            value = bin_to_dec(value)

            pkg_done = True
            packets.append((version, typeid, value))
            continue

        if typeid != 4:
            mode = binlist[pos]
            pos += 1

            if mode == 0:
                length = bin_to_dec(binlist[pos : pos + 15])
                pos += 15

                subs, n = parse(binlist[pos : pos + length])
                pos += length

            if mode == 1:
                npackets = bin_to_dec(binlist[pos : pos + 11])
                pos += 11

                subs, n = parse(binlist[pos:], max_packets=npackets)
                pos += n

            pkg_done = True
            packets.append((version, typeid, subs))
            continue

        break

    return packets, min(pos, len(binlist))

def version_sum(msg):
    s = 0

    for version, typeid, value in msg:
        s += version
        if typeid != 4:
            s += version_sum(value)

    return s

def evaluate(msg):
    version, typeid, value = msg
    match typeid:
        case 0:
            return sum(evaluate(v) for v in value)
        case 1:
            return reduce(mul, (evaluate(v) for v in value))
        case 2:
            return min(evaluate(v) for v in value)
        case 3:
            return max(evaluate(v) for v in value)
        case 4:
            return value
        case 5:
            return int(evaluate(value[0]) > evaluate(value[1]))
        case 6:
            return int(evaluate(value[0]) < evaluate(value[1]))
        case 7:
            return int(evaluate(value[0]) == evaluate(value[1]))
        case _:
            raise ValueError(f"Unknown typeid: {typeid}")

if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        msg = f.readline().strip()

    parsed_msg, length = parse(hex_to_bin(msg))

    print(version_sum(parsed_msg))

    print(evaluate(parsed_msg[0]))
