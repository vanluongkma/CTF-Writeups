with open("log.txt") as f:
    lines = [line.strip() for line in f.readlines()]
p = int(lines[0])
msg = lines[1:]
g = 6
flag = ""
pos = 0
for ln in range(0, len(msg), 6 * 20):
    for i in range(ln, ln + 6 * 20, 6):    
        ga = int(msg[i].split(" ")[-1])
        b = int(msg[i+1].split(" ")[-1])
        gb = int(msg[i+2].split(" ")[-1])
        c = msg[i+3].split(" ")[-1]
        guess = int(msg[i+4].split(" ")[-1])
        if pow(ga, b, p) == guess:
            flag += c
            pos += 1
            break
    print(flag)