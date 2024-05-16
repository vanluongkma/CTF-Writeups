import secrets
from pwn import *
from randcrack import RandCrack
from Crypto.Util.number import *

rc = RandCrack()

f = remote('chal.osugaming.lol', 7275)
f.recvline()
cur = f.recvline().decode()
f.sendline(cur)
f.interactive()
# print(sh.recvuntil(b'solution: '))
# sh.sendline(input().encode())

# sh.recvuntil(b'n = ')
# n = int(sh.recvline().decode().strip())
# sh.recvuntil(b'vs = ')
# vs = [int(num) for num in sh.recvline().decode().strip()[1:-1].split(',')]

# for _ in range(624):
# 	r = secrets.randbelow(n)
# 	x = pow(r, 2, n)

# 	sh.recvuntil(b': ')
# 	sh.sendline(str(x).encode())
# 	sh.recvuntil(b': ')
# 	mask = int(sh.recvline().decode().strip(), 2)
# 	rc.submit(mask)
# 	sh.recvuntil(b': ')
# 	sh.sendline(str(x).encode())

# for _ in range(10):
# 	mask = '{:032b}'.format(rc.predict_getrandbits(32))
# 	#print('preddd', mask)
# 	y = secrets.randbelow(n)
# 	x = pow(y, 2, n)
# 	for i in range(32):
# 		if mask[i] == '1':
# 			x = (x * inverse(vs[i], n)) % n

# 	sh.recvuntil(b': ')
# 	sh.sendline(str(x).encode())
# 	sh.recvuntil(b': ')
# 	mask = sh.recvline().decode().strip()

# 	sh.recvuntil(b': ')
# 	sh.sendline(str(y).encode())
# sh.interactive()