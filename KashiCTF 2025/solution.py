from pwn import *
import HashTools
from tqdm import trange
for i in trange(64) :
    io = remote("127.0.0.1", 1337)

    io.recvuntil(b"Example: ")
    datas = io.recvline().decode()[:-1].split("|")
   
    original_data = datas[0].encode()
    sig = datas[1]
    append_data = b"&file=flag.txt"
    
    magic = HashTools.new("sha1")
    new_data, new_sig = magic.extension(
        secret_length=i, original_data=original_data,
        append_data=append_data, signature=sig
        )
   
        # print(str(new_data))
    send_data = str(new_data)[2:][:-1] + '|' + str(new_sig)
    user_data, received_hmac = send_data.rsplit("|", 1)
  
    try :
        user_data_bytes = bytes(user_data, "utf-8").decode("unicode_escape").encode("latin-1")
        print("Round ", i)
        io.sendline(send_data.encode())
        print(io.recvall())
        exit()
    except :
        pass
    io.close()