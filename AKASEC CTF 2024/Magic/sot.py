# from Crypto.Util.number import long_to_bytes
# from pwn import *
# from tqdm import tqdm

# # f = remote('20.80.240.190', 4455)
# f = process(["python3", "server.py"])
# context.log_level = 'DEBUG'
# f.recvuntil(b'n = ')
# n = int(f.recvline().strip().decode())

# f.recvuntil(b'e = ')
# e = int(f.recvline().strip().decode())

# flag = 0
# for i in tqdm(range(302, -1, -1)):
#     f.sendline(str(i).encode())
#     f.recvuntil(b'c = ')
#     c = (int(f.recvline().strip().decode()))
#     flag *= 2
#     print(flag)
#     if pow(flag, e, n) == c:
#         continue
#     flag += 1
# print(long_to_bytes(flag))


from pwn import *
from Crypto.Util.number import long_to_bytes
from tqdm import tqdm

# conn = remote('20.80.240.190', 4455)
conn = process(["python3", "server.py"])
context.log_level = 'DEBUG'
conn.recvuntil(b'n = ')
n = int(conn.recvline().strip().decode())

conn.recvuntil(b'e = ')
e = int(conn.recvline().strip().decode())

bin_flag = '1'
for i in tqdm(range(301, -1, -1)):
    conn.sendline(str(i).encode())
    conn.recvuntil(b'c = ')
    c = int(conn.recvline().strip().decode())
    for d in ['0', '1']:
        test_flag = int(bin_flag + d, 2)
        if pow(test_flag, e, n) == c:
            bin_flag += d
            break
        
print(long_to_bytes(int(bin_flag, 2)))