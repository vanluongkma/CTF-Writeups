from pwn import *
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad
from os import urandom
import json
import socket
import threading

f = connect("103.163.24.78", 2003, level = 'debug')
# f = process(["python3", "server.py"])


f.recvuntil(b">")
f.sendline(str(2).encode())
f.recvuntil(b'Username: ')
f.sendline(b'ad000", "isAdmin": True""')
f.recvuntil(b"You can use this token to access your account : ")
a = (f.recvline())
print(a)
b = a[:32]
tf = a[64:]

# f.recvuntil(b">")
# f.sendline(str(2).encode())
# f.recvuntil(b'Username: ')
# f.sendline(b"00min")
# f.recvuntil(b"You can use this token to access your account : ")
# a = (f.recvline())
# print(a)
# c = a[32:64]

f.recvuntil(b">")
f.sendline(str(2).encode())
f.recvuntil(b'Username: ')
f.sendline(b'00min", "isAdmin": True""')
f.recvuntil(b"You can use this token to access your account : ")
a = (f.recvline())
print(a)
k = a[32:]

# f.recvuntil(b">")
# f.sendline(str(2).encode())
# f.recvuntil(b'Username: ')
# f.sendline(b'0000000000000000000000True')
# f.recvuntil(b"You can use this token to access your account : ")
# a = (f.recvline())
# print(a)
# tff = a[32:64]

f.recvuntil(b">")
f.sendline(str(1).encode())
f.recvuntil(b'Token: ')
f.sendline(b+k)
f.recvline()