from pwn import *

f = process(["python3", "zkwarmup.py"])
f.recvline()
f.recvline()
f.recvline()
f.recvline()