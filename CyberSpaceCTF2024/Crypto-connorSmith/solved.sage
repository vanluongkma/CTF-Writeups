# from sage.rings.polynomial.multi_polynomial_sequence import PolynomialSequence
# from Crypto.Util.number import getPrime
# from tqdm import tqdm
# import cysignals
# import itertools
# from re import sub as re_sub
# from subprocess import run as subprocess_run


# def _from_sagematrix_to_fplllmatrix(mat: matrix) -> str:
#     return '[' + re_sub(
#         r'\[ ',
#         r'[',
#         re_sub(r' +', r' ', str(mat))
#     ) + ']'


# def _fplllmatrix_to_sagematrix(matrixstr: str) -> matrix:
#     matlist = eval(matrixstr.replace(' ', ',').replace('\n', ','))
#     return matrix(ZZ, matlist)


# def _transformation_matrix(mat, lllmat, use_pari_matsol=False):
#     # pari.matker() does not assure smallest kernel in Z (seems not call hermite normal form)
#     # Sage kernel calls hermite normal form
#     #
#     # for computing ZZ transformation, use pari.matker, pari.matsolvemod
#     # assume first kerdim vectors for lllmat are zero vector
#     #
#     # anyway, transformation computation after LLL/BKZ is slow.
#     # instead, use builtin transformation computation on LLL/BKZ package

#     if use_pari_matsol:
#         mat_pari = pari.matrix(mat.nrows(), mat.ncols(), mat.list())
#         ker_pari_t = pari.matker(pari.mattranspose(mat_pari), 1)
#         kerdim = len(ker_pari_t)
#         if kerdim == 0:
#             # empty matrix
#             trans = matrix(ZZ, 0, mat.nrows())
#         else:
#             trans = matrix(ZZ, pari.mattranspose(ker_pari_t).Col().list())

#         mat_pari = pari.matrix(mat.nrows(), mat.ncols(), mat.list())
#         for i in range(kerdim, lllmat.nrows(), 1):
#             lllmat_pari = pari.vector(lllmat.ncols(), lllmat[i].list())
#             trans_pari_t = pari.matsolvemod(
#                 pari.mattranspose(mat_pari), 0, pari.mattranspose(lllmat_pari)
#             )
#             transele = matrix(ZZ, trans_pari_t.mattranspose().Col().list())
#             trans = trans.stack(transele)
#     else:
#         trans = mat.kernel().matrix()
#         kerdim = trans.nrows()

#         for i in range(kerdim, lllmat.nrows(), 1):
#             transele = mat.solve_left(lllmat[i])
#             trans = trans.stack(transele)

#     return trans


# def do_LLL_flatter(
#         mat: matrix,
#         transformation: bool = False,
#         use_pari_kernel: bool = False, use_pari_matsol: bool = False
#     ):


#     if mat == zero_matrix(ZZ, mat.nrows(), mat.ncols()):
#         return mat, identity_matrix(ZZ, mat.nrows())

#     # sage has integer_kernel(), but somehow slow. instead using pari.matker
#     if use_pari_kernel:
#         mat_pari = pari.matrix(mat.nrows(), mat.ncols(), mat.list())
#         ker_pari_t = pari.matker(mat_pari.mattranspose(), 1)
#         ker = matrix(ZZ, ker_pari_t.mattranspose().Col().list())
#     else:
#         ker = mat.kernel().matrix()

#     kerdim = ker.nrows()
#     matrow = mat.nrows()
#     col = mat.ncols()
#     if kerdim == matrow: # full kernel
#         return zero_matrix(ZZ, matrow, col), ker
#     if kerdim == 0:
#         Hsub = mat
#         U = identity_matrix(ZZ, matrow)
#     else:
#         # heuristic construction for unimodular matrix which maps zero vectors on kernel
#         # searching unimodular matrix can be done by HNF
#         # (echeron_form(algorithm='pari') calls mathnf()),
#         # but it is slow and produces big elements
#         #
#         # instead, searching determinant of submatrix = 1/-1,
#         # then the determinant of whole unimodular matrix is det(submatrix)*(-1)^j
#         # assume kernel has good property for gcd (gcd of some row elements might be 1)
#         found_choice = False
#         ker_submat_rows = tuple(range(kerdim))
#         ker_submat_cols = []
#         pivot = matrow - 1
#         # search submatrix of kernel assuming last column vectors are triangulate
#         while len(ker_submat_cols) < kerdim:
#             if ker[ker_submat_rows, tuple([pivot])] != zero_matrix(ZZ, kerdim, 1):
#                 ker_submat_cols.append(pivot)
#             pivot -= 1
#         ker_submat_cols = tuple(sorted(ker_submat_cols))
#         ker_last_det = int(ker[ker_submat_rows, ker_submat_cols].determinant())
#         if ker_last_det == 0:
#             raise ValueError("no unimodular matrix found (cause ker_last_det=0)")
#         for choice in range(pivot, -1, -1):
#             # gcd check
#             gcd_row = ker_last_det
#             for i in range(kerdim):
#                 gcd_row = GCD(gcd_row, ker[i, choice])
#             if abs(gcd_row) != 1:
#                 continue

#             # choice pivot: last columes for kernel are triangulated and small
#             kersubidxes = [choice] + list(ker_submat_cols)
#             detlst = [ker_last_det]
#             for i in range(1, kerdim+1, 1):
#                 ker_submat_rows = tuple(range(kerdim))
#                 ker_submat_cols = tuple(kersubidxes[:i] + kersubidxes[i+1:])
#                 detlst.append(ker[ker_submat_rows, ker_submat_cols].determinant())
#                 detlist_gcd, detlist_coef = _xgcd_list(detlst)
#                 if detlist_gcd == 1:
#                     found_choice = True
#                     break
#             if not found_choice:
#                 continue
#             detlist_coef = detlist_coef + [0] * ((kerdim + 1) - len(detlist_coef))
#             break
#         if not found_choice:
#             raise ValueError("no unimodular matrix found")
#         U_top_vec = [0 for _ in range(matrow)]
#         for i in range(kerdim+1):
#             U_top_vec[kersubidxes[i]] = (-1)**i * detlist_coef[i]
#         U_sub = matrix(ZZ, 1, matrow, U_top_vec)
#         not_kersubidxes = sorted(list(set(list(range(matrow))) - set(kersubidxes)))
#         for j in range(kerdim+1, matrow):
#             onevec = [0 for _ in range(matrow)]
#             onevec[not_kersubidxes[j-(kerdim+1)]] = 1
#             U_sub = U_sub.stack(vector(ZZ, matrow, onevec))
#         Hsub = U_sub * mat
#         U = ker.stack(U_sub)
#         #assert abs(U.determinant()) == 1

#     if Hsub.nrows() == 1:
#         lllmat = Hsub
#     else:
#         matstr = _from_sagematrix_to_fplllmatrix(Hsub)
#         result = subprocess_run(
#             'flatter',
#             input=matstr.encode(), capture_output=True
#         )
#         if result.returncode != 0:
#             print(result.stderr)
#             raise ValueError(f"LLL failed with return code {result.returncode}")
#         lllmat = _fplllmatrix_to_sagematrix(result.stdout.decode().strip())

#     if transformation:
#         trans = _transformation_matrix(Hsub, lllmat, use_pari_matsol=use_pari_matsol)
#     else:
#         trans = None

#     restrows = mat.nrows() - lllmat.nrows()
#     final_lllmat = zero_matrix(ZZ, restrows, lllmat.ncols()).stack(lllmat)

#     if transformation:
#         middle_trans = identity_matrix(ZZ, restrows).augment(zero_matrix(ZZ, restrows, trans.ncols())).stack(
#             zero_matrix(ZZ, trans.nrows(), restrows).augment(trans)
#         )
#         final_trans = middle_trans * U
#         #assert abs(final_trans.determinant()) == 1
#         #assert final_trans * mat == final_lllmat
#     else:
#         final_trans = None

#     return final_lllmat, final_trans

# def generate_polynomial(N, _p):
#     coefficients = []
#     bounds = []
#     i = 0
#     ii = 0
#     is_previous_unknown = True if _p[-1] == '?' else False

#     for char in _p[::-1]:
#         is_current_unknown = True if char == '?' else False
#         if is_current_unknown and not is_previous_unknown:
#             coefficients.append(2^(4*ii))
#             i = 0
#         if not is_current_unknown and is_previous_unknown:
#             bounds.append(2^(4*i))
#         is_previous_unknown = is_current_unknown
#         i += 1
#         ii += 1

#     if is_current_unknown:
#         bounds.append(2^(4*i))

#     if _p[-1] == '?':
#         coefficients = coefficients[::-1]
#         coefficients.append(1)

#     d = len(coefficients)
#     xs = [f"x{i}" for i in range(d)]
#     PR = PolynomialRing(Zmod(N), d, xs)
#     f = int(_p.replace("?", "0"), 16) + sum([c * PR.objgens()[1][n] for n, c in enumerate(coefficients)])
#     return f, bounds[::-1]

# def univariate(f, X, beta=1.0, m=None):
#     N = f.parent().characteristic()
#     delta = f.degree()
#     if m is None:
#         epsilon = RR(beta^2/f.degree() - log(2*X, N))
#         m = max(beta**2/(delta * epsilon), 7*beta/delta).ceil()
#     t = int((delta*m*(1/beta - 1)).floor())
#     #print(f"m = {m}")
    
#     f = f.monic().change_ring(ZZ)
#     P,(x,) = f.parent().objgens()
#     g  = [x**j * N**(m-i) * f**i for i in range(m) for j in range(delta)]
#     g.extend([x**i * f**m for i in range(t)]) 
#     B = Matrix(ZZ, len(g), delta*m + max(delta,t))

#     for i in range(B.nrows()):
#         for j in range(g[i].degree()+1):
#             B[i,j] = g[i][j]*X**j

#     try:
#         B, _ = do_LLL_flatter(B)
#     except:
#         B = B.LLL()
#     f = sum([ZZ(B[0,i]//X**i)*x**i for i in range(B.ncols())])
#     roots = set([f.base_ring()(r) for r,m in f.roots() if abs(r) <= X])
#     return [root for root in roots if N.gcd(ZZ(f(root))) >= N**beta]


# def solve_root_jacobian_newton_internal(pollst, startpnt, maxiternum=500):
#     # NOTE: Newton method's complexity is larger than BFGS, but for small variables Newton method converges soon.
#     pollst_Q = Sequence(pollst, pollst[0].parent().change_ring(QQ))
#     vars_pol = pollst_Q[0].parent().gens()
#     jac = jacobian(pollst_Q, vars_pol)

#     if all([ele == 0 for ele in startpnt]):
#         # just for prepnt != pnt
#         prepnt = {vars_pol[i]: 1 for i in range(len(vars_pol))}
#     else:
#         prepnt = {vars_pol[i]: 0 for i in range(len(vars_pol))}
#     pnt = {vars_pol[i]: startpnt[i] for i in range(len(vars_pol))}

#     iternum = 0
#     while True:
#         if iternum >= maxiternum:
#             return None

#         evalpollst = [(pollst_Q[i].subs(pnt)) for i in range(len(pollst_Q))]
#         if all([int(ele) == 0 for ele in evalpollst]):
#             break
#         jac_eval = jac.subs(pnt)
#         evalpolvec = vector(QQ, len(evalpollst), evalpollst)
#         try:
#             pnt_diff_vec = jac_eval.solve_right(evalpolvec)
#         except:
#             return None

#         prepnt = {key:value for key,value in prepnt.items()}
#         pnt = {vars_pol[i]: int(pnt[vars_pol[i]] - pnt_diff_vec[i]) for i in range(len(pollst_Q))}
#         if all([prepnt[vars_pol[i]] == pnt[vars_pol[i]] for i in range(len(vars_pol))]):
#             return None
#         prepnt = {key:value for key,value in pnt.items()}
#         iternum += 1
#     return [int(pnt[vars_pol[i]]) for i in range(len(vars_pol))]


# def solve_system_jacobian(pollst, bounds):
#     vars_pol = pollst[0].parent().gens()
#     # not applicable to non-determined system
#     if len(vars_pol) > len(pollst):
#         return []
#     # pollst is not always algebraically independent,
#     # so just randomly choose wishing to obtain an algebraically independent set
#     for random_subset in tqdm(Combinations(pollst, k=len(vars_pol))): 
#         for signs in itertools.product([1, -1], repeat=len(vars_pol)):
#             startpnt = [signs[i] * bounds[i] for i in range(len(vars_pol))]
#             result = solve_root_jacobian_newton_internal(random_subset, startpnt)
#             # filter too much small solution
#             if result is not None:
#                 if all([abs(ele) < 2**16 for ele in result]):
#                     continue
#                 return [result]

# def solve_system_gb(H, f, timeout=5):
#     vs = list(f.variables())
#     H_ = PolynomialSequence([], H[0].parent().change_ring(QQ))
#     for h in tqdm(H):
#         H_.append(h)
#         I = H_.ideal()
#         roots = []

#         alarm(timeout)
#         try:
#             for root in I.variety(ring=ZZ):
#                 root = tuple(H[0].parent().base_ring()(root[var]) for var in vs)
#                 roots.append(root)
#             cancel_alarm()
#             if roots != []:
#                 return roots
#         except:
#             cancel_alarm()       

# class IIter:
#     def __init__(self, m, n):
#         self.m = m
#         self.n = n
#         self.arr = [0 for _ in range(n)]
#         self.sum = 0
#         self.stop = False

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.stop:
#             raise StopIteration
#         ret = tuple(self.arr)
#         self.stop = True
#         for i in range(self.n - 1, -1, -1):
#             if self.sum == self.m or self.arr[i] == self.m:
#                 self.sum -= self.arr[i]
#                 self.arr[i] = 0
#                 continue

#             self.arr[i] += 1
#             self.sum += 1
#             self.stop = False
#             break
#         return ret

# def multivariate_herrmann_may(f, bounds, m, t):
#     n = f.nvariables()
#     N = f.base_ring().cardinality()
#     f /= f.coefficients().pop(0)  
#     f = f.change_ring(ZZ)
#     x = f.parent().objgens()[1]

#     g = []
#     monomials = []
#     Xmul = []
#     for ii in IIter(m, n):
#         k = ii[0]
#         g_tmp = f^k * N^max(t-k, 0)
#         monomial = x[0]^k
#         Xmul_tmp = bounds[0]^k
#         for j in range(1, n):
#             g_tmp *= x[j]^ii[j]
#             monomial *= x[j]^ii[j]
#             Xmul_tmp *= bounds[j]^ii[j]
#         g.append(g_tmp)
#         monomials.append(monomial)
#         Xmul.append(Xmul_tmp)

#     B = Matrix(ZZ, len(g), len(g))
#     for i in range(B.nrows()):
#         for j in range(i + 1):
#             if j == 0:
#                 B[i, j] = g[i].constant_coefficient()
#             else:
#                 v = g[i].monomial_coefficient(monomials[j])
#                 B[i, j] = v * Xmul[j]

#     print("LLL...")
#     try:
#         B, _ = do_LLL_flatter(B)
#     except:
#         B = B.LLL()
#     print("LLL done")

#     h = []
#     for i in range(B.nrows()):
#         h_tmp = 0
#         for j in range(B.ncols()):
#             if j == 0:
#                 h_tmp += B[i, j]
#             else:
#                 assert B[i, j] % Xmul[j] == 0
#                 v = ZZ(B[i, j] // Xmul[j])
#                 h_tmp += v * monomials[j]
#         h.append(h_tmp)
   
#     return f, h

# def multivariate_shift_polynomials(f, bounds, m, d):
#     if d is None:
#         d = f.degree()

#     R = f.base_ring()
#     N = R.cardinality()
#     f_ = (f // f.lc()).change_ring(ZZ)
#     f = f.change_ring(ZZ)
#     l = f.lm()

#     M = []
#     for k in range(m+1):
#         M_k = set()
#         T = set((f ^ (m-k)).monomials())
#         for mon in (f^m).monomials():
#             if mon//l^k in T: 
#                 for extra in itertools.product(range(d), repeat=f.nvariables()):
#                     g = mon * prod(map(power, f.variables(), extra))
#                     M_k.add(g)
#         M.append(M_k)
#     M.append(set())

#     shifts = PolynomialSequence([], f.parent())
#     for k in range(m+1):
#         for mon in M[k] - M[k+1]:
#             g = mon//l^k * f_^k * N^(m-k)
#             shifts.append(g)

#     B, monomials = shifts.coefficients_monomials()
#     monomials = vector(monomials)

#     factors = [monomial(*bounds) for monomial in monomials]
#     for i, factor in enumerate(factors):
#         B.rescale_col(i, factor)

#     print("LLL...")
#     try:
#         B, _ = do_LLL_flatter(B)
#     except:
#         B = B.dense_matrix().LLL()
#     print("LLL done")

#     B = B.change_ring(QQ)
#     for i, factor in enumerate(factors):
#         B.rescale_col(i, 1/factor)
#     B = B.change_ring(ZZ)

#     H = PolynomialSequence([h for h in B*monomials if not h.is_zero()])
#     return f, H

# def multivariate(f, bounds, implementation, algorithm, m=1, t=1, d=None):
#     if implementation == "herrmann_may":
#         f, h = multivariate_herrmann_may(f, bounds, m, t)
#     elif implementation == "shift_polynomials":
#         f, h = multivariate_shift_polynomials(f, bounds, m, d)
#     else:
#         print("invalid implementation")
#         return None

#     if algorithm == "jacobian":
#         return solve_system_jacobian(h, bounds)
#     elif algorithm == "groebner":
#         return solve_system_gb(h, f)
#     else:
#         print("invalid algorithm")
#         return None


# from Crypto.Util.number import *
# n = 7552253013225223212686972759229408890943243937848116869511428282592494711559240135372705736006054353083281103140787662239958191241833157109597880624454796412006762881501916845155158694626704629051045217266597685547634722763704638532067409306181328833329683262904207364205190648604464680961179156366009048508124744257064547090561236984730817200175311749708243086463240602718911105727107075971987228340827791295829216059926076767577606528647738447725195880791137450082195604212374273765390335921438605358227547423468794396280894150559661664635540689602987474623120205743645087417873312711804245504568677508120251077973
# e = 3972273176912267799970180147678020025192175195982968793722693097132970664724388722714705209022371322943558028173459714967997171817396680330435643595109433373306392229639747130134793710239081601404067602930871254806754684103349829634489509031907387929080189489106215966862642406152181674399593026117258657690036458955106821789654735855538375273851668820461621159458690509295524433242439365251850800232909323376356116251835554606066609685882803255427299046970093232995420925951786433206910901590576814359503385919307570360242528454529766855342865079257244016304989185569117193284115242278439808082079787893597831292429
# c = 6722063431743120124281037577917473736384734002344400102535470664988199976365033546621632487383386053044468700113542626459908567596300577088705896140930724832695917664482501591801075560437336915520962349830960551339852803481367045861684404716913927870231244602348980596739084252620702852351036834534769613031735817640709051052713694452907186969900542466747407949270228341375666775282809021111998328175103742416108902755346724742467339317044645243210574003890806923017769148711785248795287760426567277473640239499920974270994457112678786022613046685998793486144172215215581287541508145268729387185453679039441575292812
# hint = 891237814844096809623936988168241703768093224718029580247856301709140 << 795

# PR = PolynomialRing(Zmod(e), names=('x', 'k'))
# x, k = PR.gens()


# f =  k*(-hint + x) - 1 + k + k * n

# # print(multivariate(f, [2 ** 795, 2 ** 700], "herrmann_may", "jacobian", m=3 , d=2))
# # tmp = [104187725513747723032497684230019653080386848786186065006191528308813081840900501117522378138618035792858279853022394381967012525845615079380677438317669219470236837179906477475985598217372094136390078377123228155963917938085569707674435584, 5260135901548373507240989882880128665550339802823173859498280903068732154297080822113666536277588451226982968856178217713019432250183803863127814770651880849955223671128444598191663757884322717271293251735781376]
# tmp = [208375451027495446064995368460039306160773697572372130012383056617626163681801002235044756277236071585716559706044788763934025051691230158761354876635338438940473674359812954951971196434744188272780156754246456311927835876171139415348871168, 5260135901548373507240989882880128665550339802823173859498280903068732154297080822113666536277588451226982968856178217713019432250183803863127814770651880849955223671128444598191663757884322717271293251735781376]
# phi = n + 1 - hint + tmp[0]
# d = inverse_mod(e, phi)
# print(long_to_bytes(pow(c, d, n)))


from sage.all import *
from Crypto.Util.number import long_to_bytes
import itertools
import time

def defund_multivariate(f, bounds, m=1, d=None):
    if not d:
        d = f.degree()
    R = f.base_ring()
    N = R.cardinality()
    #f /= f.coefficients().pop(0)
    f = f.change_ring(ZZ)
    G = Sequence([], f.parent())
    for i in range(m+1):
        base = N**(m-i) * f**i
        for shifts in itertools.product(range(d), repeat=f.nvariables()):
            g = base * prod(map(power, f.variables(), shifts))
            G.append(g)
    B, monomials = G.coefficient_matrix()
    monomials = vector(monomials)
    factors = [monomial(*bounds) for monomial in monomials]
    for i, factor in enumerate(factors):
        B.rescale_col(i, factor)
    B = B.dense_matrix().LLL()
    B = B.change_ring(QQ)
    for i, factor in enumerate(factors):
        B.rescale_col(i, 1/factor)
    H = Sequence([], f.parent().change_ring(QQ))
    for h in filter(None, B*monomials):
        H.append(h)
        I = H.ideal()
        if I.dimension() == -1:
            H.pop()
        elif I.dimension() == 0:
            roots = []
            for root in I.variety(ring=ZZ):
                root = tuple(R(root[var]) for var in f.variables())
                roots.append(root)
            return roots
    return []

N = 19282112175199978757836790171743965808556141332434285352170729722521865890609217429046141295537816930541924182998909562083698920856072346162557815886237229264121898755433412533482126541329548702775770143247650851599401561096718651487037827010050790646159466244317390781671012298275457373525801543526267366187300611684121791440019453477960116151111518638327512032534438725355012288132078297336022345191322352475491917812480667118478851881569004846945054761218450170039505801742139361415001762972843392915917362687002389544085717267293749632274172047014063754505738387497936948593351962378508889608476557817435612331109
e = 759144221738931675093557102170677353579561041294726203914539682964155957688422269649390205448288182595719749730177684290722612220231745941471249725368375894344689067345745436617862615823470254091065500552484875817492658284271953728791123913841838289429102119988817075146467825050362468319135708276062757109523486378879168235276646456345423247807336673627785832316640714594804633785659201572499492216165738054224222488930724633341363391633009867772788335481929080024689402894203884060212338196354326707884317192115473007842709788649357486125885605855223976802633036272484051629039693566209282878848239632432837365667
d = 128343650400194695855728317368374625964411188393285474608602045633884848344165541167691848864529206233808758274977093038649702499223183014076308718859474823332045322969098339686062869270453398855617114121560528507963
p = 122689279459374591531799642420712864254849604910019160886285923077274918419926740560422062435874100395773113448910263954373881706052864374096415508361697216476278032043436230408968244446893247481519599351787920886957278426803983414376569487420161468708851176222429137874242900859701432600170610051754745536371
q = 157162160053150819145047823187062687480423913756838606035219435049680208344132668698884139013995200593812425446568043756014328771903278562333292859456844632967175387089735399639511980491580007525120504347643362875391140771233530693012972109045159052573356425030505197519195691436399386595969609098724509191879

un = 760
hint = (p+q) >> un
sh = hint << un

xx = p+q - sh
kk = (1 - e*d) // ((N+1) // 2 - (p+q) // 2)

print(xx.bit_length())
print(kk.bit_length())

PR = PolynomialRing(Zmod(e), names=('x', 'k'))
x, k = PR.gens()

A = (N+1) // 2
s = -(sh + x) // 2
f =  k*(A + s) - 1

assert f(x = xx, k=kk) == 0
print(f'{xx = }')
print(f'{kk = }')
start = time.time()
temp = defund_multivariate(f, bounds=(2**un, 2**711), m=7, d=6)
print(temp)

print(f'Time executed: ', time.time() - start)