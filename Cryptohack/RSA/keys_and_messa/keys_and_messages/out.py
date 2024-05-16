from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from factordb.factordb import FactorDB
from Crypto.Util.number import*


#msg = "???"
for i in range(1, 50):
    print("decode " , i)
    with open(f"/mnt/c/Users/dinhv/Documents/CTF_Event/keys_and_messages_701dba5b1a84cb168547ec18227a7740/keys_and_messages/{i}.pem", 'r') as f:
        key = RSA.importKey(f.read())
        print(key.exportKey)
    with open(f"/mnt/c/Users/dinhv/Documents/CTF_Event/keys_and_messages_701dba5b1a84cb168547ec18227a7740/keys_and_messages/{i}.ciphertext", "r") as f:
        c = f.read() 
    try:
        n = key.n
        e = key.e
        f = FactorDB(n)
        f.connect()
        [p, q] = (f.get_factor_list())
    except:
        continue
    d = pow(e,-1,(p-1)*(q-1))
    print(f"{c = }")
    print(f"{n = }")
    print(f"{e = }")
    c = bytes.fromhex(c)
    print(c)
    key = RSA.construct((n,e,d))
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.decrypt(c)
    if b"crypto{" in ciphertext:
        print(ciphertext)
        break