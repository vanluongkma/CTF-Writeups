import random
from secret import gift, check
from Crypto.Util.number import * 
import math

primes = [537853, 627491, 909767, 1017551, 846137, 830639, 784129, 691531, 685427, 527981, 598187, 624199, 677113, 731779, 738197, 785299, 986719, 668903, 898763, 840067]
p = 4606205736235473118387073117800402048791288415461882634612184436946667786949207327621776863371322349775441201502864859
assert 2 * math.prod(primes) == p - 1 and isPrime(p)

enc = []
gift = bytes_to_long(gift.encode())

while gift > 0:
    if gift & 1:
        exponent = random.choice(primes)
        x = pow(random.randint(2,p-2), exponent, p)
        assert check(x, exponent, p)
        enc.append(x)
    else:
        while True:
            x = random.randint(2,p-2)
            if all(not check(x,e,p) for e in primes):
                enc.append(x)
                break
    gift >>= 1

print(f'{enc = }')

