from pwn import *
import string

host = 'chal.competitivecyber.club'
port = 6001

flag_charset = string.printable

flag = 'pctf{'
junk = 'A' * 16

def encrypt(conn, data):
    conn.sendlineafter(b'Send challenge > ', data.encode())
    conn.recvuntil(b'Response > ')
    return conn.recvline().strip()

conn = remote(host, port)

p = log.progress('Flag: ')

while flag[-1] != '}':
    payload = junk[:-(len(flag)+1)]
    truth = encrypt(conn, payload)[:32]
    for c in flag_charset:
        p.status(f'{flag}{c}')
        if truth == encrypt(conn, payload + flag + c)[:32]:
            flag += c
            break

p.success(flag)
conn.close()