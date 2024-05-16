from sage.all import *
from Crypto.Util.number import long_to_bytes
from output import Public_key
from tqdm import *

Public_key = Public_key
Encrypted_Flag =  45690752833299626276860565848930183308016946786375859806294346622745082512511847698896914843023558560509878243217521


I = identity_matrix(272)
I = 2*I
I = I.insert_row(272, [ZZ(1) for x in range(272)])
Public_key.append(Encrypted_Flag)
E = [[ZZ(x)] for x in Public_key]
L = I.augment(Matrix(E))
R = L.LLL()
for i in tqdm(R):
    if len(set(i[:-1])) == 2:
        F = i

Flag = long_to_bytes(int(''.join(str(i) for i in [1 if i == -1 else 0 for i in F][::-1]),2))
print(Flag)