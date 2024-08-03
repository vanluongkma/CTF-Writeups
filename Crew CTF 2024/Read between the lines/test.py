#!/usr/bin/env python3

from random import shuffle
from Crypto.Util.number import getPrime

FLAG = b"123456789"

assert len(FLAG) < 100

encoded_flag = []

for i, b in enumerate(FLAG):
    encoded_flag.extend([i + 0x1337] * b)

shuffle(encoded_flag)

e = 65537
p, q = getPrime(1024), getPrime(1024)
n = p * q
c = sum(pow(m, e, n) for m in encoded_flag) % n


print(encoded_flag)
print(n, e, c)
