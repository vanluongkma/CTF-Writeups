from Crypto.Util.number import isPrime
import itertools

def reconstruct_full_value(masked_value, length):
    """
    Reconstruct the possible full value from the masked value.
    """
    possible_full_values = []

    # Generate all possible full values by filling in the masked digits
    for digits in itertools.product("0123456789", repeat=length):
        full_value = "".join(digits)
        if full_value[::2] == masked_value:
            possible_full_values.append(int(full_value))

    return possible_full_values

def find_primes(masked_p, masked_q, e, n):
    """
    Find possible primes p and q from their masked values.
    """
    length_p = len(masked_p) * 2  # Full length is twice the masked length
    length_q = len(masked_q) * 2

    possible_ps = reconstruct_full_value(masked_p, length_p)
    possible_qs = reconstruct_full_value(masked_q, length_q)

    for p in possible_ps:
        if isPrime(p):
            for q in possible_qs:
                if isPrime(q) and p != q:
                    return p, q

    return None, None

# Example masked results (replace with actual values)
masked_p = '27212682839330562867912869463364372917571755304412448953987184152058859363475658991885223173126836436227042631829451770281657188801132632754358573421476713'
masked_q = '17442410603282892723618602187529515359711740833730260149510807165116647546271374480187023501331151730764109747634675242379762827312400467020803390714945500'

# RSA parameters
e = 3
n = 626356193069850241095714430666797882761834354037291483886654036860221836671251841638463578359737190914757162420849474528846650079874078625978289176596617868273875322145600874926244542251323610808837860694245955675537296047908005697324988133667512181222313062877655710027850551903609314835996568001521756059717

# Find p and q
p, q = find_primes(masked_p, masked_q, e, n)

if p and q:
    print(f'Reconstructed p: {p}')
    print(f'Reconstructed q: {q}')
else:
    print('Unable to reconstruct p and q.')
