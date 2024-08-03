from Crypto.Util.number import *
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES

enc = b'\x16\x97,\xa7\xfb_\xf3\x15.\x87jKRaF&"\xb6\xc4x\xf4.K\xd77j\xe5MLI_y\xd96\xf1$\xc5\xa3\x03\x990Q^\xc0\x17M2\x18'
flag_hash = "6a96111d69e015a07e96dcd141d31e7fc81c4420dbbef75aef5201809093210e"
key = b'the_enc_key_is_'
iv = b'my_great_iv_is_'

for i in range(256):
    for j in range(256):
        _key = key + bytes([i])
        _iv = iv + bytes([j])
        cipher =  AES.new(_key, AES.MODE_CBC, _iv)
        flag = cipher.decrypt(enc)
        try:
            if b"FLAG" in flag:
                print(unpad(flag, 16))
                break
        except:
            continue