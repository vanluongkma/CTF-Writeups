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

session = (create_session('username'))

def authorise(token):
    return requests.get(
        f"https://web.cryptohack.org/rsa-or-hmac/authorise/{token}/"
    ).json()

print("""\033[95m FLAG""")
print(authorise(session))