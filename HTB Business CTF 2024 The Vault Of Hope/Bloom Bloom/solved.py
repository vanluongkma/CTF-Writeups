from output import *
from random import randint, shuffle
from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
import os

out = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

KEY = sha256(out.encode()).digest()

strr = []
for i in enc_messages:
    for j in i:
        try:
            cipher = AES.new(KEY, AES.MODE_CBC, bytes.fromhex(j[0]))
            strr.append(cipher.decrypt(bytes.fromhex(j[1])).decode())
            break
        except:
            pass

for i in strr:
    print(i)