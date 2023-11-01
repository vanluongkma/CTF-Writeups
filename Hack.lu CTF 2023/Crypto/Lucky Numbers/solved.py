from pwn import *
from math import *


f = connect("flu.xxx", 10010)
def nt(n):
    if n < 2:
        return False
    for i in range(2, isqrt(n) + 1):
        if n % i == 0:
            return False
    return True

for i in range(42):
	if nt(2**i - 1) & nt(i):
		t = i
		s = (2**(t-1))*(2**(t)-1)
		if 20000 <= s <= 150000000000:
			break

f.sendlineafter(b'You know the moment when you have this special number that gives you luck? Great cause I forgot mine\n', str(s).encode())
f.sendlineafter(b"I also had a second lucky number, but for some reason I don't remember it either :(\n", str(t).encode())

f.recvline()
