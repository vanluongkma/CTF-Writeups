
# Last Wave before you start i highly recommend that you play some of the pwn challenges to get used to pwntools and to use netcat ! Other than that try to find me !
# nc crypto.securinets.tn 8887

from random import randint
flag=open("flag.txt","r").read()
target=randint(0,2**32)
while True:
    user_input=int(input("Try to guess my number\n"))
    if user_input>target:
        print("Too big maybe next time")
    else:
        print("Smaller mater")
    if user_input==target:
        print(flag)
