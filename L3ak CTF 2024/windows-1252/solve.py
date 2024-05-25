import pytesseract
from PIL import Image
import skimage
from base64 import b64decode
from pwn import *
from io import BytesIO
import numpy as np
import skimage

tess = r'D:\Tools\Scoop\shims\tesseract.exe'

p = remote('35.229.44.203', 6666)

p.recvuntil(b'> ')
p.sendline(b'1')

p.recvuntil(b': ')

b64 = p.recvline()
png_data = b64decode(b64.strip())
image = Image.open(BytesIO(png_data))

image.save("test.png")

p.interactive()
