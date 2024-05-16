# #!/usr/bin/env python3
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad
# import time

# seed = int(time.time() * 1000) % (10 ** 6)
# def get_random_number():
#     global seed 
#     seed = int(str(seed * seed).zfill(12)[3:9])
#     return seed

# def encrypt(message):
#     key = b''
#     for i in range(8):
#         key += (get_random_number() % (2 ** 16)).to_bytes(2, 'big')
#     print(key)
#     cipher = AES.new(key, AES.MODE_ECB)
#     ciphertext = cipher.encrypt(pad(message, AES.block_size))
#     return ciphertext.hex()

# print("Thanks for using our encryption service! To get the encrypted flag, type 1. To encrypt a message, type 2.")
# while True:
#     print("What would you like to do (1 - get encrypted flag, 2 - encrypt a message)?")
#     user_input = int(input())
#     if(user_input == 1):
#         break

#     print("What is your message?")
#     message = input()
#     print("Here is your encrypted message:", encrypt(message.encode()))


# flag = "0w222222222412412000"
# print("Here is the encrypted flag:", encrypt(flag.encode()))
#!/usr/bin/env python3
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad
# import time


# for i in range(100000, 1000000):
#     ci = bytes.fromhex("d933cffa432e67776942937640eb1a11d933cffa432e67776942937640eb1a11288daebf869a75bb8b82912c01a02126")
#     seed = int(str(i * i).zfill(12)[3:9])
#     key = b''
#     for i in range(8):
#         key += (seed % (2 ** 16)).to_bytes(2, 'big')
#     cipher = AES.new(key, AES.MODE_ECB)
#     ciphertext = cipher.decrypt(ci)
#     print(ciphertext)
#     if b"00000000000000000000000000000000" in ciphertext:
#         print(seed)
#         break
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time

encry= bytes.fromhex("87e8c7f784dce76e910c9966438ae249d8c27a25f46af4122713e156249438729f3e2304c74499250160dcd27c489955")
format = b"utflag"

for i in range(1000, 10000000):
    seed = int(str(i * i).zfill(12)[3:9])
    key = b''
    for j in range(8):
        key += (seed % (2 ** 16)).to_bytes(2, 'big')
        seed = int(str(seed * seed).zfill(12)[3:9])
    cipher = AES.new(key, AES.MODE_ECB)
    msg = (cipher.decrypt(encry))
    if format in msg:
        print(key.hex())
        print(unpad(msg, AES.block_size))
        break

# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
# import time

# # Đoạn mã đã được mã hóa
# encrypted_message_hex = "87e8c7f784dce76e910c9966438ae249d8c27a25f46af4122713e156249438729f3e2304c74499250160dcd27c489955"
# encrypted_message = bytes.fromhex(encrypted_message_hex)


# # Thực hiện tấn công brute force để tìm seed và khóa tương ứng
# for i in range(10000, 1000000):
#     seed = int(str(i * i).zfill(12)[3:9])
#     key = b''
#     for j in range(8):
#         key_part = (seed % (2 ** 16)).to_bytes(2, 'big')
#         key += key_part
#         seed = int(str(seed * seed).zfill(12)[3:9])


#     # Giải mã thông điệp đã được mã hóa bằng khóa hiện tại
#     cipher = AES.new(key, AES.MODE_ECB)
#     decrypted_message = cipher.decrypt(encrypted_message)

#     # Kiểm tra xem thông điệp đã giải mã có chứa thông điệp mục tiêu không
#     if b"utflag{" in decrypted_message:
#         print("Seed found:", i)
#         print("Key:", key.hex())
#         print("Decrypted message:", decrypted_message)
#         break


# Thanks for using our encryption service! To get the encrypted flag, type 1. To encrypt a message, type 2.
# What would you like to do (1 - get encrypted flag, 2 - encrypt a message)?
# 2
# What is your message?
# 00000000000000000000000000000000
# Here is your encrypted message: d933cffa432e67776942937640eb1a11d933cffa432e67776942937640eb1a11288daebf869a75bb8b82912c01a02126
# What would you like to do (1 - get encrypted flag, 2 - encrypt a message)?
# 1
    
# Here is the encrypted flag: 87e8c7f784dce76e910c9966438ae249d8c27a25f46af4122713e156249438729f3e2304c74499250160dcd27c489955