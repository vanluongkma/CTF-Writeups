


from Crypto.Cipher import AES
from Crypto.Util.Padding import*
import os


def decrypt_ecb():
    key = bytes(input())
    ciphertext = 
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

