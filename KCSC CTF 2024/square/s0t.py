from pwn import *
from tqdm import *
import os
from aeskeyschedule import *

f = remote("103.163.24.78", 2004)

def get_ciphertexts(index):
    origin = os.urandom(16)
    A_set = []
    for i in range(256):
        temp = bytearray(origin)
        temp[index] = i
        f.sendlineafter(b'> ', b'1')
        f.sendlineafter(b"Plaintext in hex: ", temp.hex().encode())
        ct = f.recvuntil(b'\n',drop=True).decode()
        A_set.append(bytes.fromhex(ct))
    return A_set

def guess_key_byte(index):
    real_ans = set(list(range(256)))
    key_pos = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
    while True:
        A_set = get_ciphertexts(index)
        answer = set()
        for i in range(256):
            target = 0
            for state in A_set:
                target ^= inv_sbox[state[index]^i]
            if target == 0:
                answer.add(i)
        real_ans.intersection_update(answer)
        if len(real_ans) == 1:
            return real_ans.pop()
key = []
for i in tqdm(range(16)):
    ans = guess_key_byte(i)
    key.append(ans)
print((key))

hexkey = reverse_key_schedule(bytes(key), 4).hex()
print(hexkey)
f.sendlineafter(b"> ",b"2")
f.sendlineafter(b"Key in hex: ", hexkey.encode())
f.interactive()