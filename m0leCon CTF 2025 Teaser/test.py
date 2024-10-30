# import hashlib
# from Crypto.PublicKey.ECC import EccPoint
# from functools import reduce
# from pwn import remote, process, context
# from tqdm import tqdm, trange
# import itertools
# import json
# import operator
# from random import randint

# context.log_level = "CRITICAL"

# p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
# Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
# Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
# q = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
# G = EccPoint(Gx, Gy)

# N = 32
# T = 64
# B = 4
# BOUND = N * T * B

# def action(pub, priv, bases):
#     res = 1
#     for li, ei in zip(bases, priv):
#         res = (res * pow(li, ei, q)) % q
#     Q = res * pub
#     return Q

# def sub(a, b):
#     return [x - y for x, y in zip(a, b)]

# def sign(msg, sk, bases):
#     fs = []
#     Ps = []
#     cnt = 0
#     while cnt < T:
#         f = [
#             randint(-(N * T + 1) * B, (N * T + 1) * B) for _ in range(N)
#         ]
#         b = sub(f, sk)
#         if all(-N * T * B <= bb <= N * T * B for bb in b):
#             P = action(G, f, bases)
#             fs.append(f)
#             Ps.append((P.x, P.y))
#             cnt += 1
#     # h = SHA256(Ps || msg)
#     s = ",".join(map(str, Ps)) + "," + msg
#     h = int.from_bytes(hashlib.sha256(s.encode()).digest(), "big")
#     outs = []
#     for i in range(T):
#         b = (h >> i) & 1
#         if b:
#             outs.append((b, sub(fs[i], sk)))
#         else:
#             outs.append((b, fs[i]))
#     return outs

# # with process(["python3", "server.py"]) as io:
# with remote("ecsign.challs.m0lecon.it", 6482) as io:
#     io.recvuntil(b"messages!\n")
#     bases = eval(io.recvline().decode().strip())
#     assert isinstance(bases, list)

#     pk = tuple(map(int, io.recvline().decode().strip().split()))

#     TIMES = 1000
#     for _ in range(TIMES):
#         io.sendline(b"1")
#         io.sendline(b"aaaa")

#     print("\x1b[32mReceiving signatures\x1b[0m")
#     # sigs = []
#     ranges = [(0, 0) for _ in range(N)]
#     bar = trange(TIMES)
#     for _ in bar:
#         io.recvuntil(b"to sign: ")
#         outs = json.loads(io.recvline().decode().strip())
#         assert len(outs) == T
#         for bit, sig in outs:
#             # if bit == 0:
#             #     sigs.append(sig)
#             if bit == 1:
#                 continue
#             for i, s in enumerate(sig):
#                 ranges[i] = (min(ranges[i][0], s), max(ranges[i][1], s))
#         if _ % 20 == 0:
#             diff = [2 * BOUND - (y - x) + 1 for x, y in ranges]
#             combs = reduce(operator.mul, diff)
#             bar.set_description(str(combs))
#             if combs <= 20000:
#                 break

#     # for i in range(N):
#     #     min_i = min(sig[i] for sig in sigs)
#     #     max_i = max(sig[i] for sig in sigs)
#     #     ranges.append((min_i, max_i))

#     diff = [2 * BOUND - (y - x) + 1 for x, y in ranges]
#     print(f"\x1b[35mdiff: {diff}\x1b[0m")

#     combs = reduce(operator.mul, diff)
#     print(f"\x1b[36mcombs: {combs}\x1b[0m")
#     if combs > 20000:
#         raise RuntimeError("too many remaining combinations")

#     ranges_ = [[(t, t + 2 * BOUND) for t in range(y - 2 * BOUND, x + 1)] for x, y in ranges]
#     for u in tqdm(itertools.product(*ranges_), total=combs):
#         assert all(y - x == 2 * BOUND for x, y in u)
#         mid = [(x + y) // 2 for x, y in u]
#         mul = action(G, mid, bases)
#         if (mul.x, mul.y) == pk:
#             print("oh nice", mid)
#             break
#     else:
#         raise RuntimeError("bug")

#     io.sendline(b"2")
#     io.recvuntil(b"Give me a valid signature: ")
#     sig = sign("gimmetheflag", mid, bases)
#     # print("sig:", sig)
#     io.sendline(json.dumps(sig).encode())

#     FLAG = io.recvline().decode().strip()
#     print("FLAG:", FLAG)

# """
# base: B
# priv: e
# action: [B^e]pub

# sk: -4 to 4 integer
# pk: [B^sk]G

# sign:
#     fs <- []
#     Ps <- []
#     repeat successfully 64 times:
#         f <- [-260, 260]
#         f' <- f - sk
#         if f' in [-256, 256]:
#             fs.append(f)
#             Ps.append([B^f]G)
#     h <- SHA256(Ps || msg)
#     outs <- [fs[i] - sk * bit for bit in h]
#     return h, outs
# """


import os
import itertools
from tqdm import tqdm
from random import randrange
from collections import Counter
from chall import *
from pwn import context, remote, process
import multiprocessing as mp

context.log_level = "CRITICAL"


def bruteforce(base, rc):
    first = []
    for i in range(p):
        base[13] = i
        tmps, _ = absorb(base, rc, 13 + 32 * 3 + 1)
        key = tuple(tmps[13:ROUNDS:32])
        assert len(key) == 4
        first.append(key)

    key, cnt = Counter(first).most_common(1)[0]
    if cnt > 1:
        idx = [j for j in range(p) if first[j] == key]
        return idx


def parallel_bruteforce(rc):
    base = [randrange(p) for _ in range(16)] + [0] * 16
    return base, bruteforce(base, rc)


def find(rc):
    it = 0
    with mp.Pool(os.cpu_count()) as pool:
        for result in pool.imap_unordered(parallel_bruteforce, itertools.repeat(rc)):
            it += 1
            base, idx = result
            if idx is not None:
                pool.terminate()
                print(f"\x1b[32mTook {it} iterations!\x1b[0m")
                return base, idx


def main():
    with remote("talor.challs.m0lecon.it", "9445") as io:
        for _ in range(10):
            io.recvuntil(b"rc = ")
            rc = eval(io.recvline().decode().strip())
            assert isinstance(rc, list) and isinstance(rc[0], int)

            base, idx = find(rc)
            assert len(idx) > 1 and base[16:] == [0] * 16

            i, j = idx[:2]
            base[13] = i
            state1 = list(base)[:16]
            base[13] = j
            state2 = list(base)[:16]

            sponge1 = sponge(state1, rc)
            sponge2 = sponge(state2, rc)
            assert all(sponge1[i] == sponge2[i] or i == 1 for i in range(12))

            state1.extend([
                0, 0 if sponge1[1] >= sponge2[1] else sponge2[1] - sponge1[1]
            ])
            state2.extend([
                0, 0 if sponge1[1] <= sponge2[1] else sponge1[1] - sponge2[1]
            ])

            # M1, M2
            io.sendlineafter(b"M1: ", bytes(state1).hex().encode())
            io.sendlineafter(b"M2: ", bytes(state2).hex().encode())

        FLAG = io.recvline().decode().strip()
        print(f"\x1b[36mFLAG: {FLAG}\x1b[0m")


if __name__ == "__main__":
    main()