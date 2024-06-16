from randcracks.xorshift128p.release.xorshift128p_crack import * 
from hashlib import sha256 
import itertools
from pwn import * 
import math
r = process(["python3", "server.py"])
# r = remote("103.163.24.78", 2005)
context.log_level = 'debug'

def find_string(prefix, suffix):
    chars = string.ascii_letters + string.digits
    for length in itertools.count(1):
        for s in itertools.product(chars, repeat=length):
            candidate = prefix + ''.join(s)
            if hashlib.sha256(candidate.encode()).hexdigest()[-6:] == suffix:
                return candidate

line = r.recvlineS().strip()
prefix = line.split('"')[1]
suffix = line.split(' ')[-1]
r.sendline(find_string(prefix, suffix).encode())
alphabet = 'abcdefghijklmnopqrstuvwxyz'
for i in range(50):
    r.recvuntil(b'/50\n')
    prefix = r.recvlineS().strip()
    hash = r.recvlineS().strip()
    r.recvlineS()
    print(prefix)
    state = []
    for char in prefix:
        state.append(alphabet.index(char))
    randSolver = RandomSolver()
    for i in range(80):
        randSolver.submit_random_mul_const(state[i], 26)
    randSolver.solve()
    randomFunc = randSolver.answers[0].random 
    test = prefix[:80]
    for i in range(192-80):
        test += alphabet[math.floor(randomFunc()*26)]
    print(test)
    assert test == prefix
    ans = ""
    for i in range(128):
        ans += alphabet[math.floor(randomFunc()*26)]
    assert sha256(ans.encode()).hexdigest() == hash
    r.sendline(ans.encode())
r.interactive()