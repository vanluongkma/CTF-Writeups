from z3 import *
from pwn import *

def LFSR(state):
    state = state
    while 1:
        yield state & 0xf
        for i in range(4):
            bit = (state ^ (state >> 1) ^ (state >> 3) ^ (state >> 4)) & 1
            state = (state >> 1) | (bit << 63)

state_value = 0
rps = ["rock", "paper", "scissors"]
s = z3.Solver()
state = z3.BitVec('state', 64)

io = remote('mc.ax', 31234)
for _ in range(56):
    io.recvuntil(b"Choose rock, paper, or scissors: ")
    io.sendline(b'paper')
    ans = io.recvline().strip().rstrip()
    if ans == b'You win!':
        output = 0
    if ans == b'You lose!':
        output = 2
    if ans == b'Tie!':
        output = 1      
    s.add((state & 0xf) % 3 == output)
    for _ in range(4):
        bit = (state ^ z3.LShR(state, 1) ^ z3.LShR(state, 3) ^ z3.LShR(state, 4)) & 1
        state = z3.LShR(state, 1) | (bit << 63)

if s.check() == z3.sat:
    model = s.model()
    state_value = model.eval(state).as_long()
    print("Found solution:")
else:
    print("No solution found.")
cop = LFSR(state_value)
index = 0

rs = []
for i in range(50):
    index = (next(cop) + 1) % 3
    rs.append(rps[index].encode())

data = (b'\n'.join(rs))
io.sendline(data)
io.interactive()