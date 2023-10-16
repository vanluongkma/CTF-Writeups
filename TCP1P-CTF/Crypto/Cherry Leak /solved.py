# s1 = p - q 
# m1 = p % q
# p = kq + m1
# s1 + q = kq + m1
# s1 - m1 = (k-1)q
# neww q
# s2 = p - q 
# m2 = p % q
# p = kq + m2
# s2 + q = kq + m2
# s2 - m2 = (k-1)q
#=>  q = gcd(s1-m1,s2-m2)   => p = s2+q


from pwn import *
from Crypto.Util.number import *
def rec():
    return int(f.recvline().split(b' ')[-1].strip().decode())

f = connect("ctf.tcp1p.com", 13339)
f.sendlineafter(b'> ', b'2')
f.sendlineafter(b'> ', b'-')
s1 = rec()
f.sendlineafter(b'> ', b'2')
f.sendlineafter(b'> ', b'%')
mod1 = rec()


f.sendlineafter(b'> ', b'1')
f.sendlineafter(b'> ', b'p')
f.sendlineafter(b'> ', b'2')
f.sendlineafter(b'> ', b'-')
s2 = rec()
f.sendlineafter(b'> ', b'2')
f.sendlineafter(b'> ', b'%')
mod2 = rec()
f.sendlineafter("> ", b"3")
c = rec()

print(f"{s1 = }")
print(f"{s2 = }")
print(f"{mod1 = }")
print(f"{mod2 =}")

a = s1 - mod1
b = s2 - mod2
q = GCD(a, b)
p = s2 + q

n = p*q
phi = (p-1)*(q-1)
e = 65537
d = pow(e, -1, phi)
m = pow(c, d, n)
print(long_to_bytes(m))
