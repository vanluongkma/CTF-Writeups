import os

for i in range(25000, 0, -1):
    f = open("password.txt", "r")
    pwd = f.read()
    f.close()
    com = 'unzip -P ' + pwd.strip() + ' -o zip-' + str(i) + '.zip' 
    delete = 'rm -f zip-' + str(i) + '.zip'
    os.system(com)
    os.system(delete)
