from Crypto.Signature.pkcs1_15 import _EMSA_PKCS1_V1_5_ENCODE
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Util.number import long_to_bytes, bytes_to_long
import jwt_patched as jwt
import json
import base64
import gmpy2

# Private key generated using: openssl genrsa -out rsa-or-hmac-2-private.pem 2048
with open("rsa-or-hmac-2-private.pem", "rb") as f:
    PRIVATE_KEY = f.read()
# Public key generated using: openssl rsa -in rsa-or-hmac-2-private.pem -out rsa-or-hmac-2-public.pem -RSAPublicKey_out
with open("rsa-or-hmac-2-public.pem", "rb") as f:
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


# Sanity check
# key = RSA.import_key(PRIVATE_KEY)
# data = str({"a": "a"})
# jsig = jwt.encode(data, PRIVATE_KEY, algorithm="RS256").split(b".")[2]

key = RSA.import_key(PRIVATE_KEY)
data = {"a": "a"}  # Data should be a dictionary
signature, _ = rs256_sign(data, key)  # Signing the payload
encoded_signature = long_to_bytes(signature)  # Convert the signature to bytes
jsig = base64url_encode(encoded_signature)  # Encode the signature using base64url encoding

print(jsig)
sig, m = rs256_sign(data, key)
assert pow(sig, key.e, key.n) == m
assert base64url_encode(long_to_bytes(sig)) == jsig
print("kdncks dn ffdkvndskv dkemf")
import requests


def get_jwt(username):
    return requests.get(
        f"https://web.cryptohack.org/rsa-or-hmac-2/create_session/{username}/"
    ).json()["session"]


# Local testing
# def get_jwt(username):
#     return jwt.encode(
#         {"username": username, "admin": False}, PRIVATE_KEY, algorithm="RS256"
#     ).decode()


def get_sig_and_m(username):
    sig = bytes_to_long(base64url_decode(get_jwt(username).split(".")[-1]))
    _, m = rs256_sign({"username": username, "admin": False}, key)
    return sig, m


s1, m1 = get_sig_and_m("peko")
s2, m2 = get_sig_and_m("miko")

# mpz for faster exponentiation
a = gmpy2.mpz(s1) ** 65537 - gmpy2.mpz(m1)
b = gmpy2.mpz(s2) ** 65537 - gmpy2.mpz(m2)
print("running gcd")
n = int(gmpy2.gcdext(a, b)[0])
print(n)
pk = RSA.construct([n, 65537]).export_key().decode()
print(pk)
with open("pub.pem", "w") as f:
    f.write(pk)