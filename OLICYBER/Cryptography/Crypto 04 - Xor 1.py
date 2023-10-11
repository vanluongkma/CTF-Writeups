from pwn import *


m1 = "158bbd7ca876c60530ee0e0bb2de20ef8af95bc60bdf"
m2 = "73e7dc1bd30ef6576f883e79edaa48dcd58e6aa82aa2"

flag1 = bytes.fromhex(m1)
flag2 = bytes.fromhex(m2)
print(xor(flag1, flag2).decode())


#flag{x0R_f0r_th3_w1n!}
