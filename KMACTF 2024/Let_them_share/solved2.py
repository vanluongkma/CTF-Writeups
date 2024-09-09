from pwn import *
from json import * 
from ast import literal_eval
from Crypto.Util.number import *
from Crypto.Cipher import AES
from sage.all import *
from collections.abc import Sequence
import math, operator
from typing import List, Tuple

def _process_linear_equations(equations, vars, guesses) -> List[Tuple[List[int], int, int]]:
    result = []

    for rel, m in equations:
        op = rel.operator()
        if op is not operator.eq:
            raise TypeError(f"relation {rel}: not an equality relation")
        expr = (rel - rel.rhs()).lhs().expand()
        for var in expr.variables():
            if var not in vars:
                raise ValueError(f"relation {rel}: variable {var} is not bounded")
        coeffs = []
        for var in vars:
            if expr.degree(var) >= 2:
                raise ValueError(f"relation {rel}: equation is not linear in {var}")
            coeff = expr.coefficient(var)
            if not coeff.is_constant():
                raise ValueError(f"relation {rel}: coefficient of {var} is not constant (equation is not linear)")
            if not coeff.is_integer():
                raise ValueError(f"relation {rel}: coefficient of {var} is not an integer")
            coeffs.append(int(coeff) % m)
        const = expr.subs({var: guesses[var] for var in vars})
        if not const.is_constant():
            raise ValueError(f"relation {rel}: failed to extract constant")
        if not const.is_integer():
            raise ValueError(f"relation {rel}: constant is not integer")
        const = int(const) % m
        result.append((coeffs, const, m))
    return result


def solve_linear_mod(equations, bounds, verbose=False, **lll_args):
    vars = list(bounds)
    guesses = {}
    var_scale = {}
    for var in vars:
        bound = bounds[var]
        if isinstance(bound, Sequence):
            if len(bound) == 2:
                xmin, xmax = map(int, bound)
                guess = (xmax - xmin) // 2 + xmin
            elif len(bound) == 3:
                xmin, guess, xmax = map(int, bound)
            else:
                raise TypeError("Bounds must be integers, 2-tuples or 3-tuples")
        else:
            xmin = 0
            xmax = int(bound)
            guess = xmax // 2
        if not xmin <= guess <= xmax:
            raise ValueError(f"Bound for variable {var} is invalid ({xmin=} {guess=} {xmax=})")
        var_scale[var] = max(xmax - guess, guess - xmin, 1)
        guesses[var] = guess

    var_bits = math.log2(int(prod(var_scale.values()))) + len(vars)
    mod_bits = math.log2(int(prod(m for rel, m in equations)))
    if verbose:
        print(f"verbose: variable entropy: {var_bits:.2f} bits")
        print(f"verbose: modulus entropy: {mod_bits:.2f} bits")
    equation_coeffs = _process_linear_equations(equations, vars, guesses)
    is_inhom = any(const != 0 for coeffs, const, m in equation_coeffs)
    NR = len(equation_coeffs)
    NV = len(vars)

    if is_inhom:
        NV += 1
    B = matrix(ZZ, NR + NV, NR + NV)
    S = max(var_scale.values())
    eqS = S << (NR + NV + 1)

    if var_bits > mod_bits:
        eqS <<= int((var_bits - mod_bits) / NR) + 1
    col_scales = []

    for ri, (coeffs, const, m) in enumerate(equation_coeffs):
        for vi, c in enumerate(coeffs):
            B[NR + vi, ri] = c
        if is_inhom:
            B[NR + NV - 1, ri] = const
        col_scales.append(eqS)
        B[ri, ri] = m

    for vi, var in enumerate(vars):
        col_scales.append(S // var_scale[var])

        B[NR + vi, NR + vi] = 1

    if is_inhom:

        col_scales.append(S)
        B[NR + NV - 1, -1] = 1

    if verbose:
        print("verbose: scaling shifts:", [math.log2(int(s)) for s in col_scales])
        print("verbose: unscaled matrix before:")
        print(B.n())

    for i, s in enumerate(col_scales):
        B[:, i] *= s
    B = B.LLL(**lll_args)
    for i, s in enumerate(col_scales):
        B[:, i] /= s

    for i in range(B.nrows()):
        if sum(x < 0 for x in B[i, :]) > sum(x > 0 for x in B[i, :]):
            B[i, :] *= -1
        if is_inhom and B[i, -1] < 0:
            B[i, :] *= -1

    if verbose:
        print("verbose: unscaled matrix after:")
        print(B.n())

    for row in B:
        if any(x != 0 for x in row[:NR]):
            continue

        if is_inhom:
            if row[-1] != 1:
                if verbose:
                    print(
                        "verbose: zero solution",
                        {var: row[NR + vi] for vi, var in enumerate(vars) if row[NR + vi] != 0},
                    )
                continue

        res = {}
        for vi, var in enumerate(vars):
            res[var] = row[NR + vi] + guesses[var]

        return res
		
io = remote('157.15.86.73', 2004)
io.recvuntil(b'p = ')

p = int(io.recvline()[:-1].decode()) 

io.recvuntil(b'points = ')
points = literal_eval(io.recvline()[:-1].decode())
scale = [2^i for i in range(56,-1,-8)]

x = []
b_values = []

for i in points :
    x.append(i[0])
    b_values.append(i[1])

A_values = []
for i in x :
    multi_tmp = [(i^z)%p for z in range(10,-1,-1)]
    
    multi = []
    for o in multi_tmp :
        for f in scale :
            multi.append((o*f)%p)
    A_values.append(multi)
	
a = [var(f"a_{i}") for i in range(len(A_values[0]))]

eqs = []
for x in range(len(A_values)) :
    eq = 0 
    assert len(A_values[x]) == len(a)
    for c,d in zip(A_values[x],a) :
        eq += c*d 
    
    eqs.append((b_values[x] == eq,p))
    
bounds = {x: (48,70) for x in a }
print(bounds)

sol = solve_linear_mod(eqs,bounds)

ks = list(sol.values())[-8:]
print(ks)
print(sol.values())
y = bytes_to_long(bytes(ks))
io.sendline(str(y).encode())
io.recvline()
