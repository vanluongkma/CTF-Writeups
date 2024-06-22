import hashlib

with open('my_diary_11_8_Wednesday.txt', 'r') as f:
    enc = eval(f.read())

def re_md5enc(enc):
    decrypted = []
    for value in enc:
        for i in range(256): 
            x = hashlib.md5(str(i).encode()).hexdigest()
            if int(x, 16) == value:
                decrypted.append(chr(i))
                break
    return ''.join(decrypted)


print(re_md5enc(enc))
