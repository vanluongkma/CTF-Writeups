import jwt 

# # PKCS#1 pem file is test.pem
# with open('test.pem', 'rb') as f:
#     PUBLIC_KEY = f.read()


# # print("1")
# # # Change \r\n on Windows to \n
# # PUBLIC_KEY = "\n".join(PUBLIC_KEY.splitlines())
# # print(PUBLIC_KEY)
# # print("\n")
# # PUBLIC_KEY = PUBLIC_KEY.encode() + b'\n'

# print(PUBLIC_KEY)

# # with open("pub.pem", "w") as f:
# #     f.write(PUBLIC_KEY.decode())
# def create_session(username):
#     encoded = jwt.encode({'username': username, 'admin': True}, str(PUBLIC_KEY), algorithm='HS256')
#     return encoded

# print(create_session('username'))

# import jwt
# from pwn import *
# import requests

# def get_jwt():
#     return requests.get(
#         f"https://web.cryptohack.org/rsa-or-hmac/get_pubkey/"
#     ).json()["pubkey"]
# PUBLIC_KEY = get_jwt()
# print(PUBLIC_KEY)

# def create_session(username):
#     encoded = jwt.encode({'username': username, 'admin': True}, PUBLIC_KEY, algorithm='HS256')
#     return encoded

# print(create_session('username'))


with open('rsa-or-hmac-private.pem', 'rb') as f:
   PRIVATE_KEY = f.read()
with open('rsa-or-hmac-public.pem', 'rb') as f:
   PUBLIC_KEY = f.read()

FLAG = "bheqfrjfm fkefm23432"

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
    return {"session": encoded}

def get_pubkey():
    return {"pubkey": PUBLIC_KEY}


print(create_session('username'))
print(get_pubkey())

print(authorise("eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6InF2aW5ocHJvbG9sIiwiYWRtaW4iOmZhbHNlfQ.gWPuGQgApoQQj0rZN8eA52oO0Ylvm1BVGU3LXHpQ46Z4RJ3DZWpXsmoBErXf_HTotcNQrZeoJCpwBrfEAmpesjC-29aLl7EB20gBrtbI93uS39_vi0GkAa4yNOtReswQEC5AY27meVUCpdprUIkcysBQhK4nC8qu2wkVZMuR2V4hIVMdInYeIavscrJ6vUzXItt2f7wjJ1AwqzSdJ2_nzy4yhkDHt5H_mni8CvWU5aRODVrdA2FzpFBGlwk08NcSwU4V8Q0XS5PuQH5P_VEHuA_mgQghzpRh21kk4NZQsp3HfEauwdray1ine7sjVcUGlwqNFDPS6XMoB1udWPgIkQ"))

print(authorise("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXJuYW1lIiwiYWRtaW4iOnRydWV9.vc6q_yzmLtSwjPguTtXtSK5-a12s5JP8qLDh7ttLrxk"))