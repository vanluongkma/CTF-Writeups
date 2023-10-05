from pwn import *

f = connect("crypto.securinets.tn", 8887)
min=0
max=2**32

while True:
    x=(min+max)//2
    f.sendline(str(x).encode())
    flag = f.recv()
    if b"Securinets" in flag:
        print(flag)
        break
    if b"Smaller" in flag:
        min = x
    else :
        max = x
