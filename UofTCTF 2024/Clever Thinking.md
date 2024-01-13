```python3
from Crypto.Cipher import AES
import hashlib
from sage.all import *

def shared_secret(public_key, private_key):
    S = public_key * private_key
    return S.xy()

def SmartAttack(P,Q,p):
    E = P.curve()
    Eqp = EllipticCurve(Qp(p, 2), [ ZZ(t) + randint(0,p)*p for t in E.a_invariants() ])

    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)
    for P_Qp in P_Qps:
        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:
            break

    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)
    for Q_Qp in Q_Qps:
        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:
            break

    p_times_P = p*P_Qp
    p_times_Q = p*Q_Qp

    x_P,y_P = p_times_P.xy()
    x_Q,y_Q = p_times_Q.xy()

    phi_P = -(x_P/y_P)
    phi_Q = -(x_Q/y_Q)
    k = phi_Q/phi_P
    return ZZ(k)

p = 235322474717419
a = 0
b = 8856682
E = EllipticCurve(GF(p), [a, b])

G = E(185328074730054, 87402695517612)

A = E(184640716867876, 45877854358580)
B = E(157967230203538, 128158547239620)

nA = SmartAttack(G, A, p)

secret = shared_secret(B, nA)
print(secret)
```
