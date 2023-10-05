 - JUST DO IT !

 - ``nc crypto.securinets.tn 8886``
 - [RNGSGB2.py](https://ctf-friendly.securinets.tn/files/836f3a7478c9d2fd45178e4e69cfc736/RNGSGB2.py?token=eyJ1c2VyX2lkIjoxNjUsInRlYW1faWQiOjY2LCJmaWxlX2lkIjo1MX0.ZR5RdA.x1cSUmOGSUGD_0x1AGGbkBiwt9E)

```python3
import random
for i in range(1024):
    print(random.randint(0,2**32),end= " ")
print()

flag=open("flag.txt","rb").read()
for i in range(100):
    if int(input(f"guess my randomness {i}:\n"))==random.randint(0,256):
        print("Nice One keep going")
        continue
    exit(0)
print(flag)
```
