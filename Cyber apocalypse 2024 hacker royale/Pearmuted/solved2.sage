from data import g, A, B
print(b"luong")
m = []
for i in range(len(g)):
    t = [0]*len(g)
    t[g[i]] = 1
    m.append(t)

G = Matrix(m)
f = G.charpoly()

a = []
for i in range(len(g)):
    t = [0]*len(g)
    t[A[i]] = 1
    a.append(t)
A_pub = Matrix(a)

b = []
for i in range(len(g)):
    t = [0]*len(g)
    t[B[i]] = 1
    b.append(t)
B_pub = Matrix(b)
J, X = G.jordan_form(transformation=True)


X = []
M = []
for g,e in f.factor():
    assert e == 1
    K = GF(2^g.degree(), x, modulus=g, impl='pari_ffelt')
    a = g.roots(K)[0][0]
    w = (G - a*1).right_kernel_matrix().rows()[0]
    V = [vector([0]*i + [1] + [0]*(N-1-i)) for i in range(50000)]
    P = Matrix(K, [w] + V[:-1]).transpose()
    assert P.row_space().dimension() == N
    J_ = ~P * A_pub * P
    X.append(int(J_[0][0].log(a)))
    M.append(K.multiplicative_generator().multiplicative_order())

A_priv = crt(X, M)
print(A_priv)