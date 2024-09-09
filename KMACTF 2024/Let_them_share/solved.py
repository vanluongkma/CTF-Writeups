# from pwn import *
# from ast import literal_eval
# from sage.all import *
# import numpy as np
# import math
# from Crypto.Util.number import *

# # Connect to the remote service
# io = remote('157.15.86.73', 2004)
# io.recvuntil(b'p = ')

# # Read parameters from the remote service
# p = int(io.recvline().strip().decode())
# io.recvuntil(b'points = ')
# points = literal_eval(io.recvline().strip().decode())

# # Precompute scale values
# scale = [2**i for i in range(56, -1, -8)]

# # Extract x and b_values from points
# x = [i[0] for i in points]
# b_values = [i[1] for i in points]

# # Prepare A_values
# DEGREE = 10
# A_values = []
# for i in x:
#     multi = [(i**z % p * f % p) for z in range(DEGREE + 1) for f in scale]
#     A_values.append(multi)

# def solve_linear_mod(equations, bounds, verbose=False, **lll_args):
#     vars = list(bounds)
#     guesses = {}
#     var_scale = {}
#     for var in vars:
#         bound = bounds[var]
#         if isinstance(bound, tuple):
#             if len(bound) == 2:
#                 xmin, xmax = map(int, bound)
#                 guess = (xmax - xmin) // 2 + xmin
#             elif len(bound) == 3:
#                 xmin, guess, xmax = map(int, bound)
#             else:
#                 raise TypeError("Bounds must be integers, 2-tuples or 3-tuples")
#         else:
#             xmin = 0
#             xmax = int(bound)
#             guess = xmax // 2
#         if not xmin <= guess <= xmax:
#             raise ValueError(f"Bound for variable {var} is invalid ({xmin=} {guess=} {xmax=})")
#         var_scale[var] = max(xmax - guess, guess - xmin, 1)
#         guesses[var] = guess

#     var_bits = math.log2(int(prod(var_scale.values()))) + len(vars)
#     mod_bits = math.log2(int(prod(m for _, m in equations)))
#     if verbose:
#         print(f"Variable entropy: {var_bits:.2f} bits")
#         print(f"Modulus entropy: {mod_bits:.2f} bits")

#     # Create matrix B
#     equation_coeffs = [(list(rel.lhs().expand().coefficients(ZZ)), int(rel.rhs()) % m, m) for rel, m in equations]
#     is_inhom = any(const != 0 for _, const, _ in equation_coeffs)
#     NR = len(equation_coeffs)
#     NV = len(vars) + (1 if is_inhom else 0)
#     B = matrix(ZZ, NR + NV, NR + NV)

#     # Fill matrix B
#     S = max(var_scale.values())
#     eqS = S << (NR + NV + 1)
#     if var_bits > mod_bits:
#         eqS <<= int((var_bits - mod_bits) / NR) + 1
#     col_scales = []

#     for ri, (coeffs, const, m) in enumerate(equation_coeffs):
#         for vi, c in enumerate(coeffs):
#             B[NR + vi, ri] = c
#         if is_inhom:
#             B[NR + NV - 1, ri] = const
#         col_scales.append(eqS)
#         B[ri, ri] = m

#     for vi, var in enumerate(vars):
#         col_scales.append(S // var_scale[var])
#         B[NR + vi, NR + vi] = 1
#     if is_inhom:
#         col_scales.append(S)
#         B[NR + NV - 1, -1] = 1

#     if verbose:
#         print("Scaling shifts:", [math.log2(int(s)) for s in col_scales])
#         print("Unscaled matrix before:")
#         print(B.n())

#     for i, s in enumerate(col_scales):
#         B[:, i] *= s
#     B = B.LLL(**lll_args)
#     for i, s in enumerate(col_scales):
#         B[:, i] /= s

#     for row in B:
#         if any(x != 0 for x in row[:NR]):
#             continue
#         if is_inhom and row[-1] != 1:
#             continue

#         res = {var: row[NR + vi] + guesses[var] for vi, var in enumerate(vars)}
#         return res

# # Prepare equations
# a = [var(f"a_{i}") for i in range(len(A_values[0]))]
# eqs = [(b == sum(c * d for c, d in zip(A_values[x], a)), p) for x, b in enumerate(b_values)]

# # Define bounds and solve
# bounds = {x: (48, 70) for x in a}
# sol = solve_linear_mod(eqs, bounds)
# ks = list(sol.values())[-8:]
# print(ks)
# print(sol.values())

# # Convert solution to bytes and send
# y = bytes(ks)
# io.sendline(str(bytes_to_long(y)).encode())
# io.interactive()

from pwn import *

def padding_oracle(pre_block, block):
    pad = 16 * bytes([0])
    I = [0] * 16
    c1 = b''
    
    for i in range(1, 17):
        for j in range(1, 256):
            io.recvuntil(b'Please enter the ciphertext: ')
            payload = pad[:16-i] + bytes([j]) + c1
            msg = payload + block
            io.sendline(msg.hex().encode())
            oracle_reply = io.recvuntil(b'\n')
            if b'Looks fine' in oracle_reply:
                I[16 - i] = j ^ i
                c1 = xor(bytes([i + 1]) * i, bytes(I[16 - i:]))
                break
    
    return xor(pre_block, I)

# Kết nối với dịch vụ
io = remote("cbc.ctf.csaw.io", 9996)

# Giá trị biến c đã được định sẵn ở đây
c = bytes.fromhex(
    "167a787a54d2d363a04daddcf27225656ef664aabf092feb59c16e39986f31a59d00ff1ae8f92347d2543d2d5b0e8af0e4e0856df775087b02dc37c1b2e15269"
)

# Giả sử c đã được chia thành các block 16-byte
block_size = 16
blocks = [c[i:i + block_size] for i in range(0, len(c), block_size)]

# Thực hiện padding oracle attack cho từng cặp block
plain_blocks = []
for i in range(len(blocks) - 1):
    pre_block = blocks[i]
    block = blocks[i + 1]
    plain_block = padding_oracle(pre_block, block)
    plain_blocks.append(plain_block)

# Kết quả cuối cùng
plaintext = b''.join(plain_blocks)
print("Decrypted plaintext:", plaintext)

# Đóng kết nối
io.close()