from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import time
from pwn import*

enc_mess = b'\x18o\xe0\x9d\xab\xbb\xddK\x7f[7\x84/\x1d\x01!'
enc_flag = b'\xb5\x8aE?6\x1c\x04N\xc8\xf8\x94\x17\xa4\xaaU\xdc\x0f\x08\xa5\x88\x8c\xf74\x9f\xe2\xaaI\xd6\xd0\x84T\x1e\x96\x80\t\xa0\xa3M6x\x82\xdf\xf5\x1c\xb7\xf4+!'

for i in range(0,1000000):
    new_seed = i
    key = b''
    for _ in range(8):
        ran_num = int(str(new_seed * new_seed).zfill(12)[3:9])
        key += (ran_num % (2 ** 16)).to_bytes(2, 'big')
        new_seed = ran_num
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(enc_mess)
    if b"aa" in plaintext:
        key = b''
        for _ in range(8):
            ran_num = int(str(new_seed * new_seed).zfill(12)[3:9])
            key += (ran_num % (2 ** 16)).to_bytes(2, 'big')
            new_seed = ran_num
        cipher = AES.new(key, AES.MODE_ECB)
        plaintext = cipher.decrypt(enc_flag)
        print(plaintext)