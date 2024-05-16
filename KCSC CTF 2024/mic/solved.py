# from PIL import Image
# import numpy as np
# import galois
# GF256 = galois.GF(2**8)

# img = Image.open('qr_flag_encrypt.png')
# pixels = img.load()
# print(pixels)
# width, height = img.size
# print(width, height)
# M = GF256(np.random.randint(0, 256, size=(3, 3), dtype=np.uint8))

# # scan full height -> weight
# for x in range(width):
#     for y in range(0,height,3):
#         A = GF256([pixels[x, y], pixels[x, y+1], pixels[x, y+2]])
#         print(f"{A = }")
#         M = np.add(A, M)
#         pixels[x, y], pixels[x, y+1], pixels[x, y+2] = [tuple([int(i) for i in j]) for j in M]

# # img.save('qr_flag_encrypt.png')

# from PIL import Image
# import numpy as np
# import galois
# GF256 = galois.GF(2**8)

# img = Image.open('qr_flag_encrypt.png')
# pixels = img.load()
# width, height = img.size

# M_inv = np.linalg.inv(M)  # Inverse of the random matrix M

# # Scan full height -> weight
# for x in range(width):
#     for y in range(0, height, 3):
#         A = GF256([pixels[x, y], pixels[x, y+1], pixels[x, y+2]])
#         A_decrypted = np.subtract(A, M_inv)  # Decrypt each pixel value
#         pixels[x, y], pixels[x, y+1], pixels[x, y+2] = [tuple([int(i) for i in j]) for j in A_decrypted]

# img.save('qr_flag_decrypt.png')

import numpy as np
from PIL import Image
import galois
from sage.all import *

GF256 = galois.GF(2**8)

def decrypt_image(img, M):
    pixels = img.load()
    width, height = img.size
    
    M_inv = np.linalg.inv(M)

    for x in range(width):
        for y in range(0, height, 3):
            A = GF256([pixels[x, y], pixels[x, y+1], pixels[x, y+2]])
            A_decrypted = np.subtract(A, M_inv)
            pixels[x, y], pixels[x, y+1], pixels[x, y+2] = [tuple([int(i) for i in j]) for j in A_decrypted]

    return img

def brute_force_decrypt(image_path):
    img = Image.open(image_path)
    width, height = img.size

    for a11 in range(256):
        for a12 in range(256):
            for a13 in range(256):
                for a21 in range(256):
                    for a22 in range(256):
                        for a23 in range(256):
                            for a31 in range(256):
                                for a32 in range(256):
                                    for a33 in range(256):
                                        M = np.array([[a11, a12, a13],
                                                      [a21, a22, a23],
                                                      [a31, a32, a33]])
                                        decrypted_img = decrypt_image(img.copy(), M)
                                        print(decrypted_img)
    return None

decryp_image = brute_force_decrypt('qr_flag_encrypt.png')
if decryp_image:
    decryp_image.save('decrypted_image.png')
    print("D")
else:
    print("U")
