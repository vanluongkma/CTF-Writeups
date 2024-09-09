from Crypto.Util.number import long_to_bytes
from ast import literal_eval
from tqdm import tqdm

flag= ''
x = 106276637345585586395178695555113419125706596151484787339368729136766801222943
for i in tqdm(range(407)):
    with open(f"Log/output_{i}.txt", 'r') as f:
        lines = f.readlines()
    w = int(lines[1].split('=')[1].strip()) 
    pairs = [literal_eval(lines[3 + i].strip()) for i in range(407)] 
    _ = literal_eval(lines[410].split('=')[1].strip()) 
    responses = [literal_eval(line.strip()) for line in lines[412:]]          
    for idx, response in enumerate(responses):
        if isinstance(response, int): 
            a = pairs[idx][0]
            if pow(response, 2, x) == (w * a) % x:
                flag += '0'
            else:
                flag += '1'
            break
print(long_to_bytes(int(flag[::-1], 2)))