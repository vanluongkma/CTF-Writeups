import pyjwt.jwt as jwt
from Crypto.Signature.pkcs1_15 import _EMSA_PKCS1_V1_5_ENCODE
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Util.number import long_to_bytes, bytes_to_long
import json, base64, gmpy2, os, requests

os.system("openssl genrsa -out rsa-or-hmac-2-private.pem 2048")
os.system("openssl rsa -RSAPublicKey_out -in rsa-or-hmac-2-private.pem -out rsa-or-hmac-2-public.pem")


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

# From pyjwt utils.py
def base64url_encode(input):
    return base64.urlsafe_b64encode(input).replace(b"=", b"")

# From pyjwt utils.py
def base64url_decode(input):
    if isinstance(input, str):
        input = input.encode()
    rem = len(input) % 4

    if rem > 0:
        input += b"=" * (4 - rem)

    return base64.urlsafe_b64decode(input)

# From pyjwt algorithm.py flow
def rs256_sign(payload, key):
    msg = (
        base64url_encode(
            json.dumps({"typ": "JWT", "alg": "RS256"}, separators=(",", ":")).encode()
        )
        + b"."
        + base64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    )
    h = SHA256.new(msg)
    padded = _EMSA_PKCS1_V1_5_ENCODE(h, 256)
    m = bytes_to_long(padded)
    return pow(m, key.d, key.n), m

key = RSA.import_key(PRIVATE_KEY)
data = {"a": "a"}
jsig = jwt.encode(data, PRIVATE_KEY, algorithm="RS256").split(b".")[2]
sig, m = rs256_sign(data, key)


assert pow(sig, key.e, key.n) == m
assert base64url_encode(long_to_bytes(sig)) == jsig

print("""\033[95m SOLVED LOCAL""")

def get_sig_and_m(username):
    sig = bytes_to_long(base64url_decode(create_session(username).split(b".")[-1]))
    _, m = rs256_sign({"username": username, "admin": False}, key)
    return sig, m

_s1, _m1 = get_sig_and_m("username1")
_s2, _m2 = get_sig_and_m("username2")

print(f"{_s1 = }")
print(f"{_s2 = }")
print(f"{_m1 = }")
print(f"{_m2 = }")

a = gmpy2.mpz(_s1) ** 65537 - gmpy2.mpz(_m1)
b = gmpy2.mpz(_s2) ** 65537 - gmpy2.mpz(_m2)
print("gcd")
n = int(gmpy2.gcdext(a, b)[0])
print(f"{n = }")
pubkey = RSA.construct((n, 65537)).export_key("PEM").decode()

with open("pub_local.pem", "w") as f:
    f.write(pubkey)

os.system("openssl rsa -pubin -in pub_local.pem -RSAPublicKey_out -outform PEM -out re_pub_local.pem")

with open("re_pub_local.pem", "r") as f:
    PUBLIC_KEY= f.read()

PUBLIC_KEY = "\n".join(PUBLIC_KEY.splitlines())
PUBLIC_KEY = PUBLIC_KEY.encode() + b'\n'

def create_session_local(username):
    encoded = jwt.encode({'username': username, 'admin': True}, PUBLIC_KEY, algorithm='HS256')
    return encoded

session = create_session_local("username")
print(session)
print(authorise(session))