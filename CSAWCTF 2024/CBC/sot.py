from pwn import *

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def padding_oracle(pre_block, block):
    block_size = 16
    I = [0] * block_size
    c1 = b''

    for i in range(1, block_size + 1):
        for j in range(256):
            io.recvuntil(b'Please enter the ciphertext: ')
            payload = bytes([0] * (block_size - i)) + bytes([j]) + c1
            msg = payload + block
            io.sendline(msg.hex().encode())
            response = io.recvuntil(b'\n')
            if b'Looks fine' in response:
                I[block_size - i] = j ^ i
                c1 = xor(bytes([i + 1]) * i, bytes(I[block_size - i:]))
                break

    return xor(pre_block, I)

io = remote("cbc.ctf.csaw.io", 9996)
c = bytes.fromhex("167a787a54d2d363a04daddcf27225656ef664aabf092feb59c16e39986f31a59d00ff1ae8f92347d2543d2d5b0e8af0e4e0856df775087b02dc37c1b2e15269bdd85446c9e00ff648f7de40673c4c73")
block_size = 16
blocks = [c[i:i + block_size] for i in range(0, len(c), block_size)]

plain_blocks = []
for i in range(len(blocks) - 1):
    pre_block = blocks[i]
    block = blocks[i + 1]
    plain_block = padding_oracle(pre_block, block)
    plain_blocks.append(plain_block)

plaintext = b''.join(plain_blocks)
print("Decrypted plaintext:", plaintext.decode('utf-8'))
io.close()
