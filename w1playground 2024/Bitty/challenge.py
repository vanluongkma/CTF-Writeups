import random
import binteger
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def getbit():
    return random.getrandbits(1)

FLAG = open("flag.txt", "rb").read()

known = b''
for _ in range(2500):
    word = binteger.Bin([getbit() for _ in range(8)]).int
    known += word.to_bytes(1, "big")

with open("known", "wb") as f:
    f.write(known)

key = b""
for _ in range(16):
    word = binteger.Bin([getbit() for _ in range(8)]).int
    key += word.to_bytes(1, "big")

cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(pad(FLAG, 16))
open("output.txt", "w").write(ciphertext.hex())

# 5f0512a86cd89a47ecd5cb77af672f9137ecb5cd0c6141d0d5cd4257f0b4e72588d87fbc0f4cb0660ee0a4483bfbdf1a