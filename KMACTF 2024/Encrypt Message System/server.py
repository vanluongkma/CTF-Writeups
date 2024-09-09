import secrets
import hashlib
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Util.number import getPrime
import json

flag = b'KMACTF{******************************}'

l = 16
key = secrets.token_bytes(32)
def enc(cmt, nonce):
    nonce = hashlib.sha256(nonce).digest()[:12]
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(cmt)
    return nonce + ct + tag

def dec(cmt):
    nonce = cmt[:12]
    ct = cmt[12:-16]
    tag = cmt[-16:]
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    pt = cipher.decrypt_and_verify(ct, tag)
    return pt

def polynomial_evaluation(coefficients, x):
	at_x = 0
	for i in range(len(coefficients)):
		at_x += coefficients[i] * (x ** i)
		at_x = at_x % p
	return at_x

def verify(enc_message):
    message = dec(enc_message)
    if message == b'give me the flag':
        return True
    return False

print("Welcome to the encrypt message system\n")
print("1. Encrypt message")
print("2. Get flag")

p = getPrime(512)
print(f"p = {p}")

while True:
    try:
        option = input("Enter option: ")
        if option == "1":            
            coefficients = [secrets.randbelow(p) for _ in range(l)]
            print(f"coefficients = {coefficients}")
            message = input("Enter message: ")
            
            if message == "give me the flag":
                print("Invalid message")
                break
            
            x = int(input("Enter x: "))
            y = polynomial_evaluation(coefficients, x)
            encrypted = enc(message.encode(), str(y).encode())
            print(encrypted.hex())
        
        if option == "2":
            encrypted = bytes.fromhex(input("Enter encrypted message: "))
            try:
                if verify(encrypted):
                    print(flag)
            except:
                print("you failed")
                pass
    except: 
        print("Invalid input")
        break   