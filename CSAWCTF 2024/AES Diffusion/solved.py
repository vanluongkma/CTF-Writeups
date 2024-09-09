# from pwn import *

# # Define the server and port
# server = 'diffusion.ctf.csaw.io'
# port = 5000

# # Connect to the server
# conn = remote(server, port)
# conn.recvuntil(b"What will the ShiftRows output be? Please give the answer like the state given above except put all the rows in one line when submitting the answer")
# conn.recvline()
# # Prepare the result of the ShiftRows operation
# shift_rows_result = "[['x0', 'x4', 'x8', 'x12'], ['x5', 'x9', 'x13', 'x1'], ['x10', 'x14', 'x2', 'x6'], ['x7', 'x11', 'x15', 'x3']]"

# # Send the result to the server
# conn.sendline(shift_rows_result)
# conn.recvline()


from sympy import symbols, simplify

# Định nghĩa các biến
x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15 = symbols('x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 x13 x14 x15')

# Ví dụ về một biểu thức cụ thể
expr1 = 2 * (2 * x0 + 3 * x5 + 1 * x10 + 1 * x15) + 3 * (1 * x4 + 2 * x9 + 3 * x14 + 1 * x3) + 1 * (1 * x8 + 1 * x13 + 2 * x2 + 3 * x7) + 1 * (3 * x12 + 1 * x1 + 1 * x6 + 2 * x11)

# Thay các giá trị vào biến
values = {x0: 1, x1: 0, x2: 0, x3: 0, x4: 0, x5: 0, x6: 0, x7: 0, x8: 0, x9: 0, x10: 0, x11: 0, x12: 0, x13: 0, x14: 0, x15: 0}
result = expr1.subs(values)

print(simplify(result))

