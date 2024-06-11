from pwn import *
from randcrack import RandCrack
from Crypto.Util.number import long_to_bytes

rc = RandCrack()
p = remote('20.80.240.190', 4447, level = 'debug')
username = "0" * 25 + b'\xe1\x94\x89'.decode()
p.sendlinethen(b'IV used during this session:  ', username.encode())
iv = bytearray.fromhex(p.recvline(keepends=False).decode())
for _ in range(624 // 4):
    iv[-1] ^= 2 ^ (48 + 1)
    iv[-2] ^= ord('C') ^ 0x8c
    p.recvuntil(b'Your new token is :  ')
    enc = bytearray.fromhex(p.recvline(keepends=False).decode())
    enc[79 - 16] ^= 1
    p.sendline(b'1')
    p.sendlinethen(b'encrypt is ', (iv + enc).hex().encode())
    randbits128 = bytes.fromhex(p.recvline()[:-2].decode())
    big = randbits128[::-1]
    for i in range(4):
        randbits32 = int.from_bytes(big[i * 4: i * 4 + 4], byteorder='little')
        rc.submit(randbits32)
rc.predict_getrandbits(128)
p.sendline(b'2')
p.sendline(long_to_bytes(rc.predict_getrandbits(128)).hex().encode())
p.interactive()