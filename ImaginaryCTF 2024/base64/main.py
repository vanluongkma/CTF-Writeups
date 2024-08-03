from Crypto.Util.number import bytes_to_long

q = 64

flag = open("flag.txt", "rb").read()
flag_int = bytes_to_long(flag)

secret_key = []
while flag_int:
    secret_key.append(flag_int % q)
    flag_int //= q

print(f"{secret_key = }")

secret_key = [10, 52, 23, 14, 52, 16, 3, 14, 37, 37, 3, 25, 50, 32, 19, 14, 48, 32, 35, 13, 54, 12, 35, 12, 31, 29, 7, 29, 38, 61, 37, 27, 47, 5, 51, 28, 50, 13, 35, 29, 46, 1, 51, 24, 31, 21, 54, 28, 52, 8, 54, 30, 38, 17, 55, 24, 41, 1]
