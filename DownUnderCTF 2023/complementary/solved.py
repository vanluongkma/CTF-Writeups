from Crypto.Util.number import long_to_bytes
from sympy import divisors
n = 6954494065942554678316751997792528753841173212407363342283423753536991947310058248515278

for d in divisors(n):
    m1 = long_to_bytes(d)
    m2 = long_to_bytes(n //d)
    flag = m1 + m2
    if b'DUCTF' in flag:
        print(flag)
        break
#DUCTF{is_1nt3ger_f4ct0r1s4t10n_h4rd?}
