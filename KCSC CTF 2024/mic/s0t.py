from PIL import Image
import numpy as np
import galois
from tqdm import tqdm

GF256 = galois.GF(2**8)
img = Image.open('qr_flag_encrypt.png')
pixels = img.load()

width, height = img.size
x =  0 
y = 0
M = GF256([pixels[x, y], pixels[x, y+1], pixels[x, y+2]])
print(M)

for x in tqdm(range(width)):
    for y in tqdm(range(0,height,3)):
        A = GF256([pixels[x, y], pixels[x, y+1], pixels[x, y+2]])
        ans = np.subtract(A,M)
        pixels[x, y], pixels[x, y+1], pixels[x, y+2] = [tuple([int(i) for i in j]) for j in ans]
        M = A
        
img.save('qr_flag.png')