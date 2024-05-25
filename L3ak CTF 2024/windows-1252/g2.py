from pil import Image

img = Image.open(r"download.png")
px = img.load()

def getblock(n0,n1,n2,n3):
    block = []
    for i in range(n0,n1):
        for j in range(n2,n3):
            r, g, b, a= px[i,j]
            block.append("[" + str(r) + "," + str(g) + "," + str(b) + "]")
    return block

block0 = getblock(0, 24, 0, 24)

with open ("rgb.txt", "w") as f:
    for i in range(24):
        for j in range(24):
            f.write(block0[24*i + j] + " ")
        f.write("\n")
            
with open("rgb.txt","r") as f:
    lines = f.readlines()
    width = len(lines)
    tmp = lines[1].split(" ")
    length = len(tmp) - 1
        
imgsize = (width,length)
img = Image.new("RGB", imgsize)
pix = img.load()
for i in range (width):
    temp = lines[i].split(" ")
    for j in range (length):
        temp[j] = temp[j].replace('[','')
        temp[j] = temp[j].replace(']','')
        t = temp[j].split(",")
        t2 = (int(t[0]), int(t[1]), int(t[2]))
        pix[i, j] = t2
img.save("flag.png")