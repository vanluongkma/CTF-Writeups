from pwn import *
from z3 import *

f = connect("00.cr.yp.toc.tf", 17113)
context.log_level = "DEBUG"


while True:
    res = f.recvuntil(b'f(1, 1) = ').decode()
    print(res)
    res += f.recvuntil(b' and f(x, y) = ').decode()
    f11 = int(res.split('f(1, 1) = ')[1].split(' ')[0])
    print(f"[+] f(1, 1) = {f11}")
    fxy = int(f.recvline().strip().decode())
    print(f"[+] f(x, y) = {fxy}")

    def find_xy(n):
        solutions = []
        for a in range(1, int(2*n**0.5) + 1):
            if (2*n) % a == 0:
                b = (2*n) // a
                if (a + b + 1) % 2 == 0 and (b - a + 1) % 2 == 0:
                    x = (a + b + 1) // 2
                    y = (b - a + 1) // 2
                    if x >= 1 and y >= 1:
                        solutions.append((x, y))
                        break
        return solutions

    result = find_xy(fxy - f11)
    if result:
        print(f"[Y] Found solutions: {result}")
    else:
        print("[N] No solution found.")

    for x, y in result:
        f.sendline(f"{x},{y}")
        break
    print(f"[+] Sent: {x},{y}")