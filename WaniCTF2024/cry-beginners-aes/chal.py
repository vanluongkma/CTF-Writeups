# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from os import urandom
import hashlib

key = b'the_enc_key_is_'
iv = b'my_great_iv_is_'
key += urandom(1)
iv += urandom(1)

cipher = AES.new(key, AES.MODE_CBC, iv)
FLAG = b'FLAG{This_is_a_dummy_flag}'
flag_hash = hashlib.sha256(FLAG).hexdigest()

msg = pad(FLAG, 16)
enc = cipher.encrypt(msg)

print(f'enc = {enc}') # bytes object
print(f'flag_hash = {flag_hash}') # str object

# enc = b'\x16\x97,\xa7\xfb_\xf3\x15.\x87jKRaF&"\xb6\xc4x\xf4.K\xd77j\xe5MLI_y\xd96\xf1$\xc5\xa3\x03\x990Q^\xc0\x17M2\x18'
# flag_hash = 6a96111d69e015a07e96dcd141d31e7fc81c4420dbbef75aef5201809093210e