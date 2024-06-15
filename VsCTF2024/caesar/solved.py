import random

random.seed(1337)
ops = [
    lambda x: x + 3,
    lambda x: x - 3,
    lambda x: x * 3,
    lambda x: x ^ 3,
]

encoded = [354, 112, 297, 119, 306, 369, 111, 108, 333, 110, 112, 92, 111, 315, 104, 102, 285, 102, 303, 100, 112, 94, 111, 285, 97, 351, 113, 98, 108, 118, 109, 119, 98, 94, 51, 56, 159, 50, 53, 153, 100, 144, 98, 51, 53, 303, 99, 52, 49, 128]

reverse_ops = {
    ops[0]: lambda x: x - 3,
    ops[1]: lambda x: x + 3,
    ops[2]: lambda x: x // 3,
    ops[3]: lambda x: x ^ 3,
}

decoded = []
for v in encoded:
    op = random.choice(ops)
    decoded.append(reverse_ops[op](v))

flag = bytes(decoded)
print(flag.decode())