# #!/usr/bin/env python3

# from hashlib import sha256
# from random import choices

# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad


# pt = "4145535f4145535f4145535f41455321"
# ct = "edb43249be0d7a4620b9b876315eb430"
# enc_flag = "e5218894e05e14eb7cc27dc2aeed10245bfa4426489125a55e82a3d81a15d18afd152d6c51a7024f05e15e1527afa84b"

# FLAG = b"KCSC{abc123}"

# chars = b'crew_AES*4=$!?'
# L = 3

# w, x, y, z = (
#     bytes(choices(chars, k=L)),
#     bytes(choices(chars, k=L)),
#     bytes(choices(chars, k=L)),
#     bytes(choices(chars, k=L)),
# )

# k1 = sha256(w).digest()
# k2 = sha256(x).digest()
# k3 = sha256(y).digest()
# k4 = sha256(z).digest()

# print(w.decode(), x.decode(), y.decode(), z.decode())

# pt = b'AES_AES_AES_AES!'
# ct = AES.new(k4, AES.MODE_ECB).encrypt(
#          AES.new(k3, AES.MODE_ECB).encrypt(
#              AES.new(k2, AES.MODE_ECB).encrypt(
#                  AES.new(k1, AES.MODE_ECB).encrypt(
#                      pt
#                  )
#              )
#          )
#      )

# key = sha256(w + x + y + z).digest()
# enc_flag = AES.new(key, AES.MODE_ECB).encrypt(pad(FLAG, AES.block_size))


# print(f'pt = {pt.hex()}\nct = {ct.hex()}\nenc_flag = {enc_flag.hex()}')

from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

pt_hex = "4145535f4145535f4145535f41455321"
ct_hex = "edb43249be0d7a4620b9b876315eb430"
enc_flag_hex = "e5218894e05e14eb7cc27dc2aeed10245bfa4426489125a55e82a3d81a15d18afd152d6c51a7024f05e15e1527afa84b"

pt = bytes.fromhex(pt_hex)
ct = bytes.fromhex(ct_hex)
enc_flag = bytes.fromhex(enc_flag_hex)

chars = b'crew_AES*4=$!?'
L = 3

def find_wxyz():
    for w in [bytes([a, b, c]) for a in chars for b in chars for c in chars]:
        for x in [bytes([a, b, c]) for a in chars for b in chars for c in chars]:
            for y in [bytes([a, b, c]) for a in chars for b in chars for c in chars]:
                for z in [bytes([a, b, c]) for a in chars for b in chars for c in chars]:
                    k1 = sha256(w).digest()
                    k2 = sha256(x).digest()
                    k3 = sha256(y).digest()
                    k4 = sha256(z).digest()
                    print(w)
                    
                    try:
                        decipher = AES.new(k4, AES.MODE_ECB).decrypt(
                            AES.new(k3, AES.MODE_ECB).decrypt(
                                AES.new(k2, AES.MODE_ECB).decrypt(
                                    AES.new(k1, AES.MODE_ECB).decrypt(ct)
                                )
                            )
                        )
                        if decipher == pt:
                            return w, x, y, z
                    except Exception:
                        continue
    return None, None, None, None

w, x, y, z = find_wxyz()

if w and x and y and z:
    print(f"Found w: {w.decode()}, x: {x.decode()}, y: {y.decode()}, z: {z.decode()}")
    
    key = sha256(w + x + y + z).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    flag = unpad(cipher.decrypt(enc_flag), AES.block_size)
    print(f"Flag: {flag.decode()}")
else:
    print("not found")
