from pwn import *
from json import loads

HOST = '103.163.24.78'
PORT = 2003

r = remote('103.163.24.78', 2003, level = 'debug')
print(r.recv().decode())

user = 'XX{"username":           "admin", "isAdmin": true}'
add = (b'XX' + b'\x10' * 16).decode()

r.sendlineafter(b'> ', b'2')
r.sendlineafter(b'Username: ', user.encode())
r.recvuntil(b' : ')
token = bytes.fromhex(r.recvline().decode())[16:48+16]

r.sendlineafter(b'> ', b'2')
r.sendlineafter(b'Username: ', add.encode())
r.recvuntil(b' : ')
token_add = bytes.fromhex(r.recvline().decode())[16:32]

send = token + token_add
r.sendlineafter(b'> ', b'1')
r.sendlineafter(b'Token: ', bytes.hex(send).encode())
flag = r.recvline().decode()
print(flag)