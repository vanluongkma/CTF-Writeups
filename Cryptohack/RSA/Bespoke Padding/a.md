Hãy để ý hàm ``pad()``

```python
def pad(self, flag):
    m = bytes_to_long(flag)
    a = random.randint(2, self.N)
    b = random.randint(2, self.N)
    return (a, b), a*m+b
```
Khi hàm pad được thực thi ``pad_msg = a * m + b``

Khi đó 

$$enc = (a * m + b)^e \mod N$$

Nếu ta get 2 lần từ server thì sao

$$
\begin{cases}
   enc_1 = (a_1 * m + b_1)^e \mod N \\
   enc_2 = (a_2 * m + b_2)^e \mod N
\end{cases}
$$

Ta nhận thấy trong Rsa có [Franklin–Reiter related-message attack](https://en.wikipedia.org/wiki/Coppersmith%27s_attack) thỏa mãn phương trình trên 

[Đọc thêm](https://crypto.stackexchange.com/questions/30884/help-understanding-basic-franklin-reiter-related-message-attack) để hiểu hơn.

$$
\begin{cases}
   g_1 = (a_1 * m + b_1)^e - enc_1 = 0 \mod N \\
   g_2 = (a_2 * m + b_2)^e - enc_2 = \mod N
\end{cases}
$$

Nhận thấy 2 pt trên đều có chung nghiệm m nên ta sẽ sử dụng $gcd(g_1, g_2)$ trong vành $Z_n$ để tìm m



$$a * m + b$$ 
$$\Longrightarrow m = \frac{-a}{b}$$

``solved.sage``
```python
from Crypto.Util.number import *
from pwn import *
from json import *

e = 11

f = connect('socket.cryptohack.org', 13386)
f.recv()

f.sendline(dumps({'option': 'get_flag'}))
g1 = loads(f.recvuntil('\n'))

f.sendline(dumps({'option': 'get_flag'}))
g2 = loads(f.recvuntil('\n'))


enc_1 = g1["encrypted_flag"]
enc_2 = g2["encrypted_flag"]

a_1, b_1 = g1["padding"]
a_2, b_2 = g2["padding"]

n_1 = g1["modulus"]
n_2 = g2["modulus"]

assert n_1 == n_2
print("challenge has been Franklin-Reiter attack ")
print(a_1, a_2, b_1, b_2, enc_1, enc_2)

p.<x> = PolynomialRing(Zmod(n_1))

g1 = (a_1 * x + b_1) ** e - enc_1
g2 = (a_2 * x + b_2) ** e - enc_2

def gcd(a,b):
    while b:
        a, b = b, a % b
    return a.monic()


m = long_to_bytes(int(-gcd(g1, g2).coefficients()[0]))
print(m)
```