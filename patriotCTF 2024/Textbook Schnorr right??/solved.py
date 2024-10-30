import random
import subprocess
from Crypto.Util.number import *
from Crypto.PublicKey import RSA

# Unix timestamp of public_key.pem
key_timestamp = 1726938558

# taken from "openssl rsa -pubin -in public_key.pem -text -noout"
e = 0x00bd202092e27db343467c522563436c1ef2e51cee6cc0b02d728751011d954ad9c2fc485aa424e0162aa072360c8c40e8f6b4854b46bb9b07999697afc7da148b

random.seed(key_timestamp)
p, q = getPrime(512, random.randbytes), getPrime(512, random.randbytes)
n = p*q
phi = (p-1)*(q-1)

assert GCD(e, phi) == 1
d = pow(e, -1, phi)

key = RSA.construct((n, e, d, p, q))

with open("private_key.pem", "wb") as f:
    f.write(key.export_key("PEM"))

subprocess.run("openssl rsautl -decrypt -in flag.enc -inkey private_key.pem".split())