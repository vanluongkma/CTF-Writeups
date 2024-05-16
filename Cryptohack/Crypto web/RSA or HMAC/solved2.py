# import jwt 

# # PKCS#1 pem file is test.pem
# with open('rsa-or-hmac-public.pem', 'rb') as f:
#     PUBLIC_KEY = f.read()

# # # Change \r\n on Windows to \n
# # PUBLIC_KEY = "\n".join(PUBLIC_KEY.splitlines())
# # PUBLIC_KEY = PUBLIC_KEY.encode() + b'\n'

# # print(PUBLIC_KEY)

# # with open("pub.pem", "w") as f:
# #     f.write(PUBLIC_KEY.decode())
# def create_session(username):
#     encoded = jwt.encode({'username': username, 'admin': True}, PUBLIC_KEY, algorithm='HS256')
#     return encoded

# print(create_session('username'))

import jwt_patched as jwt
from pwn import *
import requests

def get_jwt():
    return requests.get(
        f"https://web.cryptohack.org/rsa-or-hmac/get_pubkey/"
    ).json()["pubkey"]
PUBLIC_KEY = get_jwt()

print(PUBLIC_KEY)
def create_session(username):
    encoded = jwt.encode({'username': username, 'admin': True}, PUBLIC_KEY, algorithm='HS256')
    return encoded

print(create_session('username'))
