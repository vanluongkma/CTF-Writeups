# # # Patch deprecation warnings
# # sage.structure.element.is_Matrix = lambda z: isinstance(z, sage.structure.element.Matrix)
# # # See README.md for this package
# from sagemath import *
# from sage.all import *
# # from vector_bundle import *
# from string import printable
# from tqdm import tqdm
# import 

# password = ''.join(choice(printable) for _ in range(15)).encode()

# p = 66036476783091383193200018291948785097
# F = GF(p)
# K.<x> = FunctionField(F)
# L = VectorBundle(K, -x.zeros()[0].divisor()) # L = O(-1)

# V = L.tensor_power(password[0])
# for b in tqdm(password[1:]):
#     V = V.direct_sum(L.tensor_power(b))

# L = L.dual() # L = O(1)
# out = [
#     len(V.tensor_product(L.tensor_power(m)).h0())
#     for m in tqdm(printable.encode())
# ]

# print(out)


# from Crypto.Cipher import AES
# from hashlib import sha256
# from flag import flag
# flag += bytes((16-len(flag)) % 16)

# key = sha256(bytes(sorted(password))).digest()[:16]
# aes = AES.new(key, AES.MODE_ECB)
# enc = aes.encrypt(flag)
# print('enc:', enc.hex())

# # [49, 52, 55, 58, 62, 66, 71, 76, 81, 86, 431, 444, 457, 470, 484, 498, 512, 526, 540, 554, 568, 582, 596, 610, 625, 640, 655, 670, 685, 700, 715, 730, 745, 760, 775, 790, 134, 141, 148, 155, 162, 169, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 257, 266, 275, 284, 293, 303, 313, 323, 333, 345, 24, 25, 26, 27, 28, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 91, 96, 101, 106, 113, 120, 127, 357, 369, 381, 393, 405, 418, 805, 820, 835, 850, 23, 0, 1, 4, 2, 3]
# # enc: 5f0a8761f98748422d97f60f11d8590d56e1462409a677fbf52259b084b8a724


import itertools
from string import printable
from hashlib import sha256
from Crypto.Cipher import AES
from tqdm import tqdm

printable_chars = ''.join([chr(i) for i in range(32, 40)])
enc_flag = bytes.fromhex('5f0a8761f98748422d97f60f11d8590d56e1462409a677fbf52259b084b8a724')

for password_tuple in tqdm(itertools.product(printable_chars, repeat=15)):
    print(password_tuple)
    password = ''.join(password_tuple).encode()
    key = sha256(bytes(sorted(password))).digest()[:16]
    aes = AES.new(key, AES.MODE_ECB)
    decrypted_flag = aes.decrypt(enc_flag)
    
    if b"ideak" in decrypted_flag:
        print("Key:", key)
        print("Decrypted Flag:", decrypted_flag)
        print("Password:", password)
        break
