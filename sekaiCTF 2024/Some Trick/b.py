import random

# Parameters from your challenge output
GSIZE = 8209
GNUM = 79
MOD_VALUE = 8029  # Giả sử bạn đã xác định được mod = 8029

cipher_suite = 11588293687583300782738267189901758830398853503235698893788514874213733015304
bob_says = 1111614208002976848114629085517104393139324568013022833215418419894738856675113047885509760165661071796212470278045704569300841344342728032373230548010560987078693455547178834159070889805183884856265869214040306570925429834823154750582449894772157334135323930449863391044604980989010796743765176748451123704994
alice_says = 604020125617187736196491360161970833876398220439719671462401476402316584188377460251449139793404323872324818490880370931943986064318260053237275284811605170994249698893022831648684175355273733223301824318194398274042832257348224660641798270424707396736243075335711221872179019840074549434173097699028875690335

random.seed(cipher_suite)

# Functions from the original code
def gen(n):
    p, i = [0] * n, 0
    for j in random.sample(range(1, n), n - 1):
        p[i], i = j, j
    return tuple(p)

def gexp(g, e):
    res = tuple(g)
    while e:
        if e & 1:
            res = tuple(res[i] for i in g)
        e >>= 1
        g = tuple(g[i] for i in g)
    return res

def enc(k, m, G):
    if not G:
        return m
    mod = len(G[0])
    return gexp(G[0], k % mod)[m % mod] + enc(k // mod, m // mod, G[1:]) * mod

def inverse(perm):
    res = list(perm)
    for i, v in enumerate(perm):
        res[v] = i
    return res

# Generate G
G = [gen(GSIZE) for i in range(GNUM)]

# Inverse G
G_inv = [inverse(i) for i in G]

# Try to reverse the encryption for alice_key
for potential_alice_key in range(MOD_VALUE):  # Trying smaller range
    decrypted_value = enc(alice_says, potential_alice_key, G_inv)
    if decrypted_value == bob_says:
        print(f"Found Alice's key: {potential_alice_key}")
        break
