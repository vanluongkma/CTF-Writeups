from Crypto.Cipher import AES
from itertools import combinations

with open("keysmashes.txt") as rf:
    lines = [line.strip() for line in rf.readlines()]

alphabet = list(b"fjdlska;")
assert len(alphabet) == 8

ct = bytes.fromhex('ed05f1440f3ae5309a3125a91dfb0edef306e1a64d1c5f7d8cea88cdb7a0d7d66bb36860082a291138b48c5a6344c1ab')

odd = set([1, 3, 5, 7, 9, 11, 13, 15])
even = set([0, 2, 4, 6, 8, 10, 12, 14])

for x1, x2 in combinations(odd, 2):
    ox = odd.difference([x1, x2])
    for y1, y2 in combinations(ox, 2):
        oy = ox.difference([y1, y2])
        for z1, z2 in combinations(oy, 2):
            t1, t2 = oy.difference([z1, z2])
            assert set([x1, x2, y1, y2, z1, z2, t1, t2]) == odd
            for a1, a2 in combinations(even, 2):
                ea = even.difference([a1, a2])
                for b1, b2 in combinations(ea, 2):
                    eb = ea.difference([b1, b2])
                    for c1, c2 in combinations(eb, 2):
                        d1, d2 = eb.difference([c1, c2])
                        key = [0] * 16
                        key[x1] = key[x2] = ord('j')
                        key[y1] = key[y2] = ord('l')
                        key[z1] = key[z2] = ord('k')
                        key[t1] = key[t2] = ord(';')

                        key[a1] = key[a2] = ord('f')
                        key[b1] = key[b2] = ord('d')
                        key[c1] = key[c2] = ord('s')
                        key[d1] = key[d2] = ord('a')

                        aes = AES.new(bytes(key), AES.MODE_ECB)
                        try:
                            print(aes.decrypt(ct).decode())
                        except:
                            pass