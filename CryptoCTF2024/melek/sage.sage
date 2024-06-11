from sage.all import *
from Crypto.Util.number import bytes_to_long, long_to_bytes
from output import enc

# Decryption function
def decrypt(e, p, PT):
    R.<x> = GF(p)[]
    # Reconstruct the polynomial from the points
    f = R.lagrange_polynomial(PT)
    # Get the coefficients of the polynomial
    C = f.coefficients(sparse=False)
    
    # The last coefficient is the encrypted message m^e % p
    m_e_mod_p = int(C[-1])
    
    # Convert e and p-1 to Sage integers
    sage_e = Integer(e)
    sage_p_minus_1 = Integer(p - 1)
    
    # Compute the modular inverse of e modulo p-1
    d = sage_e.inverse_mod(sage_p_minus_1)
    
    # Recover the original message m
    m = pow(m_e_mod_p, d, p)
    
    # Convert the long integer back to bytes
    msg = long_to_bytes(m)
    
    return msg

# Extracting the encrypted components
e = int(enc[0])
p = int(enc[1])
PT = enc[2]

# Ensure PT points are properly formatted as tuples
PT = [(int(a), int(b)) for a, b in PT]

# Decrypt the message
decrypted_msg = decrypt(e, p, PT)
print(f'decrypted message: {decrypted_msg}')