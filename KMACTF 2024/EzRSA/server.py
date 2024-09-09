import base64
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Util.number import *
import random

FLAG = "KMACTF{s0m3_r3ad4ble_5tr1ng_like_7his}"

def verifySignature(public_key, msg: bytes, sig_bytes: bytes, key_size: int, prefix: bytes, namePrefix):
    HASH_FUNC = {
        'MD5': hashlib.md5(msg).digest(),
        'SHA-1': hashlib.sha1(msg).digest(),
        'SHA-256': hashlib.sha256(msg).digest(),
        'SHA-384': hashlib.sha384(msg).digest(),
        'SHA-512': hashlib.sha512(msg).digest()
    }
    message_sum = HASH_FUNC[namePrefix] # mã hash
    print(f"{message_sum = }")
    c = bytes_to_long(sig_bytes)
    print(f"{sig_bytes = }")
    m = long_to_bytes(pow(c, public_key.e, public_key.n))
    em = bytearray(key_size//8)
    em[key_size//8-len(m):] = m
    em = bytes(em)
    print(f"{em = }")
    i = 0
    print("pass0")
    print(em[i], em[i+1])
    if em[i] != 0 or em[i+1] != 1:
        return 0
    print("pass1")

    i = i + 2
    while i < key_size//8 and em[i] == 0xff:
        i += 1
    if em[i] != 0:
        return 0
    i += 1
    print(i, "fsnfud", len(prefix))
    print("pass2")
    print(f"{em[i:i+len(prefix)] = }")
    print(f"{prefix = }")
    # if em[i:i+len(prefix)] != prefix:
    #     return 0
    # print("pass3")

    i = i + len(prefix)
    print(i)
    if em[i:i+len(message_sum)] != message_sum:
        return 0
    print("pass4")
    return 1

def main():
    HASH_ASN1 = {
        'MD5': b'\x30\x20\x30\x0c\x06\x08\x2a\x86\x48\x86\xf7\x0d\x02\x05\x05\x00\x04\x10',
        'SHA-1': b'\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14',
        'SHA-256': b'\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20',
        'SHA-384': b'\x30\x41\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x02\x05\x00\x04\x30',
        'SHA-512': b'\x30\x51\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x03\x05\x00\x04\x40'
    }

    namePrefix = random.choice(list(HASH_ASN1.keys()))
    p, q = getPrime(1024), getPrime(1024)
    modulus = p*q
    key_size = modulus.bit_length()
    # print(key_size)
    public_key = RSA.construct((modulus, 3))
    rsa_public_key = public_key.export_key("PEM")
    print(rsa_public_key)
    with open("private_key.pem", "wb") as f:
        f.write(rsa_public_key)
    print("Hash:", namePrefix)
    print("Modulus =", modulus)

    try:
        message = input("Enter the message you want to verify: ")
        signature = base64.b64decode(input("Enter its base64 signature: "))
    except:
        print("Invalid input!")
        exit()

    err = verifySignature(public_key, message.encode(), signature, key_size, HASH_ASN1[namePrefix], namePrefix)
    print(f"{err = }")
    if err:
        print("Well done! This is your flag:", FLAG)
        exit()
    else:
        print("Not good enough! Try harder! -.-")
        exit()

if __name__ == "__main__":
    main()



