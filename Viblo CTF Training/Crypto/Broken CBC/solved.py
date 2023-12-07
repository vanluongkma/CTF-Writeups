from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pwn import *


io = connect("172.104.49.143", 1582)
io.recvline()
io.sendlineafter("> ", b"1")
io.sendlineafter("message:", b"\x00" *16)
io.recvuntil("\n")

cipher = "8715affda71f33d3f83babe7486185a17c635ef1c09f9618f40b0bf1f69a58d2ae556860bca750de540cbbb7a3404c52"
key = "44b9c1737b3f6c{}{}" 
encIV = "4ba0476b7825d1c260acbcdf4abeea8a" 
b = ''.join([chr(i) for i in range(32, 127)])

for i in b:
    for j in b:
        Key = key.format(i, j).encode()
        aesecb = AES.new(Key, AES.MODE_ECB)
        IV = aesecb.decrypt(bytes.fromhex(encIV))  
        plant = AES.new(Key, AES.MODE_CBC, iv = IV)
        res = plant.decrypt(bytes.fromhex(cipher))
        if b'Flag' in res:
            print(IV)
            print(Key)
            print(res)
            break
