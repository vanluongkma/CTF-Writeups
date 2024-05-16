
from pwn import *
from Crypto.Util.number import long_to_bytes
import json

io = remote("socket.cryptohack.org", 13402)
io.recvline()

def get_hash(data):
    io.sendline(json.dumps({"option":"mix","data":enhex(data)}))
    return json.loads(io.recvline())["mixed"]
    
seen = set()
with log.progress("Getting all 256 hashes for all zeroes input") as progress:
    while len(seen) < 256:
        seen.add(get_hash(long_to_bytes(0, 39)))
        progress.status(str(len(seen)))     

flag = 0
with log.progress("Getting flag") as progress:
    for i in range(8*39-1, -1, -1):
        # there's a small chance to get a false negative, but it'll do
        if get_hash(long_to_bytes(1<<i, 39)) not in seen: 
            flag |= (1<<i)
        progress.status(f"{long_to_bytes(flag)[:-i//8]}")
    progress.success(f"{long_to_bytes(flag)}")
   