import hashlib
from mycipher import MyCipher

username = 'gureisya'
ciphertext = '3da5f9fa6998a991cb244a12fa72d311f3e6e9fbcac9984c0c'

def make_token(data1: str, data2: str):
    sha256 = hashlib.sha256()
    sha256.update(data1.encode())
    right = sha256.hexdigest()[:20]
    sha256.update(data2.encode())
    left = sha256.hexdigest()[:12]
    token = left + right
    return token

for sec in range(60):
    for minutes in range(60):
        data1 = f'user: {username}, {minutes}:{sec}'
        for i in range(10):
            data2 = f'{username}{i}'
            token = make_token(data1, data2)
            sha256 = hashlib.sha256()
            sha256.update(token[:32].encode())
            key = sha256.hexdigest()[:32]
            nonce = token[:12]
            cipher = MyCipher(key.encode(), nonce.encode())
            decrypted = cipher.encrypt(bytes.fromhex(ciphertext))
            if b'FLAG' in decrypted:
                print(decrypted)
                exit()