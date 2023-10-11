from base64 import b64decode
from Crypto.Util.number import*


flag1 = "ZmxhZ3t3NDF0XzF0c19hbGxfYjE="
flag2 = 664813035583918006462745898431981286737635929725
print(b64decode(flag1)+ long_to_bytes(flag2))

# flag{w41t_1ts_all_b1ts?_4lw4ys_H4s_b33n}
