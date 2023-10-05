
 - chuck norris doesnt have time to predict the next appocalypse its your time to shine

```crypto.securinets.tn 8889```

```python3
import random
random.seed(random.randint(0,2**128)%10)

flag=open("flag.txt","rb").read()
for i in range(100):
    if int(input(f"guess my randomness {i}:\n"))==random.randint(0,256):
        print("Nice One keep going")
        continue
    exit(0)
print(flag)
```
