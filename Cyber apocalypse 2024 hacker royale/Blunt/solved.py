from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import getPrime, long_to_bytes
from hashlib import sha256
from sympy.ntheory.residue_ntheory import discrete_log
import random


p = 0xdd6cc28d
g = 0x83e21c05
A = 0xcfabb6dd
B = 0xc4a21ba9
ciphertext = b'\x94\x99\x01\xd1\xad\x95\xe0\x13\xb3\xacZj{\x97|z\x1a(&\xe8\x01\xe4Y\x08\xc4\xbeN\xcd\xb2*\xe6{'

a = discrete_log(p, A, g)
b = discrete_log(p, B, g)

C = pow(B, a, p)
assert C == pow(B, a, p)

# now use it as shared secret
hash = sha256()
hash.update(long_to_bytes(C))

key = hash.digest()[:16]
iv = b'\xc1V2\xe7\xed\xc7@8\xf9\\\xef\x80\xd7\x80L*'
cipher = AES.new(key, AES.MODE_CBC, iv)

fl = cipher.decrypt(pad(ciphertext, 16))
print(f'found = {fl}')
