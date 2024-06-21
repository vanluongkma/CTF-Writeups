import jwt_patched as jwt # note this is the PyJWT module, not python-jwt
from Crypto.Signature.pkcs1_15 import _EMSA_PKCS1_V1_5_ENCODE
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Util.number import long_to_bytes, bytes_to_long
import json
import base64
import gmpy2
import os

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
jsig = jwt.encode(data, PRIVATE_KEY, algorithm="RS256").encode().split(b".")[2]
sig, m = rs256_sign(data, key)

assert pow(sig, key.e, key.n) == m
assert base64url_encode(long_to_bytes(sig)) == jsig

# print(f"{ create_session('peko').split('.')[-1] = }")

def get_sig_and_m(username):
    sig = bytes_to_long(base64url_decode("DrSj0mWQNTj5I32WXy1JCcoHX_CwyawgvPRvmXz96DRI7AumDCHG1ATPYLMh2RvTuH7UKoJgGrJnfKIjyjBvby5pitkrlLBx1AJLuQ1CaOHnso6oV_rqrfAY0SES9CJV_wvsZrNsyjOWNC2cd7eMje1X6zoFseNWhjJjyzDUvJhsbIHDONQw5Wosx7qo4sQkAQQkYqlRiOfl3de20pct4DSBbCxeg-zoIMpMtAPb7GNzPhdB-LidzlR8k-3__o2Z48V5jQOEwjVmVxOd-jaWoBGWMV1ltXht5j0fh4U-4M23SNFA_fgDhdQGP23TrTZTH4CerO0KndWUjLP6bM1nTQ"))
    _, m = rs256_sign({"username": "peko", "admin": False}, key)
    return sig, m

s1 = bytes_to_long(base64url_decode("DrSj0mWQNTj5I32WXy1JCcoHX_CwyawgvPRvmXz96DRI7AumDCHG1ATPYLMh2RvTuH7UKoJgGrJnfKIjyjBvby5pitkrlLBx1AJLuQ1CaOHnso6oV_rqrfAY0SES9CJV_wvsZrNsyjOWNC2cd7eMje1X6zoFseNWhjJjyzDUvJhsbIHDONQw5Wosx7qo4sQkAQQkYqlRiOfl3de20pct4DSBbCxeg-zoIMpMtAPb7GNzPhdB-LidzlR8k-3__o2Z48V5jQOEwjVmVxOd-jaWoBGWMV1ltXht5j0fh4U-4M23SNFA_fgDhdQGP23TrTZTH4CerO0KndWUjLP6bM1nTQ"))

_, m1 = rs256_sign({"username": "peko", "admin": False}, key)
s2 = bytes_to_long(base64url_decode("U8IKkMviMJbHon5hEgXarcoajlS6Hv3QMfCai3tQdYLTsG4bDHYrVV9XMQuut-PPaWh0t6IQfRKQgGTMcjp4kgDF6rXseSmLTsxFDW3uP9fGFk7dxFfc1ohTkqQt2Tn_aDRZhwgWYOf9ncAfrOIJegMk_NHIykmy95rgUuHxtudYnj29-YoT6CIKatjZsoxqmZGJnWvE6IkHzZujilDtdPKVpd1Kb3XqhVa0CCQm3Y-0BsnWUpHDuwg-i9OaA7LIEhZCSUG3aVdlkEZU_SMkLsDGLNO-DOKASWN3Yq-9X_p07h-5gaGqy1ceaj4j3H4-SiBoUzUYeRu_OSZ0JM-tfw"))
_, m2 = rs256_sign({"username": "miko", "admin": False}, key)

print(s1 ,"\n", s2)
print(m1, "\n", m2)

a = gmpy2.mpz(s1) ** 65537 - gmpy2.mpz(m1)
b = gmpy2.mpz(s2) ** 65537 - gmpy2.mpz(m2)
print("running gcd")
# n = int(gmpy2.gcdext(a, b)[0])
# print(n)
n = 30119723976045246500887959920897642376905514522104705876695572516818975656665827754462226597973931127004963194508794779495518118035029841228002850562126612806174354282950756669656076190799693066363785733231859172664786298352294594850108982261525326147060353679479844558827458650965802914077525964824412575118501773357860374735206849817271524812002047307305597712628593230518376740507962518305824812671107459660525177087958778694060270468673690931325503094560625544374011735643694318730778241846282742819834483180624645324880062782719575587058519516842316778261924794437716972651884728674806670910304714203419102131413
pk = RSA.construct([n, 65537]).export_key().decode()
print(pk)
with open("pub.pem", "w") as f:
    f.write(pk)


def create_session(username):
    encoded = jwt.encode({'username': username, 'admin': True}, pk, algorithm='HS256')
    return encoded


session = create_session("admin")
print(session)
print(authorise(session))

with open("rsa-or-hmac-2-public.pem", "rb") as f:
    PUBLIC_KEY = f.read()

def create_session(username):
    encoded = jwt.encode({'username': username, 'admin': True}, PUBLIC_KEY, algorithm='HS256')
    return encoded


session = create_session("admin")
print(session)
print(authorise(session))