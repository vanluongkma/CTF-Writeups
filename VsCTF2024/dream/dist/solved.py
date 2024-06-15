from pwn import *
import random

def recv():
    outputs = []
    ciphertext = None

    for i in range(0, 624, 8):
        # f = process(["python3", "chall.py"])
        f = connect("vsc.tf", 5001)
        context.log_level = 'debug'
        
        indices = list(range(i, min(i + 8, 624)))
        f.sendlineafter(b">>>", str(indices).encode())
        
        for _ in indices:
            try:
                output = int(f.recvline().strip())
                outputs.append(output)
            except EOFError:
                break

        if ciphertext is None:
            try:
                ciphertext = f.recvline().strip().decode()
                ciphertext = bytes.fromhex(ciphertext)
            except EOFError:
                break
        
        f.close()
    
    return outputs, ciphertext

outputs, ciphertext = recv()
print(outputs)
print(ciphertext)
print(len(ciphertext))

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256

import randcrack

rc = randcrack.RandCrack()

for output in outputs:
    rc.submit(output)

key = rc.predict_getrandbits(256)
nonce = rc.predict_getrandbits(256)
print(key)
print(nonce)


cipher = AES.new(sha256(str(key).encode()).digest()[:16], AES.MODE_GCM, nonce=sha256(str(nonce).encode()).digest()[:16])
print(cipher.decrypt(ciphertext))