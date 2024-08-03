from Crypto.Util.number import *

p = getPrime(64)
q = getPrime(64)
r = getPrime(64)
s = getPrime(64)
a = getPrime(64)
n = p*q*r*s*a
e = 0x10001

FLAG = b'FLAG{This_is_a_fake_flag}'
m = bytes_to_long(FLAG)
enc = pow(m, e, n)
print(f'n = {n}')
print(f'e = {e}')
print(f'enc = {enc}')

# n = 317903423385943473062528814030345176720578295695512495346444822768171649361480819163749494400347
# e = 65537
# enc = 127075137729897107295787718796341877071536678034322988535029776806418266591167534816788125330265