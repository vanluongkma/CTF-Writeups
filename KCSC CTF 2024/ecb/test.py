from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad
from os import urandom
import json
import socket
import threading

flag = 'KCSC{s0m3_r3ad4ble_5tr1ng_like_7his}'

key = b"dinhvanluong0000"
cipher = AES.new(key, AES.MODE_ECB)
users = ['admin']

def login(token):
    data = cipher.decrypt(bytes.fromhex(token))
    print(f"{data = }")
    return data
    
def register(user):
    data = b'{"username": "%s", "isAdmin": false}' % (user.encode())
    print(f"{data = }")
    token = cipher.encrypt(pad(data, 16)).hex()
    print(f"{token = }")
    return token

user = '\x00\x00{"username":           "admin", "isAdmin": true}'
token = register(user)
data = login(token)
token = token[32:128]
add = (b'\x00\x00\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10').decode()
token_add = register(add)
data_add = login(token_add)
token_add = token_add[32:64]
send = token + token_add
print(login(send))
verify = json.loads(unpad(cipher.decrypt(bytes.fromhex(send)), 16))
print(verify, "1")