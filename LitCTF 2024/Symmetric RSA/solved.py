from Crypto.Util.number import *
from pwn import *

f = remote('litctf.org', 31783, level = 'debug')
C = int(f.recvline()[5:].decode())
print(C)

f.sendlineafter(b':', b'2')
C2 = int(f.recvline(b'')[6:].decode())
f.recvuntil(b'')

f.sendlineafter(b':', b'3')
C3 = int(f.recvline(b'')[6:].decode())
f.recvuntil(b'')

f.sendlineafter(b':', b'4')
C4 = int(f.recvline(b'')[6:].decode())
f.recvuntil(b'')

f.sendlineafter(b':', b'6')
C6 = int(f.recvline(b'')[6:].decode())

a= C2 * C2 - C4
b= C2 * C3- C6
N = GCD(a, b)
p = GCD(N, C2 - 2)
print("Flag: ",long_to_bytes(C % p))
