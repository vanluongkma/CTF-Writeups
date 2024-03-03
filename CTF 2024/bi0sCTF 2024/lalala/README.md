## lalala
```python3
from random import randint
from re import search

flag = "bi0sctf{%s}" % f"{randint(2**39, 2**40):x}"

p = random_prime(2**1024)
unknowns = [randint(0, 2**32) for _ in range(10)]
unknowns = [f + i - (i%1000)  for i, f in zip(unknowns, search("{(.*)}", flag).group(1).encode())]

output = []
for _ in range(100):
    aa = [randint(0, 2**1024) for _ in range(1000)]
    bb = [randint(0, 9) for _ in range(1000)]
    cc = [randint(0, 9) for _ in range(1000)]
    output.append(aa)
    output.append(bb)
    output.append(cc)
    output.append(sum([a + unknowns[b]^2 * unknowns[c]^3 for a, b, c in zip(aa, bb, cc)]) % p)

print(f"{p = }")
print(f"{output = }")
```
 - Bài này flag được ẩn trong **unknowns** bao gồm 10 giá trị với 100 vòng for :
 - Ta hãy để ý
```python3
output.append(sum([a + unknowns[b]^2 * unknowns[c]^3 for a, b, c in zip(aa, bb, cc)]) % p)
```
 - Ở vòng for đầu tiên ta sẽ có  coefficient $coeff_i$  là: $coeff_0 * unknown_{b0}^2 * unknown_{c0}^3 + coeff_0 * unknown_{b1}^2 * unknown_{c1}^3 + coeff_0 * unknown_{b2}^2 * unknown_{c2}^3 + ... + coeff_0 * unknown_{b9}^2 * unknown_{c9}^3 + sum(aa_0) = output_0 $
 - Với $b, c \in [0,9]$
 - Ta sẽ dựng ma trận như sau:


$$
\begin{equation*}
    \begin{bmatrix}
        coeff_0.b_0.c_0 &amp; coeff_0.b_0.c_1 &amp; ... &amp; coeff_0.b_9.c_9 \\
        coeff_1.b_0.c_0 &amp; coeff_1.b_0.c_1 &amp; ... &amp; coeff_1.b_9.c_9 \\
        \vdots &amp; \vdots \\
    coeff_{99}.b_0.c_0 &amp; coeff_{99}.b_0.c_1 &amp; ... &amp; coeff_{99}.b_9.c_9 \\
    \end{bmatrix}
    =
    \begin{bmatrix}
         output_0 - sum(aa_0) \\
        output_1 - sum(aa_1) \\
        \vdots  \\
        output_{99} - sum(aa_{99})
    \end{bmatrix}
\end{equation*}
$$
 - Giải ma trận bằng sage ta thu được 100 nghiệm của  $unknown_0^2 * unknown_0^3$ đến $unknown_9^2 * unknown_9^3$
 - Thu được 10 giá trị của $unknown_0^5$ đến $unknown_9^5$ tôi dùng **nth_root(5)** và chia dư cho 1000 để khôi phục lại flag.
 - Solution bằng python
```python3
from sage.all import *

p = ...
output = ...

m = []
y = []
vars = [[i, j] for i in range(10) for j in range(10)]

for i in range(0, len(output), 4):
    aa = output[i]
    bb = output[i+1]
    cc = output[i+2]
    rs = output[i+3]
    
    coeffs = [0]*100

    # sum([aa[i] + unknowns[bb[i]]^2 + unknowns[cc[i]]^3 for i in range(1000)])
    sum = 0

    for j in range(1000):
        sum = (sum + aa[j]) % p
        temp = [bb[j], cc[j]]
        coeffs[vars.index(temp)] += 1

    y.append((rs-sum) % p)
    row = coeffs
    m.append(row)

l = len(m)
m = Matrix(GF(p), m)
y = vector(GF(p), y)

ans = list(m.solve_right(y))

flag = []
for i in range(100):
    try:
        u = ans[i].nth_root(5)
        flag.append(u)
    except:
        continue

print("".join([bytes([c%1000]).decode() for c in flag]))
```
