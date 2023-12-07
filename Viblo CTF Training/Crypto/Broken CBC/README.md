- ![image](https://github.com/piropatriot/CTF-Writeups/assets/127461439/7be07837-e89a-46d5-81bd-60aff2dc6ec2)
- Mô hình ``AES-CBC``
- Chúng ta gửi ``Plantext = b"\x00" *16`` => Đầu vào sẽ là ``IV`` vì ``IV ^ 0 = IV``
- Khi đó Challenge sẽ quay về chế độ ``AES-ECB``
- ![image](https://github.com/piropatriot/CTF-Writeups/assets/127461439/a4ba3c7b-ad69-41f7-8718-451b3f92fcf5)
- Giờ đây ta Decrypt theo ``AES-ECB`` để tìm lại ``IV`` chính và Brute Force 2 kí tự của key
-  Kết hợp đưa ``key`` và ``IV`` vào Decrypt AES-CBC cho đến khi đầu ra xuât hiện format ``Flag``
- Solution : [solved.py](https://github.com/piropatriot/CTF-Writeups/blob/main/Viblo%20CTF%20Training/Crypto/Broken%20CBC/solved.py)
> Flag{51a21a1d80eb8397e62fd1e8e7f0e839}
