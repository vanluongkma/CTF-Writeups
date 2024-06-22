import jwt_patched as jwt # note this is the PyJWT module, not python-jwt
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
jsig = jwt.encode(data, PRIVATE_KEY, algorithm="RS256").encode().split(b".")[2]
sig, m = rs256_sign(data, key)


assert pow(sig, key.e, key.n) == m
assert base64url_encode(long_to_bytes(sig)) == jsig

print("""\033[95m TEST LOCAL""")

def get_sig_and_m(username):
    sig = bytes_to_long(base64url_decode(create_session(username).split(".")[-1]))
    _, m = rs256_sign({"username": username, "admin": False}, key)
    return sig, m

_s1, _m1 = get_sig_and_m("a")
_s2, _m2 = get_sig_and_m("b")

print(f"{_s1 = }")
print(f"{_s2 = }")
print(f"{_m1 = }")
print(f"{_m2 = }")

a = gmpy2.mpz(_s1) ** 65537 - gmpy2.mpz(_m1)

b = gmpy2.mpz(_s2) ** 65537 - gmpy2.mpz(_m2)
print("running gcd")
n = int(gmpy2.gcdext(a, b)[0])
print(f"{n = }")
pk = RSA.construct([n, 65537]).export_key().decode()
print(pk)

def create_session_local(username):
    encoded = jwt.encode({'username': username, 'admin': True}, pk, algorithm='HS256')
    return encoded

session = create_session_local("a")
print(session)
print(authorise(session))















# def get_jwt(username):
#     return requests.get(
#         f"https://web.cryptohack.org/rsa-or-hmac-2/create_session/{username}/"
#     ).json()["session"]

# def get_sig_and_m(username):
#     sig = bytes_to_long(base64url_decode(get_jwt(username).split(".")[-1]))
#     _, m = rs256_sign({"username": username, "admin": False}, key)
#     return sig, m

# # s1 = bytes_to_long(base64url_decode("2tAA3re-8C2EQa0q_WM4F2uqREZR1ygH91Ga-6fCf9SbndFMQ1EDN238pIcyfpjuOWls00DXa3JFv9q29fqo-L0e_M3fqRwltoKoEh1GJ9WSDnwcNs74Dsst0N5_swC8yrYXtsEl45rzS9XnjR2m4YVi-RQqlrIwm5H1i46UzlF6VFFvTZoMCLdSjPBaiwrf9hbmz0GacNyl_xwS8yjlYEzORv7K_klp6zaL1X1PkL5B1SMe2DU9RxGzfg0hYzQPlJmzmegGKojF_FoqnThLqQaBVXMJjMor1eHr1tFJ4VncGuppWu6C0rWwqLsDi04AfLnqO65ZMrPbT9nI_FA5ag"))

# # _, m1 = rs256_sign({"username": "admin1", "admin": False}, key)
# # s2 = bytes_to_long(base64url_decode("tQaRjm73xnLD6t4NagrMhnN-gCEeg9_CqOrQmezbAM2MyFeQELobk9IVrJrbgtOhBQhKnCD3yuIer9X5scPvwghOqt1HbtF-qQSXlN5mDsezO1fcmiCxU7KsEo-Gl264nO1RCd9zPj0bXSQpK1N-2WjiKwBVO8Y2aXj95hS0lnQ7gEK9B1IwkhDAvjNQ4VMsrmvI-fgF1p6nH44owJ5swvYlwTm9y_mCVTKf8P1esQI6XpL4dlhY4zrq9OGPaxTCmFkTkHC4B7nIkZ00NtTONtoTaprrqmo1Z3E4mUQF4QsUW0qRIAe0TKAHD2nVVJAFbqNwU-VVIUa-IyCz5S_YAQ"))
# # _, m2 = rs256_sign({"username": "admin2", "admin": False}, key)

# s1, m1 = get_sig_and_m("a")
# s2, m2 = get_sig_and_m("b")

# print(s1 ,"\n", s2)
# print(m1, "\n", m2)

# a = gmpy2.mpz(s1) ** 65537 - gmpy2.mpz(m1)

# b = gmpy2.mpz(s2) ** 65537 - gmpy2.mpz(m2)
# print("running gcd")
# n = int(gmpy2.gcdext(a, b)[0])
# print(n)
# # n = 30119723976045246500887959920897642376905514522104705876695572516818975656665827754462226597973931127004963194508794779495518118035029841228002850562126612806174354282950756669656076190799693066363785733231859172664786298352294594850108982261525326147060353679479844558827458650965802914077525964824412575118501773357860374735206849817271524812002047307305597712628593230518376740507962518305824812671107459660525177087958778694060270468673690931325503094560625544374011735643694318730778241846282742819834483180624645324880062782719575587058519516842316778261924794437716972651884728674806670910304714203419102131413
# pk = RSA.construct([n, 65537]).export_key().decode()
# print(pk)
# with open("pub.pem", "w") as f:
#     f.write(pk)


# def create_session(username):
#     encoded = jwt.encode({'username': username, 'admin': True}, pk, algorithm='HS256')
#     return encoded


# session = create_session("a")
# print(session)
# print(authorise(session))

# with open("rsa-or-hmac-2-public.pem", "rb") as f:
#     PUBLIC_KEY = f.read()

# def create_session(username):
#     encoded = jwt.encode({'username': username, 'admin': True}, PUBLIC_KEY, algorithm='HS256')
#     return encoded


# session = create_session("a")
# print(session)
# print(authorise(session))


# def authorise(token):
#     return requests.get(
#         f"https://web.cryptohack.org/rsa-or-hmac-2/authorise/{token}/"
#     ).json()


# with open("pub.pem", "rb") as f:
#     PUBLIC_KEY = f.read()


# def create_session(username):
#     encoded = jwt.encode({'username': username, 'admin': True}, PUBLIC_KEY, algorithm='HS256')
#     return encoded

# session = create_session("a")
# print(session)
# print(authorise(session))