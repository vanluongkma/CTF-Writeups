from hashlib import sha256
from pwn import * 
import json 
from Crypto.Util.number import long_to_bytes
import os 

io = remote('socket.cryptohack.org', 13402)
io.recvline()

FLAG = b"crypto{???????????????????????????????}"

# Check whether the hash exists in the table of 256 hashes of string
# with equal bytes
def check_guess(hash):
    for i in range(256):
        msg = bytes([i]) * len(FLAG)
        if sha256(msg).hexdigest() == hash: 
            return 0 
    
    return 1 

flag = 0

for i in range(8 * len(FLAG)):
    msg = long_to_bytes(1 << i)
    msg = b'\x00' * (len(FLAG) - len(msg)) + msg 
    bit = 0 

    # Send 5 times to avoid false negative 
    for j in range(5):
        to_send = {'option': 'mix', 'data': msg.hex()}
        io.sendline(json.dumps(to_send).encode())
        target = json.loads(io.recvline().decode())['mixed']
        if check_guess(target) == 1:
            bit = 1 
    flag += bit << i 
    print(long_to_bytes(flag))
