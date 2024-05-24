from pwn import *
from hashlib import *
from Crypto.Util.number import *  
from tqdm import *

# s = connect("83.136.248.97", 43808)
s = process(["python3", "server.py"])
def keyed_hash(key: bytes, inp: bytes) -> bytes:
    return sha256(key + inp).digest()

def get() -> None:

    s.sendlineafter(b"Option: ", b"3")
    s.recvuntil(b"I used input ")
    inp = bytes.fromhex(s.recvline()[:-1].decode())
    s.recvuntil(b"I got output ")
    out = bytes.fromhex((s.recvline()[:-1]).decode())
    print(keyed_hash(hash, inp))
    print(out)
    if out.startswith(keyed_hash(hash, inp)):
        rand = 0
    else:
        rand = 1
    print(rand)
    s.sendlineafter(b":: ", str(rand).encode())

    return s.recvline()

s.recvline()
s.sendlineafter(b"Option: ", b"2")
s.sendlineafter(b"Enter your input in hex :: ", hex(bytes_to_long(b"Improving on the security of SHA is easy"))[2:].encode())
s.recvuntil(b":: ")

hash = bytes.fromhex(s.recvline()[:-1].decode()[-64:])

for i in tqdm(range(90)):
    print(get())

s.sendlineafter(b"Option: ", b"1")

print(s.recv())