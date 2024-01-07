from json import *
from binascii import *
from Crypto.Cipher import *
from Crypto.Random import *
from pwn import*

f = connect("integral-communication.chal.irisc.tf", 10103)
f.recvuntil(">")

guest = b'{"from": "guest"'
admin = b'{"from": "admin"'

echo = b', "act": "echo",'
flag = b', "act": "flag",'
#1
f.sendline(b"1")
f.recvuntil("message: ")
f.sendline(b"hello")
IV1 = bytes.fromhex(f.recvline().decode().replace("IV: ", ""))
f.recvline()
command1 = f.recvline().decode().replace("Command: ", "")
command000 = bytes.fromhex("00"*16 + command1[32:])

#2
f.sendlineafter(">", "2")
f.sendlineafter("IV:", IV1.hex())
f.sendlineafter('Command:', command000.hex())
ciphertext2 = bytes.fromhex(f.recvline().decode().replace("Failed to decode UTF-8: ", ""))

IV2 = xor(ciphertext2[16:32], flag).hex()

block1 = IV2 + command1[32:]
print(block1)

IV3 = "00" * 16
f.sendlineafter(">", "2")
f.sendlineafter("IV:", IV3)
f.sendlineafter('Command:', block1)


plain1= bytes.fromhex(f.recvline().decode().replace("Failed to decode UTF-8: ", ""))
IV4 = xor(admin, plain1[:16]).hex()

cmd = IV4 + command1[32:]
print(cmd)


f.sendlineafter(">", "2")
f.sendlineafter("IV:", IV4)
f.sendlineafter('Command:', block1)
f.recvline()
