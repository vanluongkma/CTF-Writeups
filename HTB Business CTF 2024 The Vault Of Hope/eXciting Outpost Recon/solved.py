# from pwn import *
# dataa = bytes.fromhex("fd94e649fc4c898297f2acd4cb6661d5b69c5bb51448687f60c7531a97a0e683072bbd92adc5a871e9ab3c188741948e20ef9afe8bcc601555c29fa6b61de710a718571c09e89027413e2d94fd3126300eff106e2e4d0d4f7dc8744827731dc6ee587a982f4599a2dec253743c02b9ae1c3847a810778a20d1dff34a2c69b11c06015a8212d242ef807edbf888f56943065d730a703e27fa3bbb2f1309835469a3e0c8ded7d676ddb663fdb6508db9599018cb4049b00a5ba1690ca205e64ddc29fd74a6969b7dead69a7341ff4f32a3f09c349d92e0b21737f26a85bfa2a10d")


# fm = b"Great and Noble Leader of the Tariaki"


# a = xor((dataa), fm )

# print(a)

# k = b'\xba\xe6\x83(\x88l\xe8\xec\xf3\xd2\xe2\xbb\xa9\n\x04\xf5\xfa\xf9:\xd1q:H\x10\x06\xe7\'r\xf2\x80\xb2\xe2uB\xdc\xf9\xc4'

# print(xor(dataa, k))

# from hashlib import sha256
# import os

# LENGTH = 32

# def decrypt_data(encrypted, k):
#     decrypted = b''

#     for i in range(0, len(encrypted), LENGTH):
#         chunk = encrypted[i:i+LENGTH]

#         for a, b in zip(chunk, k):
#             decrypted += bytes([a ^ b])

#         k = sha256(k).digest()

#     return decrypted.rstrip(b'\x00')

# # Giả sử bạn có khóa đã sử dụng để mã hóa (thay thế os.urandom(32) bằng khóa thực tế)
# key = os.urandom(32)  # Replace this with the actual key used during encryption

# # Đọc dữ liệu đã mã hóa từ file
# with open('output.txt', 'r') as f:
#     enc_hex = f.read()
#     encrypted = bytes.fromhex(enc_hex)

# # Giải mã dữ liệu đã mã hóa
# decrypted = decrypt_data(encrypted, key)

# # Kiểm tra định dạng flag "HTB{}"
# decrypted_str = decrypted


# print(decrypted_str)


from hashlib import sha256
import os

LENGTH = 32

def decrypt_data(encrypted, k):
    decrypted = b''

    for i in range(0, len(encrypted), LENGTH):
        chunk = encrypted[i:i+LENGTH]

        for a, b in zip(chunk, k):
            decrypted += bytes([a ^ b])

        k = sha256(k).digest()

    return decrypted.rstrip(b'\x00')

# Đặt khóa sử dụng trong quá trình mã hóa (thay thế bằng khóa thực tế)
key = os.urandom(32)  # Thay thế khóa này bằng khóa thực tế đã sử dụng khi mã hóa

# Đọc dữ liệu đã mã hóa từ file
with open('output.txt', 'r') as f:
    enc_hex = f.read()
    encrypted = bytes.fromhex(enc_hex)

# Giải mã dữ liệu đã mã hóa
decrypted = decrypt_data(encrypted, key)

# Kiểm tra xem dữ liệu giải mã có bắt đầu bằng chuỗi yêu cầu hay không
decrypted_str = decrypted

# In dữ liệu giải mã
print(decrypted_str)