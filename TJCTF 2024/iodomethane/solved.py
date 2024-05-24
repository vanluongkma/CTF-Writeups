from sage.all import *
from itertools import product
alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0192834756{}_!@#$%^&*()"
modulus = 15106021798142166691
ct = [8103443654527565038, 9131436358818679900, 4957881569325453096, 10608823513649500284, 6675039786579943629, 6611905972844131155, 1244757961681113340, 7547487070745190563, 1913848887301325654, 9737862765813246630, 2820240734893834667, 4787888165190302097, 11681061051439179359, 11976272630379115896, 2884226871403054033, 13149362434991348085, 2676520484503789480, 6933002550284269375, 6634913706901406922, 3790038065981008837, 7593117393518680210, 1266282031812681717, 14297832010203960867, 6803759075981258244, 2235840587449302546, 9573113061825958419, 7208484535445728720, 3230648965441849617, 14844603229849620928, 2548590493342454145, 12648684202717570605, 8664656898390315577, 13502288186462622020, 8391628990279857365, 5501744205282111713, 5327399420219427046, 904912426181632886, 4805354280735678357, 12915117098149429818, 12340346813869037506, 9907136040657333887, 12822605127735793613]
start = 0
end = start + 9
C = ct[start:end]
flag = [alphabet.index(i) for i in "tjctf{"]
print(flag)
for x, y, z in product(range(75), repeat=3):
    ff = flag + [x, y, z]
    M = matrix(GF(modulus), 3, 3, ff)
    N = matrix(GF(modulus), 3, 3, C)
    print(flag)
    try:
        K = M.solve_right(N)
        if not K.is_invertible(): continue
        v = vector(GF(modulus), ct[end:end+3])
        u = v * K.inverse()
        if all(t < len(alphabet) for t in list(u)):
            print("Found key!")
            print(K)
            F = matrix(GF(modulus), len(ct) // 3, 3, ct)
            print(F)
            flag_ = F * K.inverse()
            print(flag)
            flag_ = sum([list(f) for f in flag_], start = [])
            print("".join(alphabet[f] for f in flag_[:41]))
            print()
    except:
        pass