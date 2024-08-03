from Crypto.Util.number import *
from binascii import crc32
from pwn import process, xor

f = process(["python3", "server.py"])
f.recvuntil(b"> ")
f.sendline("E")
f.sendlineafter(b"Your command: ", b"kma")
f.recvuntil(b"Your encrypted packet is: ")
encrypted =bytes.fromhex(f.recvline().decode())
nonce = encrypted[:8]
checksum = encrypted[8:12]
ciphertext = encrypted[12:]

check = b'{"user": "user", "command": "kma", "nonce": "trh65hrstbsf"}'
keystream = xor(check[:35],ciphertext[:35])
check = b'{"user": "root", "command": "flag"}'
new_ciphertext = xor(keystream,check)

checksum = long_to_bytes(crc32(check))
nonce = nonce
check_flag = ((nonce + checksum + new_ciphertext).hex())

f.sendlineafter(b"> ", b'R')
f.sendline(check_flag)
f.recvline()