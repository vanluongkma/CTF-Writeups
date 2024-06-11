from pwn import *
import json 

m1 = "43727970746f4861636b20536563757265205361666530309b9f2f6f86928ea091d873fc781f34f7151536db965edebf11718595c31d5f2bf832b1e9e70d49671d7fe8851d3776a20eed4a89052a47f9cbef6b8d64e6fda4fd2daf78ebed627987517d0681a6c197a830435cac27fdf523956d739543ea641dbb741f18d2496e"
m2 = "43727970746f4861636c20536563757265205361666530309b9f2f6f86928ea091d873fc781f34f7151536db965edebf11718595c31d5f2bf832b1e9e70d49671d7fe8851d3776a20eec4a89052a47f9cbef6b8d64e6fda4fd2daf78ebed627987517d0681a6c197a830435cac27fdf523956d739543ea641dbb741f18d2496e"

io = remote('socket.cryptohack.org', 13397, level = 'debug')
io.recvline()

to_send = {'option': 'insert_key', 'key': m1}
io.sendline(json.dumps(to_send).encode())
print(io.recvline())

to_send = {'option': 'insert_key', 'key': m2}
io.sendline(json.dumps(to_send).encode())
print(io.recvline())

to_send = {'option': 'unlock'}
io.sendline(json.dumps(to_send).encode())
io.interactive()

# check Blog https://vanluong504.github.io/posts/Hash-Function-Cryptohack/#twin-keys