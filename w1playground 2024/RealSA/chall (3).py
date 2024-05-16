from secrets import token_urlsafe
from sage.all import GF, random_matrix, matrix, random_prime

p = random_prime(1<<256, proof=True, lbound=1<<255)

with open("flag.txt") as f:
    flag = f.read().strip()
    flag = flag.encode()
    flag = [pow(f,-1,p) for f in flag]

rot_matrix = random_matrix(GF(p), nrows=len(flag), x=2432564235)
while rot_matrix.det() == 0:
    rot_matrix = random_matrix(GF(p), nrows=len(flag), x=2432564235)

# rotate the flag
flag = matrix(flag).T
flag = rot_matrix * flag

flag_out = flag*flag.T
out = open("output.txt", 'w')
out.write(f'{p = }\n')
out.write(f"rot_matrix = {list(rot_matrix)}\n")
out.write(f"flag_out = {list(flag_out)}")
