## crypto/no-dorchadas

```python3
from hashlib import md5
from secret import flag, secret_slider
from base64 import b64encode, b64decode

assert len(secret_slider) == 244
dorchadas_slider = b"0,328,33297,6,0,B|48:323|61:274|61:274|45:207|45:207|63:169|103:169|103:169|249:199|249:199|215:214|205:254,1,450.000017166138,6|6,1:1|2:1,0:0:0:0:"

def sign(beatmap):
    hsh = md5(secret_slider + beatmap)
    return hsh.hexdigest()

def verify(beatmap, signature):
    return md5(secret_slider + beatmap).hexdigest() == signature

def has_dorchadas(beatmap):
    return dorchadas_slider in beatmap

MENU = """
--------------------------
| [1] Sign a beatmap     |
| [2] Verify a beatmap   |
--------------------------"""

def main():
    print("Welcome to the osu! Beatmap Signer")
    while True:
        print(MENU)
        try:
            option = input("Enter your option: ")
            if option == "1":
                beatmap = b64decode(input("Enter your beatmap in base64: "))
                if has_dorchadas(beatmap):
                    print("I won't sign anything with a dorchadas slider in it >:(")
                else:
                    signature = sign(beatmap)
                    print("Okay, I've signed that for you: " + signature)
            elif option == "2":
                beatmap = b64decode(input("Enter your beatmap in base64: "))
                signature = input("Enter your signature for that beatmap: ")
                if verify(beatmap, signature) and has_dorchadas(beatmap):
                    print("How did you add that dorchadas slider?? Anyway, here's a flag: " + flag)
                elif verify(beatmap, signature):
                    print("Signature is valid!")
                else:
                    print("Signature is invalid :(")
        except:
            print("An error occurred!")
            exit(-1)

main()
```
 - Sau khi đọc đoạn code tôi cần phải bypass qua điều kiện

![image](https://github.com/luongdv35/CTF-Writeups/assets/127461439/e692c10c-bdc3-48f0-b81d-eec2475675d1)

 - Tôi đã tìm lấy cách tấn công của hash để giải quyết nó

 - Solution demo

```
patriot@Nitro:~$ nc chal.osugaming.lol 9727
proof of work:
curl -sSfL https://pwn.red/pow | sh -s s.AAAH0A==.taQ4GJTgw+Sq7D/bDsUTjA==
solution: s.JMtrthv2gE8n6PnGKXRLrUfukJyeyu8uBeEsOt573M+IQpIl3h1nllaY+Xqi89WrdvFRyMqXP4mzpbWR6tssRaLXUqNdqOih0hBUdmmpDmWR76GnAEXTToI1CHB0jGiJrz88kASvOPjv8FeLjyb2fpGFwH4sQd4htZbCrckFKjhpf22aIT7zaXLzrhEt90OgYtc6TMgdbeZAO48zULXQ2A==
Welcome to the osu! Beatmap Signer

--------------------------
| [1] Sign a beatmap     |
| [2] Verify a beatmap   |
--------------------------
Enter your option: 1
Enter your beatmap in base64: bHVvbmc==
Okay, I've signed that for you: b2946d690f35b9d33793fd96f2e2d74c

--------------------------
| [1] Sign a beatmap     |
| [2] Verify a beatmap   |
--------------------------
Enter your option: 2
Enter your beatmap in base64: bHVvbmeAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADIBwAAAAAAADAsMzI4LDMzMjk3LDYsMCxCfDQ4OjMyM3w2MToyNzR8NjE6Mjc0fDQ1OjIwN3w0NToyMDd8NjM6MTY5fDEwMzoxNjl8MTAzOjE2OXwyNDk6MTk5fDI0OToxOTl8MjE1OjIxNHwyMDU6MjU0LDEsNDUwLjAwMDAxNzE2NjEzOCw2fDYsMToxfDI6MSwwOjA6MDowOg==
Enter your signature for that beatmap: 1666d911ad437cbc4fe02ffe5ba41a2a
How did you add that dorchadas slider?? Anyway, here's a flag: osu{s3cr3t_sl1d3r_i5_th3_burp_5l1d3r_fr0m_Feiri's_Fake_Life}

--------------------------
| [1] Sign a beatmap     |
| [2] Verify a beatmap   |
--------------------------
Enter your option:
```
> FLAG :  osu{s3cr3t_sl1d3r_i5_th3_burp_5l1d3r_fr0m_Feiri's_Fake_Life}
