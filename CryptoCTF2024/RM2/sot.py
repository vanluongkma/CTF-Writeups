from Crypto.Util.number import *
from factordb.factordb import FactorDB
from pwn import *
import re


f = remote("01.cr.yp.toc.tf", 13371, level='debug')
f.recvuntil(b"Please provide your desired 1024-bit prime numbers p, q:")

p= 98713501923232051054844740510687989999273022489836711569952864028898217237641550238694095751228728231022511110694084289536079894189010129732619311796495998678633088914448015297822600116508658635272868115786055670132447451825682398850076833522399059649016996676833663150607781375047681152693609495897227395073
q= 98032022449061585038721542179485828847755969029591992195618638781894673969126090864788421582301945665253360898718520488155260869787309818000890692662745169321102850403969194207149819771626691830649430229801121914323491640361075837233313904927428558447650268580852799068744578037754574241690763215408015081473
first = str(p) + ", " + str(q)
f.sendline(first.encode())

f.recvuntil(b"\n")
# server_response = f.recvline().decode()
c1_match = re.search(r'c1 = (\d+)',  f.recvline().decode())
c1 = int(c1_match.group(1))
print(f"{c1 = }")

c2_match = re.search(r'c2 = (\d+)',  f.recvline().decode())
c2 = int(c2_match.group(1))
print(f"{c2 = }")

fator = FactorDB(p-1)
fator.connect()
p_1= fator.get_factor_list()

fator = FactorDB(q- 1)
fator.connect()
q_1= fator.get_factor_list()

e= 65537
phi_p= 1
for x in p_1:
    phi_p *= x- 1
phi_q= 1
for y in q_1:
    phi_q *= y-1
phi_1= phi_p*phi_q


d_1= pow(e, -1, (p-1)*(q-1))
m1= long_to_bytes(pow(c1, d_1, (p-1)*(q-1)))

m1 = m1[-64:].replace(b"\x00", b"")
m1 = m1.decode('latin-1')

fator = FactorDB(2*p+ 1)
fator.connect()
p_1= fator.get_factor_list()

fator = FactorDB(2*q+ 1)
fator.connect()
q_1= fator.get_factor_list()
e= 65537
phi_p= 1
for x in p_1:
    phi_p *= x- 1
phi_q= 1
for y in q_1:
    phi_q *= y-1
phi_1= phi_p*phi_q
d2= pow(e, -1, phi_1)

m2= long_to_bytes(pow(c2, d2, (2*p+1)*(2*q+1)))
m2 = m2.decode('latin-1')

get_flag = str(m1) + str(m2)
f.sendline(get_flag.encode())
f.interactive()

