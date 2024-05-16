from pwn import *
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad
from os import urandom
import json
import socket
import threading

f = connect("103.163.24.78", 2003, level = 'debug')

f.recvuntil(b">")
f.sendline(str(2).encode())
f.recvuntil(b'Username: ')
f.sendline(b'\x00\x00{"username":           "admin", "isAdmin": true}')
f.recvuntil(b"You can use this token to access your account : ")
a = (f.recvline())
print(a)
b = a[32:128]


f.recvuntil(b">")
f.sendline(str(2).encode())
f.recvuntil(b'Username: ')
f.sendline(b"\x00\x00\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10")
f.recvuntil(b"You can use this token to access your account : ")
a = (f.recvline())
print(a)
c = a[32:64]

f.recvuntil(b">")
f.sendline(str(1).encode())
f.recvuntil(b'Token: ')
f.sendline(b+c)
f.recvline()

# f.recvuntil(b">")
# f.sendline(str(2).encode())
# f.recvuntil(b'Username: ')
# f.sendline(b'{"username":           "admin", "isAdmin": true}')
# f.recvuntil(b"You can use this token to access your account : ")
# a = (f.recvline())
# print(a)
# # tff= a[64:]
# # print(f"{tff = }")

# f.recvuntil(b">")
# f.sendline(str(1).encode())
# f.recvuntil(b'Token: ')
# f.sendline(a)
# f.recvline()


# f.sendlineafter(">", 1)
# f.recvuntil(b"Token: ")
# f.recvuntil(b">")
# f.sendline(str(2).encode())
# f.recvuntil(b'Username: ')
# # f.sendline(json.dumps({"username": "admin", "isAdmin": True}))

# f.sendline(pad(b" admin", 16))
# f.recvline()