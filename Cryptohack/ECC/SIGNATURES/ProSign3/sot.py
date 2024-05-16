from pwn import *
from Crypto.Util.number import *
from ecdsa.ecdsa import generator_192
import hashlib, json
from datetime import datetime

def sha1(data):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(data)
    return sha1_hash.digest()

g = generator_192
mod = g.order()

while True:
    now = datetime.now()
    m, n = int(now.strftime("%m")), int(now.strftime("%S"))
    current = f"{m}:{n}"
    try:
        r = connect('socket.cryptohack.org', 13381, level = 'debug')
        r.recvuntil('\n')
        r.sendline(json.dumps({'option': 'sign_time'}))
        data = r.recvuntil('\n')
        data = json.loads(data)

        msg = data['msg']
        sig_r = data['r']
        sig_s = data['s']
        hsh = bytes_to_long(sha1(msg.encode()))
        sig_r = int(sig_r, 16)
        sig_s = int(sig_s, 16)
        mymsg = "unlock"
        myhsh = bytes_to_long(sha1(mymsg.encode()))
        x = (sig_s - hsh) * inverse(sig_r, mod) % mod
        newSigS = (myhsh + x * sig_r) % mod
        r.sendline(json.dumps({'option': 'verify', 'msg': mymsg, 'r': hex(sig_r), 's': hex(newSigS)}))
        flag = (r.recvuntil('\n'))
    except:
        continue
    if b"crypto" in flag:
        print(flag)
        break



# from Crypto.Util.number import inverse, bytes_to_long
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
# from random import randint
# from hashlib import sha1
# import os
# from sage.all import *

# FLAG = b'crypto{????????????????????????????????????}'


# class TwistedEdwards():
#     # Elliptic curve in Edwards form:
#     # -x**2 + y**2 = 1 + d*x**2*y**2
#     # birationally equivalent to the Montgomery curve:
#     # y**2 = x**3 + 2*(1-d)/(1+d)*x**2 + x

#     def __init__(self, p, d, order, x0bit, y0):
#         self.p = p
#         self.d = d
#         self.order = order
#         self.base_point = (x0bit, y0)

#     def recover_x(self, xbit, y):
#         xsqr = (y**2 - 1)*inverse(1 + self.d*y**2, self.p) % self.p
#         x = pow(xsqr, (self.p + 1)//4, self.p)
#         if x**2 == xsqr :
#             if int(x) & 1 != xbit:
#                 return p - x
#             return x
#         return 0

#     def decompress(self, compressed_point):
#         xbit, y = compressed_point
#         x = self.recover_x(xbit, y)
#         return (x, y)

#     # complete point addition formulas
#     def add(self, P1, P2):
#         x1, y1 = P1
#         x2, y2 = P2
        
#         C = x1*x2 % self.p
#         D = y1*y2 % self.p
#         E = self.d*C*D
#         x3 = (1 - E)*((x1 + y1)*(x2 + y2) - C - D) % self.p
#         y3 = (1 + E)*(D + C) % self.p
#         z3 = 1 - E**2 % self.p
#         z3inv = inverse(z3, self.p)
#         return (x3*z3inv % self.p, y3*z3inv % self.p)

#     # left-to-right double-and-add
#     def single_mul(self, n, compressed_point):
#         P = self.decompress(compressed_point)        
#         t = int(n).bit_length()
#         if n == 0:
#             return (0,1)
#         R = P
#         for i in range(t-2,-1,-1):
#             bit = (n >> i) & 1
#             R = self.add(R, R)
#             if bit == 1:
#                 R = self.add(R, P)
#         return (int(R[0]) & 1, int(R[1]))


# def gen_key_pair(curve):
#     n = randint(1, curve.order-1)
#     P = curve.single_mul(n, curve.base_point)
#     return n, P
    
# def gen_shared_secret(curve, n, P):
#     xbit, y = curve.single_mul(n, P)
#     return y
    

# def encrypt_flag(shared_secret: int):
#     # Derive AES key from shared secret
#     key = sha1(str(shared_secret).encode('ascii')).digest()[:16]
#     # Encrypt flag
#     iv = os.urandom(16)
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     ciphertext = cipher.encrypt(pad(FLAG, 16))
#     # Prepare data to send
#     data = {}
#     data['iv'] = iv.hex()
#     data['encrypted_flag'] = ciphertext.hex()
#     return data

# def decrypt_flag(shared_secret, iv, ciphertext):

#     key = sha1(str(shared_secret).encode('ascii')).digest()[:16]

#     iv = bytes.fromhex(iv)
#     ciphertext = bytes.fromhex(ciphertext)
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     plaintext = cipher.decrypt(ciphertext)
#     return unpad(plaintext, AES.block_size)


# # curve parameters
# # birationally equivalent to the Montgomery curve y**2 = x**3 + 337*x**2 + x mod p
# p = 110791754886372871786646216601736686131457908663834453133932404548926481065303
# order = 27697938721593217946661554150434171532902064063497989437820057596877054011573
# d = 14053231445764110580607042223819107680391416143200240368020924470807783733946
# x0bit = 1
# y0 = 11
# curve = TwistedEdwards(p, d, order, x0bit, y0)


# # Alice sends public key: (0, 109790246752332785586117900442206937983841168568097606235725839233151034058387)
# # Bob sends public key: (0, 45290526009220141417047094490842138744068991614521518736097631206718264930032)

# # Alice sends encrypted_flag: {'iv': '31068e75b880bece9686243fa4dc67d0', 'encrypted_flag': 'e2ef82f2cde7d44e9f9810b34acc885891dad8118c1d9a07801639be0629b186dc8a192529703b2c947c20c4fe5ff2c8'}

# A = (0, 109790246752332785586117900442206937983841168568097606235725839233151034058387)
# B = (0, 45290526009220141417047094490842138744068991614521518736097631206718264930032)
# iv = '31068e75b880bece9686243fa4dc67d0'
# encrypted_flag = 'e2ef82f2cde7d44e9f9810b34acc885891dad8118c1d9a07801639be0629b186dc8a192529703b2c947c20c4fe5ff2c8'
# y = curve.decompress((int(x0bit), int(y0)))[1]
# F = GF(p)
# y = F(int(y))
# yA = F(A[1])


# n_a = discrete_log(yA, y)

# shared_secret = gen_shared_secret(curve, n_a, B)

# print(decrypt_flag(shared_secret, iv, encrypted_flag)) 