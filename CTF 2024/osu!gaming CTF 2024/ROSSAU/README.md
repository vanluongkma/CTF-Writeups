### crypto/ROSSAU

```
My friend really likes sending me hidden messages, something about a public key with n = 5912718291679762008847883587848216166109 and e = 876603837240112836821145245971528442417. What is the name of player with the user ID of the private key exponent? (Wrap with osu{})
```
 - Challenge này yêu cầu ta tính private key **d**
 - Thoáng qua ta thấy e ở đây rất lớn tôi dùng [``wiener attack``](https://en.wikipedia.org/wiki/Wiener%27s_attack)
 - Solution bằng python
```python3
import RSA_owiener
from Crypto.Util.number import*
n = 5912718291679762008847883587848216166109 
e = 876603837240112836821145245971528442417

d = RSA_owiener.attack(e, n)

if d is None:
    print("Failed")
else:
    print(f"{d = }")
# 124493
 ```
 - Khi có private key **d** thì flag chính là tên người dùng trên [osu](https://osu.ppy.sh/) có ID là 124493

![image](https://github.com/luongdv35/CTF-Writeups/assets/127461439/0ada5e6a-c752-410a-97ab-f55ab656b64f)

> FLAG : osu{chocomint}
