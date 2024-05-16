from pwn import *
from json import *
from Crypto.Util.number import *
from pkcs1 import emsa_pkcs1_v15
from sage.all import Mod, discrete_log
from bitcoin import random_key, privtopub, pubtoaddr

f = remote('socket.cryptohack.org', 13394, level = 'debug')
f.recvline()

f.sendline(dumps({"option": "get_signature"}))

s = int(loads(f.recvline())['signature'], 16)

n = int(getPrime(16) ** 128)

f.sendline(dumps({'option': 'set_pubkey', 'pubkey': hex(n)}))

suffix = loads(f.recv())['suffix']

btc_check = pubtoaddr(privtopub(random_key()))

m1 = 'This is a test for a fake signature.' + suffix
m2 = 'My name is Jack and I own CryptoHack.org' + suffix
m3 = "Please send all my money to " + btc_check + suffix

msg1 = bytes_to_long(emsa_pkcs1_v15.encode(m1.encode(), 768 // 8))
msg2 = bytes_to_long(emsa_pkcs1_v15.encode(m2.encode(), 768 // 8))
msg3 = bytes_to_long(emsa_pkcs1_v15.encode(m3.encode(), 768 // 8))

s = Mod(s, n)
e1 = discrete_log(msg1, s)
e2 = discrete_log(msg2, s)
e3 = discrete_log(msg3, s)

print(pow(s, e1, n) == msg1)
print(pow(s, e2, n) == msg2)
print(pow(s, e3, n) == msg3)

option1 = {
    'option': 'claim',
    'msg': m1,
    'index': int(0),
    'e': hex(e1)
}
f.sendline(dumps(option1).encode())

secret1 = bytes.fromhex(loads(f.recv())['secret'])

option2 = {
    'option': 'claim',
    'msg': m2,
    'index': int(1),
    'e': hex(e2)
}
f.sendline(dumps(option2).encode())

secret2 = bytes.fromhex(loads(f.recv())['secret'])

option3 = {
    'option': 'claim',
    'msg': m3,
    'index': int(2),
    'e': hex(e3)
}
f.sendline(dumps(option3).encode())

secret3 = bytes.fromhex(loads(f.recv())['secret'])

print(xor(xor(secret1, secret2), secret3))
