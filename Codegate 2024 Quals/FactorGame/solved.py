from sage.all import *
from binteger import Bin
from sock import Sock
from pwn import *
from tqdm import tqdm
import time

known = 264
t = known + 4


@parallel(ncpus=8)
def try_sol(N, lo, epsilon):
    R, x = Zmod(N)['x'].objgen()
    beta = 0.5000001
    X = 2**(512 - t)
    # epsilon = RR(beta**2 - log(2*X, N)) * 1.8
    # epsilon = 0.019

    poly = (x * 2**t + lo) / 2**t
    res = poly.small_roots(X=X, beta=beta, epsilon=epsilon)
    if res:
        x = int(res[0])
        q = x * 2**t + lo
        return q


def try_solve(rnd, p_redacted, p_mask, q_redacted, q_mask, N):
    tt = max(Bin(p_mask).n, Bin(q_mask).n)
    print("bits", tt, "using", t)
    sols = {(0, 0)}
    for e in range(1, t+1):
        sols2 = set()
        bit = 2**(e-1)
        mask = 2**e - 1
        Nmask = N & mask
        for (p, q) in sols:
            for pbit in range(2):
                for qbit in range(2):
                    pp = p + bit * pbit
                    qq = q + bit * qbit
                    if (pp * qq) & mask != Nmask:
                        continue
                    if pp & p_mask & mask != p_redacted & mask:
                        continue
                    if qq & q_mask & mask != q_redacted & mask:
                        continue
                    sols2.add((pp, qq))
        sols = sols2
        #assert (sol_p & mask, sol_q & mask) in sols, e
        if len(sols) >= 100_000:
            raise RuntimeError("too many sols mid %d" % len(sols))
    #assert sol_p & p_mask == p_redacted
    #assert sol_q & q_mask == q_redacted

    if rnd <= 1 and len(sols) > 16:
        raise RuntimeError("too many sols end %d for round 1" % len(sols))

    if len(sols) <= 32:
        epsilon = 0.018
    elif len(sols) <= 128:
        epsilon = 0.020
    else:
        raise RuntimeError("too many sols end %d" % len(sols))

    print("sols", len(sols), "eps", epsilon)

    todo = []
    for plo, qlo in sols:
        for lo in plo, qlo:
            todo.append((N, lo, epsilon))

    res = try_sol(todo)
    #print("res", res)
    for item in tqdm(res, total=len(todo)):
        q = item[-1]
        if q:
            print("got q", q)
            if N % q == 0:
                p = N // q
                return p, q
    raise RuntimeError("no sol found")


def one_round(f, rnd, att):
    print(repr(f.recvuntil("p : 0x")))
    p_red = int(f.recvline(), 16)

    f.recvuntil("p_mask : 0x")
    p_mask = int(f.recvline(), 16)

    f.recvuntil("q : 0x")
    q_red = int(f.recvline(), 16)

    f.recvuntil("q_mask : 0x")
    q_mask = int(f.recvline(), 16)

    f.recvuntil("N : 0x")
    N = int(f.recvline(), 16)

    try:
        p, q = try_solve(rnd, p_red, p_mask, q_red, q_mask, N)
        print("good")
        assert p * q == N
        print("N =", N)
        print("p =", p)
        print("q =", q)
        if p & p_mask != p_red:
            print("weird")
            p, q = q, p
            if p & p_mask != p_red:
                print("weird x2")
            else:
                print("fixed with swap!")
        assert p & p_mask == p_red
        assert q & q_mask == q_red
    except RuntimeError as err:
        print("fail at", rnd, att, err)
        p = q = 1

    f.recvuntil("format : ")
    f.sendline("%x" % p)
    f.recvuntil("format : ")
    f.sendline("%x" % q)
    print(repr(f.recvline()))
    return p > 1

def try_game():
    
    f = process(["python3", "FactorGame.py", "DEBUG"])
    n_fail = 0
    t0 = time.time()
    for rnd in range(1, 11):
        for att in range(5):
            print("game", itr, ":", "round", rnd, "attempt", att, "elapsed %.1fs" % (time.time() - t0), "fails", n_fail)
            try:
                if one_round(f, rnd, att):
                    break
            except EOFError:
                print(repr(f.buf))
                with open("flag", "a") as fd:
                    print(repr(f.buf), file=fd)
                quit()
            print()
        else:
            n_fail += 1
            if rnd <= 3:
                print("too bad")
                return
            if n_fail > 2:
                print("failed total")
                print()
                print()
                return

        print()
        print()
        print()

    res = f.recv()
    print(repr(res))
    with open("flag", "a") as fd:
        print(repr(res), file=fd)
    quit()


itr = 0
while True:
    itr += 1
    try_game()