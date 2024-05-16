import sys
import string
import random
import hashlib
import time
import subprocess
import os

flag = 'KCSC{s0m3_r3ad4ble_5tr1ng_like_7his}'

NUM_TRIALS = 50
USE_POW = True

if USE_POW:
    # proof of work
    prefix = ''.join(random.choice(string.digits) for i in range(5))
    suffix = os.urandom(3).hex()
    print("Give me a string starting with \"{}\" (no quotes) so its sha256sum ends in {}".format(prefix, suffix), flush=True)
    l = input().strip()
    if not l.startswith(prefix) or hashlib.sha256(l.encode()).hexdigest()[-6:] != suffix:
        print("Nope.", flush=True)
        sys.exit(1)

for trial in range(NUM_TRIALS):
    print(f'KCSC Lottery v3: trial {trial+1}/{NUM_TRIALS}', flush=True)
    tick = time.time()
    p = subprocess.run(['node', 'lottery.js'])
    tock = time.time()
    if abs(tock-tick) > 15:
        print(f'⌛️❗️ ({tock-tick:.3f})', flush=True)
        sys.exit(1)
    if p.returncode != 42:
        print(f'🔮️🚫️❗️', flush=True)
        sys.exit(1)

print('congrats!', flush=True)
print(flag)
