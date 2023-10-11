```python3
from Crypto.Util.number import *


m1 = 5 
m2 = 83
m3 = 42
m4 = 89
m5 = 13
a1 = 3
a2 = 67
a3 = 28
a4 = 22
a5 = 0

M = m1*m2*m3*m4*m5
M1 = M//m1
M2 = M//m2
M3 = M//m3
M4 = M//m4
M5 = M//m5

u1 = inverse(M1, m1)
u2 = inverse(M2, m2)
u3 = inverse(M3, m3)
u4 = inverse(M4, m4)
u5 = inverse(M5, m5)


x = (a1*u1*M1 + a2*u2*M2 + a3*u3*M3 + a4*u4*M4 + a5*u5*M5 ) % M
print(x%20166510)
#8610238
```
![image](https://github.com/piropatriot/CTF-Writeups/assets/127461439/c62dac2a-70c4-4029-92fa-d64932555e99)
