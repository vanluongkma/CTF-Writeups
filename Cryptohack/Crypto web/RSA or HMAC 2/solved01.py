import jwt_patched as jwt
from pwn import *
import requests

def authorise(token):
    return requests.get(
        f"https://web.cryptohack.org/rsa-or-hmac-2/authorise/{token}/"
    ).json()

# with open("pub.pem", "rb") as f:
#     PUBLIC_KEY = f.read()

# print(PUBLIC_KEY)
# with open("rsa-or-hmac-2-private.pem", "rb") as f:
#     PRIVATE_KEY = f.read()
    
# with open("rsa-or-hmac-2-public.pem", "rb") as f:
#     PUBLIC_KEY = f.read()

with open("pub.pem", "rb") as f:
    PUBLIC_KEY1 = f.read()
def create_session(username):
    encoded = jwt.encode({'username': username, 'admin': True}, PUBLIC_KEY1, algorithm='HS256')
    return encoded


session = create_session("admin")
print(session)
print(authorise(session))

# with open('rsa-or-hmac-2-private.pem', 'rb') as f:
#    PRIVATE_KEY = f.read()
# with open('rsa-or-hmac-2-public.pem', 'rb') as f:
#    PUBLIC_KEY = f.read()


# FLAG = "KCSC{1234374658969508964273euh_3857238_}"


# def authorise(token):
#     try:
#         decoded = jwt.decode(token, PUBLIC_KEY, algorithms=['HS256', 'RS256'])
#     except Exception as e:
#         return {"error": str(e)}

#     if "admin" in decoded and decoded["admin"]:
#         return {"response": f"Welcome admin, here is your flag: {FLAG}"}
#     elif "username" in decoded:
#         return {"response": f"Welcome {decoded['username']}"}
#     else:
#         return {"error": "There is something wrong with your session, goodbye"}


# def create_session(username):
#     encoded = jwt.encode({'username': username, 'admin': False}, PRIVATE_KEY, algorithm='RS256')
#     return {"session": encoded}


# # test local

# with open("pub.pem", "rb") as f:
#     PUBLIC_KEY = f.read()

# print(PUBLIC_KEY)
# def create_session(username):
#     encoded = jwt.encode({'username': username, 'admin': True}, PUBLIC_KEY, algorithm='RS256')
#     return encoded

# print(create_session('username'))
# print(authorise(create_session('username')))