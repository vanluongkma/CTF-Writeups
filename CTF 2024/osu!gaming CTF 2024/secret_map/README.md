## crypto/secret_map

![image](https://github.com/luongdv35/CTF-Writeups/assets/127461439/91ef3525-9b6f-47b2-8fda-52000003c427)

 - Thấy rằng, challenge cho 1 file [``Alfakyun. - KING.osz``](https://ctf.osugaming.lol/uploads/2cdc85778a40b176f4541bc782650cf933dd9997083d69e928cd9b4b85e0c189/Alfakyun.%20-%20KING.osz)
 - Khi mở ra thì ta thấy nó là 1 file game của osugaming, file game
 - Nhưng chúng tôi đã cẩn thận hơn sử dụng $binwalk$ để tìm các file ẳn trong đó

 ![image](https://github.com/luongdv35/CTF-Writeups/assets/127461439/346ead55-b5d7-4d58-9367-37c0ca6b476a)

 - Khi đó chúng tôi tiến hành convert **Alfakyun. - KING.osz** **=>** **Alfakyun. - KING.zip**

![image](https://github.com/luongdv35/CTF-Writeups/assets/127461439/f2d7abf4-5904-4ff9-a983-f16fd0c29c17)

 - Mở file python **enc.py** tôi nghi ngờ flag được giấu trong đó
```python3
import os

xor_key = os.urandom(16)

with open("flag.osu", 'rb') as f:
    plaintext = f.read()

encrypted_data = bytes([plaintext[i] ^ xor_key[i % len(xor_key)] for i in range(len(plaintext))])

with open("flag.osu.enc", 'wb') as f:
    f.write(encrypted_data)
```

 - Đây chỉ là phép xor bình thường
 - Tôi giải mã file như sau
```python3
from pwn import xor
data = b"osu file format v14"
data = (data[:16])

with open("flag.osu.enc","rb") as file:
    enc = file.read()
key = b'\xd1B,s\xdc\xf0\xcf\xd3\x11\xbb\xae;\xef2I\x97'
x = bytes([enc[i] ^ key[i % len(key)] for i in range(len(enc))])

print(x.hex())
```
 - Sau khi decrypt ra tôi thấy một đem so sánh với file ``Alfakyun. - KING (QuintecX) [ryuk eyeka's easy].osu``
 - File gốc:

   ![image](https://github.com/luongdv35/CTF-Writeups/assets/127461439/2820a2fd-ff81-47b5-b276-817168640524)
 
 - File sau khi decrypt
 
   ![image](https://github.com/luongdv35/CTF-Writeups/assets/127461439/c19b8b9c-2031-4522-852f-ad4baf6835d5)

- Tôi tiến hành copy file sau khi decrypt và thay file cho file ``Alfakyun. - KING (QuintecX) [ryuk eyeka's easy].osu`` và đổi đuôi folder thành ``.osz``

- Khi mở và chơi game ta sẽ có flag
> osu{xor_xor_xor_by_frums}
