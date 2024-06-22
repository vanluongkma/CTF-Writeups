# from Crypto.Util.number import long_to_bytes, bytes_to_long
# from Crypto.Util.Padding import unpad


# def rotl(x, y):
#     x &= 0xFFFFFFFFFFFFFFFF
#     return ((x << y) | (x >> (64 - y))) & 0xFFFFFFFFFFFFFFFF

# class MyCipher:
#     def __init__(self, s0, s1):
#         self.X = s0
#         self.Y = s1
#         self.mod = 0xFFFFFFFFFFFFFFFF
#         self.BLOCK_SIZE = 8
    
#     def get_key_stream(self):
#         s0 = self.X
#         s1 = self.Y
#         sum = (s0 + s1) & self.mod
#         s1 ^= s0
#         key = []
#         for _ in range(8):
#             key.append(sum & 0xFF)
#             sum >>= 8
        
#         self.X = (rotl(s0, 24) ^ s1 ^ (s1 << 16)) & self.mod
#         self.Y = rotl(s1, 37) & self.mod
#         return key
    
#     def encrypt(self, pt: bytes):
#         ct = b''
#         for i in range(0, len(pt), self.BLOCK_SIZE):
#             ct += long_to_bytes(self.X)
#             key = self.get_key_stream()
#             block = pt[i:i+self.BLOCK_SIZE]
#             ct += bytes([block[j] ^ key[j] for j in range(len(block))])
#         return ct
    
#     def decrypt(self, ct: bytes):
#         pt = b''
#         for i in range(0, len(ct), self.BLOCK_SIZE + 8):
#             key = self.get_key_stream()
#             block = ct[i+8:i+8+self.BLOCK_SIZE]
#             pt += bytes([block[j] ^ key[j] for j in range(len(block))])
#         return pt

# def find_initial_states(ct):
#     for s0 in range(0x10000000000000000):
#         for s1 in range(0x10000000000000000):
#             cipher = MyCipher(s0, s1)
#             decrypted_pt = cipher.decrypt(ct)
#             try:
#                 plaintext = unpad(decrypted_pt, 8)
#                 if plaintext.startswith(b'FLAG{'):
#                     return s0, s1, plaintext
#             except ValueError:
#                 continue
#     return None, None, None

# ct = b'"G:F\xfe\x8f\xb0<O\xc0\x91\xc8\xa6\x96\xc5\xf7N\xc7n\xaf8\x1c,\xcb\xebY<z\xd7\xd8\xc0-\x08\x8d\xe9\x9e\xd8\xa51\xa8\xfbp\x8f\xd4\x13\xf5m\x8f\x02\xa3\xa9\x9e\xb7\xbb\xaf\xbd\xb9\xdf&Y3\xf3\x80\xb8'

# s0, s1, plaintext = find_initial_states(ct)

# if s0 is not None and s1 is not None:
#     print(s0, s1)
#     print(plaintext)
# else:
#     print('Fail')

from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.Padding import pad, unpad

def rotl(x, y):
    x &= 0xFFFFFFFFFFFFFFFF
    return ((x << y) | (x >> (64 - y))) & 0xFFFFFFFFFFFFFFFF

class MyCipher:
    def __init__(self, s0, s1):
        self.X = s0
        self.Y = s1
        self.mod = 0xFFFFFFFFFFFFFFFF
        self.BLOCK_SIZE = 8
    
    def get_key_stream(self):
        s0 = self.X
        s1 = self.Y
        sum = (s0 + s1) & self.mod
        s1 ^= s0
        key = []
        for _ in range(8):
            key.append(sum & 0xFF)
            sum >>= 8
        
        self.X = (rotl(s0, 24) ^ s1 ^ (s1 << 16)) & self.mod
        self.Y = rotl(s1, 37) & self.mod
        return key
    
    def encrypt(self, pt: bytes):
        ct = b''
        for i in range(0, len(pt), self.BLOCK_SIZE):
            ct += long_to_bytes(self.X)
            key = self.get_key_stream()
            block = pt[i:i+self.BLOCK_SIZE]
            ct += bytes([block[j] ^ key[j] for j in range(len(block))])
        return ct
    
    def decrypt(self, ct: bytes):
        pt = b''
        for i in range(0, len(ct), self.BLOCK_SIZE + 8):
            key = self.get_key_stream()
            block = ct[i+8:i+8+self.BLOCK_SIZE]
            pt += bytes([block[j] ^ key[j] for j in range(len(block))])
        return pt

ct = b'"G:F\xfe\x8f\xb0<O\xc0\x91\xc8\xa6\x96\xc5\xf7N\xc7n\xaf8\x1c,\xcb\xebY<z\xd7\xd8\xc0-\x08\x8d\xe9\x9e\xd8\xa51\xa8\xfbp\x8f\xd4\x13\xf5m\x8f\x02\xa3\xa9\x9e\xb7\xbb\xaf\xbd\xb9\xdf&Y3\xf3\x80\xb8'
known_plaintext = b'FLAG{' + b'*'*19 + b'}'

def derive_keystream(ct, known_plaintext):
    keystream = []
    for i in range(len(known_plaintext)):
        keystream.append(ct[8 + i] ^ known_plaintext[i])
    return keystream

keystream = derive_keystream(ct, known_plaintext)

def decrypt_with_keystream(ct, keystream):
    pt = b''
    keystream_len = len(keystream)
    for i in range(0, len(ct), keystream_len + 8):
        block = ct[i+8:i+8+keystream_len]
        pt += bytes([block[j] ^ keystream[j] for j in range(len(block))])
    return pt

decrypted_pt = decrypt_with_keystream(ct, keystream)



plaintext = (decrypted_pt)
print(plaintext)
