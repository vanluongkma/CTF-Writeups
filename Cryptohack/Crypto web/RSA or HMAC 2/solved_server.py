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

print("""\033[96m SOLVED SERVER""")


def get_jwt(username):
    return requests.get(
        f"https://web.cryptohack.org/rsa-or-hmac-2/create_session/{username}/"
    ).json()["session"]

def get_sig_and_m(username):
    sig = bytes_to_long(base64url_decode(get_jwt(username).split(".")[-1]))
    _, m = rs256_sign({"username": username, "admin": False}, key)
    return sig, m

s1, m1 = get_sig_and_m("username1")
s2, m2 = get_sig_and_m("username2")

print(f"{s1 = }")
print(f"{s2 = }")
print(f"{m1 = }")
print(f"{m2 = }")

a = gmpy2.mpz(s1) ** 65537 - gmpy2.mpz(m1)
b = gmpy2.mpz(s2) ** 65537 - gmpy2.mpz(m2)
print("gcd")
n = int(gmpy2.gcdext(a, b)[0])
print(n)
pubkey = RSA.construct((n, 65537)).export_key().decode()
print(pubkey)
with open("pub_server.pem", "w") as f:
    f.write(pubkey)

os.system("openssl rsa -pubin -in pub_server.pem -RSAPublicKey_out -outform PEM -out re_pub_server.pem")

with open("re_pub_server.pem", "r") as f:
    PUBLIC_KEY= f.read()

PUBLIC_KEY = "\n".join(PUBLIC_KEY.splitlines())
PUBLIC_KEY = PUBLIC_KEY.encode() + b'\n'

def create_session_server(username):
    encoded = jwt.encode({'username': username, 'admin': True}, PUBLIC_KEY, algorithm='HS256')
    return encoded

def authorise_server(token):
    return requests.get(
        f"https://web.cryptohack.org/rsa-or-hmac-2/authorise/{token}/"
    ).json()

session = create_session_server('username')
print(session)
print(authorise_server(session))
