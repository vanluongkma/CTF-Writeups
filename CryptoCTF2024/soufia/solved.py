from pwn import *
import re

f = remote("03.cr.yp.toc.tf", 13377, level='debug')

f.recvline()
f.recvline()
f.recvline()
f.recvline()

f0_match = re.search(r'f\(0\) = (\d+)', f.recvline().decode())
f0 = int(f0_match.group(1))
print(f"f(0) = {f0}")
fx_match = re.search(r'f\((\d+)\) = (\d+)', f.recvline().decode())
x = int(fx_match.group(1))
fx = int(fx_match.group(2))
print(f"f({x}) = {fx}")

def calculate_f_x(x, f0, fx, y):
    k = (fx - f0) // x
    return y * k + f0

f.recvline()
fx_match = re.search(r'f\((\d+)\):', f.recvline().decode())
y = int(fx_match.group(1))
print(x)

num1 = calculate_f_x(x,f0,fx,y)
print(num1)
f.sendline(str(num1).encode())
f.recvline()
for i in range(10000):
    fx_match = re.search(r'f\((\d+)\):', f.recvline().decode())
    y = int(fx_match.group(1))
    print(x)

    num1 = calculate_f_x(x,f0,fx,y)
    print(num1)
    f.sendline(str(num1).encode())
    f.recvline()

# CCTF{A_funCti0nal_3qu4tiOn_iZ_4_7yPe_oF_EquAtioN_tHaT_inv0lVe5_an_unKnOwn_funCt!on_r4tH3r_thAn_juS7_vArIabl3s!!}