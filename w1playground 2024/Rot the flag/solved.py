from sage.all import *
from output import p, rot_matrix, flag_out

_flag = matrix(GF(p), rot_matrix).inverse() * matrix(GF(p), flag_out) * matrix(GF(p), rot_matrix).T.inverse()

flag = ''
for i in range(len(list(_flag))):
    x = _flag[i][i]
    temp = pow(x, -(p+1)//4, p)
    if temp < 256:
        flag += chr(temp)
    else:
        flag += chr(p - temp)
print(flag)