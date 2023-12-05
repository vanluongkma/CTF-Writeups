from pwn import *

f = connect("172.104.49.143", 9234)
min=0
max=18446744073709551616
print('> ' + f.recvline().decode())
print('> ' + f.recvline().decode())

while True:
    temp= (min+max)//2
    f.sendline(str(temp))
    fl = f.recvline().decode()
    print(fl)
    if 'too high' in fl:
        max = temp
    else:
        min = temp

    if 'Flag' in fl:
        break
