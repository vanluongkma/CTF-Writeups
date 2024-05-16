from pwn import *
from Crypto.Util.number import long_to_bytes, inverse, bytes_to_long
from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192
import hashlib
import json
from random import randrange
from datetime import datetime

r = remote('socket.cryptohack.org', 13381)

context.log_level = 'DEBUG'

r.recvuntil('\n')
data = {
    'option': 'sign_time'
}

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
    if n == 2:
        r.sendline(json.dumps(data))
        r.interactive()
        data = r.recvuntil('\n')
        data = json.loads(data)
        print(data)
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
        print(r.recvuntil('\n'))