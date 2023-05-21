# RSA1
```python
from Crypto.Util.number import *

n = 287838647563564518717519107521814079281
e = 7
c = 258476617615202392748150555415953446503

#factor n
p = 18413880828441662521
q = 15631612382272805561
phi = (p-1)*(q-1)
d = inverse(e,phi)
m =pow(c,d,n)


flag =long_to_bytes(m).decode()
print(flag)

#byuctf{too_smol}
```
