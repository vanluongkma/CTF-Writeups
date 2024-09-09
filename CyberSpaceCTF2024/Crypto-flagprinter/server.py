from sympy import isprime
from Crypto.Util.number import long_to_bytes, bytes_to_long

# Given values
w = 115017953136750842312826274882950615840
x = 16700949197226085826583888467555942943
y = 20681722155136911131278141581010571320
c = 2246028367836066762231325616808997113924108877001369440213213182152044731534905739635043920048066680458409222434813

def find_primes(w, x, y):
    from sympy import nextprime
    p = 2
    while True:
        if isprime(p):
            q = w
            r = x
            if (r % q == y) and isprime(q) and isprime(r):
                return p, q, r
        p = nextprime(p)

p, q, r = find_primes(w, x, y)

# Ensure p, q, r are sorted
p, q, r = sorted([p, q, r])

# Compute n
n = p * q * r

# Compute the modular inverse of e
e = 65537
phi = (p - 1) * (q - 1) * (r - 1)
from sympy import mod_inverse
d = mod_inverse(e, phi)

# Decrypt the message
m = pow(c, d, n)

# Convert to bytes
flag = long_to_bytes(m)
print("Decrypted message:", flag.decode())
