![image](https://github.com/piropatriot/CTF-Writeups/assets/127461439/e6f4a597-d889-4791-ad6d-0b03b7bb59ca)
 - https://flu.xxx/challenges/15
 - Tôi chú ý đến ``data2`` và ``data3``
```python3
        print("You know the moment when you have this special number that gives you luck? Great cause I forgot mine")
        data2=input()
        print("I also had a second lucky number, but for some reason I don't remember it either :(")
        data3=input()
```
- Để qua được 3 điều kiện if thì
```
t <= 42
20000 <= s <= 150000000000
```
- Tiếp đó dể ``sent = True`` thì ``isPrime(n=2**t-1) = True``
- Và qua vòng for cuối thì ``number=(2**u)*(2**(t)-1)`` Là số hoàn hảo (u = t-1) nghĩa là t cũng phải là số nguyên tố
- [Script](https://github.com/piropatriot/CTF-Writeups/blob/main/Hack.lu%20CTF%202023/Crypto/Lucky%20Numbers/solved.py)
> FLAG : flag{luck_0n_fr1d4y_th3_13th?}
