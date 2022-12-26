INPUT_FILE = "input_03"

SAMPLE = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

def most_common_bits(nums, nbits):
    bits = [0] * nbits

    bits = [0] * nbits
    for num in nums:
        num = num % 2**nbits
        for i in range(nbits - 1, -1, -1):
            bits[i] += num // 2**i
            num = num % (2**i)

    nn = len(nums)
    if nn % 2 == 0:
        return [int(b >= len(nums) // 2) for b in reversed(bits)]
    else:
        return [int(b > len(nums) // 2) for b in reversed(bits)]

if __name__ == "__main__":
    nums = []
    nbits = 0

    with open(INPUT_FILE) as f:
        # for line in SAMPLE.splitlines():
        for line in f:
            line = line.strip()
            nbits = max(nbits, len(line))
            nums.append(int(line, 2))

    gamma = sum(b * 2**i for i, b in enumerate(reversed(most_common_bits(nums, nbits))))
    epsilon = (2**nbits - 1) ^ gamma

    print(gamma * epsilon)

    oxygen_nums = nums.copy()
    n = nbits

    while len(oxygen_nums) > 1:
        bits = most_common_bits(oxygen_nums, n)
        tmp = []
        for num in oxygen_nums:
            a = num
            for k in range(nbits, n - 1, -1):
                a = a % (2**k)
            if a // 2**(n - 1) == bits[0]:
                tmp.append(num)

        oxygen_nums = tmp
        n -= 1

    co2_nums = nums.copy()
    n = nbits

    while len(co2_nums) > 1:
        bits = [int(not(b)) for b in most_common_bits(co2_nums, n)]
        tmp = []
        for num in co2_nums:
            a = num
            for k in range(nbits, n - 1, -1):
                a = a % (2**k)
            if a // 2**(n - 1) == bits[0]:
                tmp.append(num)

        co2_nums = tmp
        n -= 1

    print(co2_nums[0] * oxygen_nums[0])
