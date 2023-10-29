from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
import hashlib


with open("flag.enc", "rb") as f:
    data = f.read()

data = pad(data, AES.block_size)
iv = data[:AES.block_size]
ct = data[AES.block_size:]
key = hashlib.sha256(b"tasciewapeoiu").digest()

flag = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
print(flag)
# UDCTF{N0th1ng_pr0t3cts_4gainst_5l0ppiness}\x06\x06\x06\x06\x06\x06 \x9f\x9b\xe4\xe2\xd6\x17\xe6k\x1e\xa1^\xde\xb6\x0e|
