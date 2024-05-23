# from sympy.ntheory.residue_ntheory import discrete_log
# a = 15012705211963716478
# b = 7577241659616393293
# A = 15822795117370428541
# g = 2
# p = 17579313417490987469
# print(discrete_log(p,A, g))

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# key =(b"1234561234561234")
# # flag = pad(open("flag.txt", "rb").read(), 16)
# flag = bytes.fromhex("3035255761e31a384513ec79400596b8")
# cipher = AES.new(key, AES.MODE_ECB)
# print(cipher.decrypt(flag))
with open("key1.txt", "r") as f:
    for i in range(18):
        key = (f.readline().encode().strip())

        flag = bytes.fromhex("ed05f1440f3ae5309a3125a91dfb0edef306e1a64d1c5f7d8cea88cdb7a0d7d66bb36860082a291138b48c5a6344c1ab")
        cipher = AES.new(key, AES.MODE_ECB)
        print(cipher.decrypt(flag))