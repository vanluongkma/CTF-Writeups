import random
from secrets import randbelow

# Các giá trị từ output của bạn
CIPHER_SUITE = 11588293687583300782738267189901758830398853503235698893788514874213733015304
bob_encr = 1111614208002976848114629085517104393139324568013022833215418419894738856675113047885509760165661071796212470278045704569300841344342728032373230548010560987078693455547178834159070889805183884856265869214040306570925429834823154750582449894772157334135323930449863391044604980989010796743765176748451123704994
alice_encr = 604020125617187736196491360161970833876398220439719671462401476402316584188377460251449139793404323872324818490880370931943986064318260053237275284811605170994249698893022831648684175355273733223301824318194398274042832257348224660641798270424707396736243075335711221872179019840074549434173097699028875690335
bob_decr = 1147619756293043615104918524329039840095770853537816486566786648648221642959639870209342960416893887453291002571183024876655761759608975905429620629383962952505085957134763018112052951676254333633850791751647937810537021074857421481271059820171548242268202218309654920497306813456012659559390764214813398616792

# Thiết lập random seed
random.seed(CIPHER_SUITE)

GSIZE = 8209
GNUM = 79
MOD = 8029  # Giá trị mod được biết

# Hàm sinh hoán vị
def gen(n):
    p, i = [0] * n, 0
    for j in random.sample(range(1, n), n - 1):
        p[i], i = j, j
    return tuple(p)

# Hàm lũy thừa của hoán vị
def gexp(g, e):
    res = tuple(g)
    while e:
        if e & 1:
            res = tuple(res[i] for i in g)
        e >>= 1
        g = tuple(g[i] for i in g)
    return res

# Hàm mã hóa
def enc(k, m, G):
    if not G:
        return m
    mod = len(G[0])
    return gexp(G[0], k % mod)[m % mod] + enc(k // mod, m // mod, G[1:]) * mod

# Hàm đảo ngược hoán vị
def inverse(perm):
    res = list(perm)
    for i, v in enumerate(perm):
        res[v] = i
    return res

# Sinh danh sách các hoán vị
G = [gen(GSIZE) for _ in range(GNUM)]

# Hàm tìm khóa khả nghi dựa trên giá trị mod
def find_possible_keys(bob_encr, alice_encr, mod):
    possible_keys = []
    for k in range(mod):  # Sử dụng giá trị mod để hạn chế không gian tìm kiếm
        encrypted_value = enc(bob_encr, k, [inverse(i) for i in G])
        if encrypted_value == alice_encr:
            possible_keys.append(k)
            print(f"Possible key found: {k}")
    return possible_keys

# Giải mã FLAG với các khóa khả nghi
def decrypt_flag_with_possible_keys(possible_keys):
    for key in possible_keys:
        flag_value = enc(bob_encr, key, [inverse(i) for i in G])
        flag_bytes = flag_value.to_bytes((flag_value.bit_length() + 7) // 8, 'big')
        if b"SEKAI" in flag_bytes:  # Kiểm tra nếu FLAG có định dạng như vậy
            print(f"Recovered FLAG: {flag_bytes}")
            break

# Tìm khóa khả nghi và giải mã FLAG
possible_keys = find_possible_keys(bob_encr, alice_encr, MOD)
decrypt_flag_with_possible_keys(possible_keys)
