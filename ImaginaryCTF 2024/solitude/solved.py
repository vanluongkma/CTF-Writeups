# from pwn import *
# from Crypto.Util.number import *
# from string import *
# from tqdm import *
# # s = connect("solitude.chal.imaginaryctf.org", 1337)
# s = process(["python3", "main.py"])
# s.recvline()
# s.recvuntil(b"got flag? ")

# tmp = []
# s.sendline(b"100000")
# for i in tqdm(range(100000)):
#     # print(s.recvline().strip().decode())
#     tmp.append(bytes.fromhex(s.recvline().strip().decode()))
    
# for i_ in range(33):
#     k = [tmp[i][i_]for i in range(100000)]
#     count_ = 0
#     max_ = 0
#     for i in (ascii_letters + digits + "{}_").encode():
#         l = k.count(i)
#         if l > count_:
#             max_ = i
#             count_ = l
            
#     print(chr(max_), end="")


from pwn import *
import pandas as pd
from collections import Counter
context.log_level = 'error'
conn = process(["python3", "main.py"])
conn.recvuntil(b"got flag? ")
conn.sendline(b"10000")
data = conn.recvuntil(b"got flag? ", drop=True)
data = [bytes.fromhex(x.decode()) for x in data.split(b"\n") if x]
data = [[data[i][j] for i in range(len(data))] for j in range(len(data[0]))]
for c in data:
    print(chr(Counter(c).most_common(1)[0][0]), end="")
conn.close()
