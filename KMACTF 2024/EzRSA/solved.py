from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.PublicKey import RSA
from hashlib import sha1, sha256, sha384, sha512, md5
import gmpy2
from pwn import *
import re
from base64 import b64encode

def forge_signature(message,prefix, n, e):
    key_length = len(bin(n)) - 2
    block = b'\x00\x01\xff\x00' + prefix + message
    garbage = (((key_length + 7) // 8) - len(block)) * b'\xff'
    block += garbage

    pre_encryption = bytes_to_long(block)
    forged_sig = gmpy2.iroot(pre_encryption, e)[0]

    return long_to_bytes(forged_sig)

f = connect("157.15.86.73", 2003, level='debug')
# f = process(["python3", "server.py", "DEBUG"])
f.recvuntil(b"Hash: ")
hash_name = f.recvline().strip()
f.recvuntil(b"Modulus = ")
n = int(f.recvline().decode().strip())
e = 3
msg = b'0' * 15
HASH_ASN1 = {
    b'MD5': b'\x30\x20\x30\x0c\x06\x08\x2a\x86\x48\x86\xf7\x0d\x02\x05\x05\x00\x04\x10',
    b'SHA-1': b'\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14',
    b'SHA-256': b'\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20',
    b'SHA-384': b'\x30\x41\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x02\x05\x00\x04\x30',
    b'SHA-512': b'\x30\x51\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x03\x05\x00\x04\x40'
}
HASH_FUNC = {
    b'MD5': hashlib.md5(msg).digest(),
    b'SHA-1': hashlib.sha1(msg).digest(),
    b'SHA-256': hashlib.sha256(msg).digest(),
    b'SHA-384': hashlib.sha384(msg).digest(),
    b'SHA-512': hashlib.sha512(msg).digest()
}
    
hash_mess = HASH_FUNC[hash_name]

if hash_name in HASH_ASN1:
    HASH = HASH_ASN1[hash_name]
else:
    raise ValueError("Unsupported hash algorithm")

f.sendlineafter(b'Enter the message you want to verify:', msg)
base64_signature = b64encode(forge_signature(hash_mess, HASH, n, e))
f.sendlineafter(b'Enter its base64 signature:', base64_signature)
f.recvline()