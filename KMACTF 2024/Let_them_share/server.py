import os 
import random
from Crypto.Util.number import bytes_to_long, getPrime

DEGREE = 10
BITSIZE = 64
FLAG = "KMACTF{s0m3_r3ad4ble_5tr1ng_like_7his}"

def get_coeff(p):
    # bigger coeff, safer sss :D
    while True:
        coeff = bytes_to_long(os.urandom(64 // 16).hex().upper().encode())
        if BITSIZE - 1 <= coeff.bit_length() and coeff < p:
            return coeff

def _eval_at(poly, x, prime):
    """Evaluates polynomial (coefficient tuple) at x, used to generate a
    shamir pool in make_random_shares below.
    """
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= prime
    return x, accum

def make_random_shares(secret, modulus):
    coefficients = [secret] + [get_coeff(modulus) for _ in range(DEGREE)]
    print(f"{coefficients = }")
    return [_eval_at(coefficients, random.randint(0, modulus - 1), modulus) for _ in range(DEGREE)]

def main():
    p = getPrime(BITSIZE)
    SECRET = get_coeff(p)
    points = make_random_shares(SECRET, p)
    print("Wait, there's something wrong, is our secret lost ?")
    print("p =", p)
    print("points =", points)
    number = int(input("What's our secret ? "))
    if number == SECRET:
        print("Cool!! You can deal with hard challenge, get your treasure here:", FLAG)
        exit()
    else:
        print("We lost it! :((")
        exit()

if __name__ == "__main__":
    main()

