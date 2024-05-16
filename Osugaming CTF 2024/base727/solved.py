import binascii

flag = "06c3abc49dc4b443ca9d65c8b0c386c4b0c99fc798c2bdc5bccb94c68c37c296ca9ac29ac790c4af7bc585c59d"

def decode_base_727(string):
    de_value = 0

    for char in string:
        de_value = de_value * 727 + ord(char)

    de_string = ""
    while de_value > 0:
        de_string = chr(de_value % 256) + de_string
        de_value //= 256

    return de_string

de_string = decode_base_727(binascii.unhexlify(flag).decode())
print(de_string)
