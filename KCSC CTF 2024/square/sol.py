from pwn import *
from tqdm import *
import os
from miniAES import *
from aeskeyschedule import reverse_key_schedule

target = process(["python3", "chall.py"])

def encrypt(pt:bytes):
    target.sendlineafter(b"[-] plaintext(hex): ", pt.hex().encode())
    ct = target.recvline()[:-1][len("[+] ciphertext(hex): "):].decode()
    return bytes.fromhex(ct)

def find_key_bytes(idx:int):
    real_ans = set(list(range(256)))
    key_pos = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
    while True:
        ans = set()
        A_set = []
        init = os.urandom(16)
        for i in range(256):
            temp = bytearray(init)
            temp[idx] = i
            A_set += [encrypt(temp)]
        
        for i in range(256):
            A_set_dec = 0
            for ele in A_set:
                # temp = bytearray(ele)
                # temp[idx] ^= i
                # ele_dec_arr = list(temp)
                # InvShiftRows(ele_dec_arr)
                # InvSubBytes(ele_dec_arr)
                # A_set_dec ^= ele_dec_arr[key_pos[idx]]
                A_set_dec ^= InvS_box[ele[idx] ^ i]
            if A_set_dec == 0:
                ans.add(i)
        real_ans.intersection_update(ans)
        if len(real_ans) == 1:
            return real_ans.pop()

key = []
for i in tqdm(range(16)):
    ans = find_key_bytes(i)
    key.append(ans)

hexkey = reverse_key_schedule(bytes(key), 4).hex()
target.sendline(b"")
target.sendlineafter(b"key(hex): ", hexkey.encode())
print(hexkey)
target.interactive()