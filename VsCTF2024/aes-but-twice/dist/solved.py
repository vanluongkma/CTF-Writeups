import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter
from pwn import*

f = remote("vsc.tf", 5000, level = 'debug')
ctf_flag = bytes.fromhex(f.recvline().decode())
cbc_flag = bytes.fromhex(f.recvline().decode())
nonce = bytes.fromhex(f.recvline().decode())


f.sendline((xor(cbc_flag[-16:],nonce + b'\x00\x00\x00\x00\x00\x00\x00\x00').hex()).encode())
f.recvuntil(b'\n')
out1 = f.recvuntil(b'\n',drop=True).decode()
out1 = bytes.fromhex(out1)
a = (xor(out1[:16],ctf_flag[:16]))

f.sendline((xor(out1[16:32],nonce + b'\x00\x00\x00\x00\x00\x00\x00\x01').hex()).encode())
f.recvuntil(b'\n')
out2 = f.recvuntil(b'\n',drop=True).decode()
out2 = bytes.fromhex(out2)
b = (xor(out2[:16],ctf_flag[16:32]))

f.sendline((xor(out2[-16:],nonce + b'\x00\x00\x00\x00\x00\x00\x00\x02').hex()).encode())
f.recvuntil(b'\n')
out3 = f.recvuntil(b'\n',drop=True).decode()
out3 = bytes.fromhex(out3)
c = unpad(xor(out3[:16],ctf_flag[32:48]), 16)

print(f"flag : {a + b + c}")