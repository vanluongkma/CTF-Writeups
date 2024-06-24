import jwt_patched as jwt
from pwn import *
import requests

def get_jwt():
    return requests.get(
        f"https://web.cryptohack.org/rsa-or-hmac/get_pubkey/"
    ).json()["pubkey"]
# with open("pubkey.pem", "rb") as file:
#     PUBLIC_KEY = file.read()
PUBLIC_KEY = get_jwt()
with open("pubkey.pem", "w") as file:
    file.write(PUBLIC_KEY)


print(PUBLIC_KEY)


with open("pubkey.pem", "r") as file:
    PUBLIC_KEY12 = file.read()

PUBLIC_KEY12 = "\n".join(PUBLIC_KEY12.splitlines())
PUBLIC_KEY12 = PUBLIC_KEY12.encode() + b'\n'
print(PUBLIC_KEY12)

def create_session(username):
    encoded = jwt.encode({'username': username, 'admin': True}, PUBLIC_KEY12, algorithm='HS256')
    return encoded

session = (create_session('username'))

def authorise(token):
    return requests.get(
        f"https://web.cryptohack.org/rsa-or-hmac/authorise/{token}/"
    ).json()

print("""\033[95m FLAG""")
print(authorise(session))