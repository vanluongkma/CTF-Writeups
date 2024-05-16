import random

primes = [537853, 627491, 909767, 1017551, 846137, 830639, 784129, 691531, 685427, 527981, 598187, 624199, 677113, 731779, 738197, 785299, 986719, 668903, 898763, 840067]
p = 4606205736235473118387073117800402048791288415461882634612184436946667786949207327621776863371322349775441201502864859
print(random.choice(primes))
print(len(primes))
from sage.all import *
from output import enc

_flag = matrix(GF(p), enc)
print(len(list(_flag)))
flag = ''
for i in range(len(list(_flag))):
    x = _flag[i][i]
    temp = is_square(x)
    print(x)
    if temp < 256:
        flag += chr(temp)
    else:
        flag += chr(p - temp)
print(flag)
