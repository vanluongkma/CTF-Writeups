from Crypto.Util.number import bytes_to_long
import random

p = 1337**42
coff = [random.randint(1, p-1) for i in range(3)]

class LCG:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (coff[0]*self.seed**3 + coff[1]*self.seed**2 + coff[2]*self.seed)%p
        return self.seed

    def encyrpt(self, bina):
        encrypt = []
        seed = []
        bin_msg=bin(bina)[2:]
        for i in bin_msg:
            seed.append(self.seed)
            self.next()
            if i == '1':
                if self.seed % 2 == 0:
                    encrypt.append('0')
                else:
                    encrypt.append('1')
            else:
                if self.seed % 2 == 0:
                    encrypt.append('1')
                else:
                    encrypt.append('0')
        return ''.join(encrypt), seed

flag = b'AKASEC{example_flag}'
seed = random.randint(1, p-1)
lcg = LCG(seed)

for i in range(1337):
    lcg.next()

encrypted, seeds = lcg.encyrpt(bytes_to_long(flag))

print(f'seed = {seeds[-10:]}')
print(f'encrypted flag = {encrypted}')