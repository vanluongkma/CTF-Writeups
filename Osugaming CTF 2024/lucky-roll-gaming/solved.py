from Crypto.Util.number import inverse
from math import floor
from Crypto.Cipher import AES
from sage.all import *

p = 4420073644184861649599
a = 1144993629389611207194
b = 3504184699413397958941
out = [39, 47, 95, 1, 77, 89, 77, 70, 99, 23, 44, 38, 87, 34, 99, 42, 10, 67, 24, 3, 2, 80, 26, 87, 91, 86, 1, 71, 59, 97, 69, 31, 17, 91, 73, 78, 43, 18, 15, 46, 22, 68, 98, 60, 98, 17, 53, 13, 6, 13, 19, 50, 73, 44, 7, 44, 3, 5, 80, 26, 10, 55, 27, 47, 72, 80, 53, 2, 40, 64, 55, 6]
encrypted = "34daaa9f7773d7ea4d5f96ef3dab1bbf5584ecec9f0542bbee0c92130721d925f40b175e50587196874e14332460257b"

size = len(out)
B = 2 ** 66
inv_100 = inverse(100, p)
inv_a1 = inverse(a - 1, p)

M = matrix(QQ, size + 2, size + 2)
print(M)
for i in range(size):
    M[i, i] = p
print(M)
for i in range(size):
    M[size, i] = pow(a, i + 1, p) * inv_100 % p
    M[size + 1, i] = (out[i] * inv_100 - b * (a ** (i + 1) - 1) * inv_a1 * inv_100) % p
M[size, size] = QQ(B/p)
M[size + 1, size + 1] = B
A = M.LLL()
# for i in range(size + 2):
#     if A[i, size + 1] == B or A[i, size + 1] == -B:
#         print(i, A[i, size + 1], A[i, size])
seed = (53765932436314634507284602211246379368448 * inverse(B, p)) % p

def lcg(s, a, b, p):
    return (a * s + b) % p

def get_roll():
    global seed
    seed = lcg(seed, a, b, p)
    return seed % 100


for i in range(floor(72.7)):
    num = get_roll()
    assert num == out[i]

key = bytes([get_roll() for _ in range(16)])
iv = bytes([get_roll() for _ in range(16)])
cipher = AES.new(key, AES.MODE_CBC, iv)
print(cipher.decrypt(bytes.fromhex(encrypted)))