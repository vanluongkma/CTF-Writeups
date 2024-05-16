from sage.all import *
from output import p, rot_matrix, flag_out

_flag = matrix(GF(p), rot_matrix).inverse() * matrix(GF(p), flag_out) * matrix(GF(p), rot_matrix).T.inverse()

flag = ''
for i in range(len(list(_flag))):
    x = _flag[i][i]
    temp = is_square(x)
    if temp < 256:
        flag += chr(temp)
    else:
        flag += chr(p - temp)
print(flag)




# from sage.all import *

# with open("output.txt", 'r') as out:
#     data = out.read().split('\n')
#     p = int(data[0].split("=")[1])
#     rot_matrix = matrix(GF(p), eval(data[1].split("=")[1]))
#     flag_out = matrix(GF(p), eval(data[2].split("=")[1]))
    
# # flag_out = rot_matrix * flag.T*flag * rot_matrix.T
# # Đặt A = flag.T*flag
# # find A
# print(rot_matrix)
# print(flag_out)
# A = rot_matrix.inverse()# * flag_out * rot_matrix.T.inverse()
# print()
# l = len(list(A))

# D = [A[i][i] for i in range(l)]
# F = [pow(x, -(p+1)//4, p) for x in D]
# F = [i if i < 256 else p - i for i in F]
# flag = "".join([chr(i) for i in F])
# # print(flag)