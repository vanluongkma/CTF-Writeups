from Crypto.Util.number import*


# msg = b'VOTE FOR PEDRO'

# x = var('x')
# n = 256 ^ (len(msg) + 1)
# f = x ^ 3 - bytes_to_long(msg)
# print(solve_mod(f, n))

# ALICE_N = 22266616657574989868109324252160663470925207690694094953312891282341426880506924648525181014287214350136557941201445475540830225059514652125310445352175047408966028497316806142156338927162621004774769949534239479839334209147097793526879762417526445739552772039876568156469224491682030314994880247983332964121759307658270083947005466578077153185206199759569902810832114058818478518470715726064960617482910172035743003538122402440142861494899725720505181663738931151677884218457824676140190841393217857683627886497104915390385283364971133316672332846071665082777884028170668140862010444247560019193505999704028222347577

# from Crypto.Util.number import*
# p = getPrime(1024)
# q = getPrime(1024)
# ALICE_N = p * q
# ALICE_E = 3

# plaintext = b"VOTE FOR PEDRO"

# b_x00 = b"\x00"

# left = long_to_bytes(getPrime(100))
# print(left)

# vote = left + b_x00 + plaintext
# print(vote)

# verified_vote = vote.split(b'\00')[-1]
# print(verified_vote)

from Crypto.Util.number import *
from pwn import *
from sage.all import * 
import json
msg = b'VOTE FOR PEDRO'

x = var('x')
f = x ** 3 - bytes_to_long(msg)

vote = solve_mod(f, 256**15)[0][0]
print(vote)

f = remote('socket.cryptohack.org', 13375, level = "debug")
f.recvline()
f.sendline(json.dumps({'option': 'vote', 'vote': hex(vote)}))
f.interactive()