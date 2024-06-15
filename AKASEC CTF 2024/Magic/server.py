from Crypto.Util.number import getPrime

n = getPrime(512)*getPrime(512)
e = 65537 
m = 8312884801970423563923630354880850246936953016337466382247876358746442082740980087131367805 

print(f'{n = }')
print(f'{e = }')
print()

while True:
    val = input("give your magic number: ")
    try:
        val = int(val)
        if val < 0:
            print("can't shif... Nevermind")
        c = pow(m >> val, e, n)
        print(f'{c = }')
    except:
        print("Are sure about that ...")