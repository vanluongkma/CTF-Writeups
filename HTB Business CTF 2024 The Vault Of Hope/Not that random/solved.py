from Crypto.Util.number import *
from pwn import *
from tqdm import tqdm
from hashlib import *

# f = connect("83.136.248.97", 35702, level = 'debug')
f = process(["python3", "server.py"])

f.recvline()
f.sendlineafter(b"Option: ", b"2")
f.recvuntil(b"Enter your input in hex :: ")
f.sendline((b"Improving on the security of SHA is easy").hex())
f.recvuntil(b"Your output is :: ")

hash_key = bytes.fromhex(f.recvline()[:-1].decode()[-64:])
print(hash)

def keyed_hash(key, inp):
    return sha256(key + inp).digest()

for i in tqdm(range(100)):
    f.sendlineafter(b"Option: ", b"3")
    f.recvuntil(b"I used input ")
    inp = bytes.fromhex(f.recvline()[:-1].decode())
    f.recvuntil(b"I got output ")
    out = bytes.fromhex(f.recvline()[:-1].decode())
    if out.startswith(keyed_hash(hash_key, inp)):
        f.sendlineafter(b":: ", str(0).encode())
    else:
        f.sendlineafter(b":: ", str(1).encode())

f.sendlineafter(b"Option: ", b"4")
f.sendlineafter(b"Option: ", b"1")
f.interactive()
