# from sympy import symbols, Eq, solve
# import math

# # Known values
# e = 3
# c = 241770216610682199125137534490833365336381994085836826001094932013052758251077284104377640305129489215818589015524930537584522589702172966258812852133149114945582729507431141623719338534240447537727090195880376544398326675880609206966977525544630838499583739148184807302251026006808274011648896499843914218393

# # Masked results from the server (only even-indexed digits)
# masked_results = {
#     '-p': '4225025479808829913572482938069431309064901145164208996072776077131233761783838532276774428366090413629973481583915482981801166464411385908031999612947260',
#     '-q': '24628849465188417459896519896860135206537250025695828921731185042264967186554789270766941554455245547951710159963827482740089119281501867873585443046957695',
#     'p': '15410671673247672713566928873767325273562473551618511803138792719390830757548273205332435332276403185271512937958463191588274760043692727988969912891102275',
#     'q': '17702245835516036226425712211935551274432224824135788330657564890496921283974842488742089753539439015436484687619909681775699836507806983619903991034106152',
#     'p+q': '33222916418754609040981741095702877558004708376754399134885366500796761031412126693084524096815832191608997625567362883363963597651499610697973914935209437',
#     'p*q': '0',  # This suggests p or q might be too small or there was an issue
#     'p%q': '15410671673247672713566928873767325273562473551618511803138792719390830757548273205332435332276403185271512937958463191588274760043692727988969912891102275',
#     'p//q': '0'  # This also suggests an issue or unhelpful result
# }

# def reconstruct_full_value(masked_value, length):
#     # Attempt to reconstruct the full number from the masked (even-indexed digits) result
#     possible_full_values = []
#     for odd_digit in range(10):
#         # Construct full number
#         full_value = [''] * (length * 2)
#         full_value[::2] = masked_value
#         full_value[1::2] = [str(odd_digit)] * len(masked_value)
#         possible_full_values.append(int(''.join(full_value)))
#     return possible_full_values

# def validate_full_value(full_value, expressions):
#     # Validate the full values against the given ciphertext
#     for expr in expressions:
#         res = eval(expr)
#         if pow(res, e, n) == c:
#             return res
#     return None

# # Recover p and q directly from masked results
# p_value = int(masked_results['p'])
# q_value = int(masked_results['q'])

# # Compute n
# n = p_value * q_value

# # Print computed n
# print(f"Recovered n: {n}")


# from Crypto.Util.number import long_to_bytes, inverse
# from sympy import symbols, Eq, solve

# # Given values
# masked_results = {
#     'p': '27212682839330562867912869463364372917571755304412448953987184152058859363475658991885223173126836436227042631829451770281657188801132632754358573421476713',
#     'q': '17442410603282892723618602187529515359711740833730260149510807165116647546271374480187023501331151730764109747634675242379762827312400467020803390714945500',
#     '-p': '38200097575700115914411561323232249443010697435908638696567102347749448553492075730675563288317242953708423794668516427076463044785437657739775722179799854',
#     '-q': '48070269701857885058725729608087015001779693906580906591923479334681651370686349351273762840192927650161365578753491045997358305375179722463221005987230077',
#     '-p - q': '11767686861427213280803869235613733183208847591177467547946294281532791016210791359487439676976091223943313946933930274706600116473036189618962432455853254',
#     '-p + q': '56743418179093017738039163501752755702722348268738999836087009412866085109763450210862586890748303684462622542293181770456225972098837115859589113994745354',
#     'p + q': '45755003543623364580520461651893888277383596238243719093508981227175406809747922372073256785557097167082251389554136923661410016114533190874162964246322313',
#     'p % q': '10770261236047660043304167275744866658769005560682277804466276087931202717194273511698209562785775606462942883194885528811895260599732174633545282707430213',
#     'p // q': '1',
#     'p * q': '0',  # This suggests p or q might be too small or there was an issue
#     '-p * q': '0'
# }

# # Decryption parameters
# e = 3
# c = 74777606227461956889771614759108018225860449460616378216552369417296767205273338346791374528263030651040166096573892453226402987876892977873269105663723635661343236734596620651154246738986433226563951268258998755169764030666851201256359293124577009275941159245849910125751058589572484504006872372726098805777

# # Reconstruct the full values from masked results
# def reconstruct_full_value(masked_value, length):
#     possible_full_values = []
#     for odd_digit in range(10):
#         full_value = [''] * (length * 2)
#         full_value[::2] = masked_value
#         full_value[1::2] = [str(odd_digit)] * len(masked_value)
#         possible_full_values.append(int(''.join(full_value)))
#     return possible_full_values

# # Possible lengths for the result
# lengths = {
#     'p': len(masked_results['p']),
#     'q': len(masked_results['q']),
#     '-p': len(masked_results['-p']),
#     '-q': len(masked_results['-q']),
#     '-p - q': len(masked_results['-p - q']),
#     '-p + q': len(masked_results['-p + q']),
#     'p + q': len(masked_results['p + q']),
#     'p % q': len(masked_results['p % q']),
#     'p // q': len(masked_results['p // q']),
#     'p * q': len(masked_results['p * q']),
#     '-p * q': len(masked_results['-p * q'])
# }

# # Recover p and q from masked results
# possible_p_values = reconstruct_full_value(masked_results['p'], lengths['p'])
# possible_q_values = reconstruct_full_value(masked_results['q'], lengths['q'])

# # Try each possible pair of p and q
# for p_candidate in possible_p_values:
#     for q_candidate in possible_q_values:
#         if p_candidate == q_candidate:
#             continue
#         n_candidate = p_candidate * q_candidate
#         if n_candidate == 0:
#             continue

#         try:
#             # Test the calculated n with the encrypted message
#             decrypted_message = pow(c, inverse(e, n_candidate), n_candidate)
#             print(f"Possible n: {n_candidate}")
#             print(f"Decrypted message: {long_to_bytes(decrypted_message).decode('utf-8')}")
#         except Exception as e:
#             print(f"Failed with n: {n_candidate}, error: {e}")



# from sympy import mod_inverse, isprime
# from itertools import product
# import math

# # Hàm khôi phục giá trị từ mặt nạ
# def unmask(masked_value, e, n):
#     length = len(masked_value)
#     candidates = []
    
#     for i in range(0, length, 2):
#         try:
#             candidate = int(masked_value[i:i+2])
#             candidates.append(candidate)
#         except ValueError:
#             continue
    
#     for value in candidates:
#         try:
#             original_value = pow(value, mod_inverse(e, n), n)
#             return original_value
#         except:
#             pass
    
#     return None

# # Hàm kiểm tra điều kiện
# def check_conditions(p, q, masked_p, masked_q, masked_p_plus_q, masked_p_mod_q):
#     try:
#         assert unmask(masked_p, e, n) == p
#         assert unmask(masked_q, e, n) == q
#         assert (p + q) == unmask(masked_p_plus_q, e, n)
#         assert (p % q) == unmask(masked_p_mod_q, e, n)
#         return True
#     except AssertionError:
#         return False

# # Hàm áp dụng BPA
# def branch_and_prune(masked_p, masked_q, masked_p_plus_q, masked_p_mod_q, e):
#     possible_values = []
    
#     # Giả sử rằng các giá trị p, q nằm trong một khoảng nhất định
#     for p_candidate in range(2**512, 2**513):
#         for q_candidate in range(2**512, 2**513):
#             if p_candidate != q_candidate and isprime(p_candidate) and isprime(q_candidate):
#                 if check_conditions(p_candidate, q_candidate, masked_p, masked_q, masked_p_plus_q, masked_p_mod_q):
#                     possible_values.append((p_candidate, q_candidate))
                    
#     return possible_values

# # Các mặt nạ của p, q, p + q và p % q
# masked_p = '27212682839330562867912869463364372917571755304412448953987184152058859363475658991885223173126836436227042631829451770281657188801132632754358573421476713'
# masked_q = '17442410603282892723618602187529515359711740833730260149510807165116647546271374480187023501331151730764109747634675242379762827312400467020803390714945500'
# masked_p_plus_q = '45755003543623364580520461651893888277383596238243719093508981227175406809747922372073256785557097167082251389554136923661410016114533190874162964246322313'
# masked_p_mod_q = '10770261236047660043304167275744866658769005560682277804466276087931202717194273511698209562785775606462942883194885528811895260599732174633545282707430213'

# e = 3

# # Khôi phục các giá trị p, q
# possible_values = branch_and_prune(masked_p, masked_q, masked_p_plus_q, masked_p_mod_q, e)
# print(f"Các giá trị khả thi của (p, q): {possible_values}")


# from Crypto.Util.number import getPrime, inverse, long_to_bytes

# # Given ciphertext c
# c = 12345678901234567890  # replace with actual value

# # Example of guessed expressions
# expressions = ["p", "q", "p+q", "p-q", "p*q"]

# def eval_expression(expr, p, q):
#     r = eval(expr)
#     return str(pow(r, 3, p * q))[::2]

# # Guess possible values for p and q
# for p in range(2**512, 2**513):
#     for q in range(2**512, 2**513):
#         if (p-1) % 3 == 0 and (q-1) % 3 == 0:
#             n = p * q
#             phi_n = (p-1) * (q-1)
#             try:
#                 d = inverse(3, phi_n)
#                 m = pow(c, d, n)

#                 flag = long_to_bytes(m).decode()
#                 print(f"Possible FLAG: {flag}")
#             except:
#                 pass


from sympy import isprime
from Crypto.Util.number import long_to_bytes, bytes_to_long

def find_possible_values(masked_value, e, n):
    """
    Given a masked value, this function attempts to find all possible full values
    that could match the masked value.
    """
    length = len(masked_value)
    possible_values = []

    # Attempt to reconstruct the possible full values
    for i in range(10**length):
        full_value = str(i).zfill(length * 2)  # Make sure it's of appropriate length
        if full_value[::2] == masked_value:
            possible_values.append(int(full_value))

    return possible_values

def find_p_and_q(masked_p, masked_q, e, n):
    """
    Given masked values for p and q, find possible candidates for p and q.
    """
    possible_p = find_possible_values(masked_p, e, n)
    possible_q = find_possible_values(masked_q, e, n)
    
    # Validate candidates
    for p in possible_p:
        for q in possible_q:
            if p != q and isprime(p) and isprime(q):
                return p, q

    return None, None

# Example masked results (replace with your actual masked values)
masked_p = '27212682839330562867912869463364372917571755304412448953987184152058859363475658991885223173126836436227042631829451770281657188801132632754358573421476713'
masked_q = '17442410603282892723618602187529515359711740833730260149510807165116647546271374480187023501331151730764109747634675242379762827312400467020803390714945500'

# Constants
e = 3
n = 626356193069850241095714430666797882761834354037291483886654036860221836671251841638463578359737190914757162420849474528846650079874078625978289176596617868273875322145600874926244542251323610808837860694245955675537296047908005697324988133667512181222313062877655710027850551903609314835996568001521756059717

# Find p and q
p, q = find_p_and_q(masked_p, masked_q, e, n)

if p and q:
    print(f'Reconstructed p: {p}')
    print(f'Reconstructed q: {q}')
else:
    print('Unable to reconstruct p and q.')
