from sage.all import *
from pwn import *

# f = process(["python3", "main.py"])
f = connect("tjc.tf", 31601, level = 'debug')

f.recvuntil(b"<Bobby> i'll give you the powerful numbers, ")
c = Integer(f.recvuntil(b' and ', drop=True).decode())
n = Integer(f.recvuntil(b'\n', drop=True).decode())
f.recvline()
f.recvline()
f.sendlineafter(b'<You>', b'yea')
f.recvuntil(b"<Bobby> i'll send coords\n")
dont_leak_this = Integer(f.recvline().replace(b'<Bobby> ',b'').strip().decode())
for sub in range(1, 2**20):
    if (n + sub**2 - dont_leak_this) % sub != 0: continue
    s = (n + sub**2 - dont_leak_this) // sub
    P = PolynomialRing(ZZ, 'x')
    x = P.gen()
    fx = x**2 - s*x + n
    roots = fx.roots()
    if len(roots) == 0: continue
    p, q = roots[0][0], roots[1][0]
    assert p * q == n
    d = pow(65537, -1, (p-1) * (q-1))
    print(f"{d = }")
    my_password = pow(c, d, n)
    f.recvline()
    f.recvline()
    f.sendlineafter(b"<You>", str(my_password).encode())
    f.recvline()
    f.recvline()
    print(f.recvline())
f.close()