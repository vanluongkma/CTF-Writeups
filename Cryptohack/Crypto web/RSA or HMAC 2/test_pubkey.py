import jwt_patched as jwt # note this is the PyJWT module, not python-jwt
from Crypto.Signature.pkcs1_15 import _EMSA_PKCS1_V1_5_ENCODE
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Util.number import long_to_bytes, bytes_to_long
import json, base64, gmpy2, os, requests

# Private key generated using: openssl genrsa -out rsa-or-hmac-2-private.pem 2048
with open('rsa-or-hmac-2-private.pem', 'rb') as f:
   PRIVATE_KEY = f.read()
# Public key generated using: openssl rsa -RSAPublicKey_out -in rsa-or-hmac-2-private.pem -out rsa-or-hmac-2-public.pem
with open('rsa-or-hmac-2-public.pem', 'rb') as f:
   PUBLIC_KEY = f.read()

FLAG = "KCSC{1234374658969508964273euh_3857238_}"



def authorise(token):
    try:
        decoded = jwt.decode(token, PUBLIC_KEY, algorithms=['HS256', 'RS256'])
    except Exception as e:
        return {"error": str(e)}

    if "admin" in decoded and decoded["admin"]:
        return {"response": f"Welcome admin, here is your flag: {FLAG}"}
    elif "username" in decoded:
        return {"response": f"Welcome {decoded['username']}"}
    else:
        return {"error": "There is something wrong with your session, goodbye"}


def create_session(username):
    encoded = jwt.encode({'username': username, 'admin': False}, PRIVATE_KEY, algorithm='RS256')
    return encoded


with open("pub.pem", "rb") as f:
    pk = f.read()


def create_session(username):
    encoded = jwt.encode({'username': username, 'admin': True}, pk, algorithm='HS256')
    return encoded


session = create_session("a")
print(session)
print(authorise(session))


def create_session(username):
    encoded = jwt.encode({'username': username, 'admin': True}, PUBLIC_KEY, algorithm='HS256')
    return encoded


session = create_session("a")
print(session)
print(authorise(session))