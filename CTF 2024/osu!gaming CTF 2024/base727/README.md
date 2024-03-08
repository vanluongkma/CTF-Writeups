### crypto/base 727
```python3
import binascii

flag = open('flag.txt').read()

def encode_base_727(string):
    base = 727
    encoded_value = 0

    for char in string:
        encoded_value = encoded_value * 256 + ord(char)

    encoded_string = ""
    while encoded_value > 0:
        encoded_string = chr(encoded_value % base) + encoded_string
        encoded_value //= base

    return encoded_string

encoded_string = encode_base_727(flag)
print(binascii.hexlify(encoded_string.encode()))
# 06c3abc49dc4b443ca9d65c8b0c386c4b0c99fc798c2bdc5bccb94c68c37c296ca9ac29ac790c4af7bc585c59d
```
 - Như tiêu đề của challenge, bài này mã hóa rất đơn giản ta chỉ cần đảo ngược lại quá trình mã hóa là sẽ lấy được flag.
 - Solution bằng python
```python3
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
```
> FLAG : osu{wysiwysiwysiywsywiwywsi}
