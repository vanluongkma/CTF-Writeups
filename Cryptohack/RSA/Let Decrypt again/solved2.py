from pwn import *
from json import *
from Crypto.Util.number import bytes_to_long
from pkcs1 import emsa_pkcs1_v15
from sage.all import Mod, discrete_log

HOST = 'socket.cryptohack.org'
PORT = 13394

def send(msg):
    return r.sendline(dumps(msg).encode())

def cvt(msg):
    return bytes_to_long(emsa_pkcs1_v15.encode(msg.encode(), 768 // 8))

r = remote(HOST, PORT)
r.recv()
option = {'option': 'get_signature'}
send(option)
s = int(loads(r.recv())['signature'], 16)

p, k = 2010103, 50
n = p**k

option = {'option': 'set_pubkey', 'pubkey': hex(n)}
send(option)
suffix = loads(r.recv())['suffix']

m1 = 'This is a test for a fake signature.' + suffix
m2 = 'My name is Zupp and I own CryptoHack.org' + suffix
m3 = 'Please send all my money to 3EovkHLK5kkAbE8Kpe53mkEbyQGjyf8ECw' + suffix

msg1, msg2, msg3 = cvt(m1), cvt(m2), cvt(m3)
s = Mod(s, n)
msg1, msg2, msg3 = Mod(msg1, n), Mod(msg2, n), Mod(msg3, n)
e1 = discrete_log(msg1, s)
e2 = discrete_log(msg2, s)
e3 = discrete_log(msg3, s)

assert pow(s, e1, n) == msg1
assert pow(s, e2, n) == msg2
assert pow(s, e3, n) == msg3

option1 = {
    'option': 'claim',
    'msg': m1,
    'index': int(0),
    'e': hex(e1)
}
send(option1)
sec1 = bytes.fromhex(loads(r.recv())['secret'])

option2 = {
    'option': 'claim',
    'msg': m2,
    'index': int(1),
    'e': hex(e2)
}
send(option2)
sec2 = bytes.fromhex(loads(r.recv())['secret'])

option3 = {
    'option': 'claim',
    'msg': m3,
    'index': int(2),
    'e': hex(e3)
}
send(option3)
sec3 = bytes.fromhex(loads(r.recv())['secret'])

flag = xor(sec1, sec2, sec3).decode()
print(flag)