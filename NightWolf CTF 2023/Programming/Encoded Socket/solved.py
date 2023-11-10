from math import *
from pwn import *
import base64
import binascii

def decode_binary_string(s, encoding='UTF-8'):
    byte_string = ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))
    return byte_string

f = connect("152.67.127.64", 8025)
f.recvline()
for i in range(1000):
    a = f.recv()
    if b"What is the answer for 2:" in a:
        q = a.decode().strip()
        qq = q.split("2:")[1].rstrip("?")
        decoded_string = decode_binary_string(qq)
        f.sendline(decoded_string)
        f.recvline()
    elif b"What is the answer for 8:" in a:
        q = a.decode().strip()
        qq = q.split("8:")[1].rstrip("?")
        qq = qq.encode()
        parts = [qq[i:i+3] for i in range(0, len(qq), 3)]
        ascii_string = ''.join(chr(int(part, 8)) for part in parts)

        f.sendline(ascii_string)
        f.recvline()
    elif b"What is the answer for 64:" in a:
        q = a.decode().strip()
        qq = q.split("64:")[1].rstrip("?")
        f.sendline(base64.b64decode(qq))
        f.recvline()
    elif b"What is the answer for 16:" in a:
        q = a.decode().strip()
        qq = q.split("16:")[1].rstrip("?")
        f.sendline(binascii.unhexlify(qq))
        f.recvline()
    elif b"What is the answer for 32:" in a:
        q = a.decode().strip()
        qq = q.split("32:")[1].rstrip("?")
        f.sendline(base64.b32decode(qq))
        f.recvline()

f.recvline()
f.close()
