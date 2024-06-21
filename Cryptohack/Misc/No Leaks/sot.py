import base64
import telnetlib
import json

HOST = "socket.cryptohack.org"
PORT = 13370

tn = telnetlib.Telnet(HOST, PORT)


def readline():
	return tn.read_until(b"\n")

def json_recv():
	line = readline()
	return json.loads(line.decode())

def json_send(hsh):
	request = json.dumps(hsh).encode()
	tn.write(request)

print(readline())

# Keep track of all the possible values for every character in the flag
# The server will never send a correct one
start = 32
stop = 127
flag_possibilties = [
	set([chr(c) for c in range(start, stop)])
	for _ in range(20)
]
request = {
	'msg': 'request'
}

while(True):
	# continuously get encrypted flags
	json_send(request)
	response = json_recv()
	if 'error' in response:
		continue
	enc_flag = base64.b64decode(response['ciphertext'])
	done = True
	for f, r in zip(flag_possibilties, enc_flag):
		# Discard all the flags it gives us
		f.discard(chr(r))
		if len(f) > 1:
			done = False
	# sanity check
	assert 'c' in flag_possibilties[0]
	
	s = ''
	sum_ = 0
	for f in flag_possibilties:
		# There is no peek otherwise I would just use join()
		c = f.pop()
		f.add(c)
		s += c
		# keep track of the progress
		# when there is only one possibility in every entry, we are done
		sum_ += len(f)
	
	# calculate the progress
	avg_len = sum_/len(flag_possibilties)
	progress = 1 - avg_len/(stop-start)
	# print progress
	print(f'{progress*100:.2f}%\t', s, end='\r')
	if done:
		break
print(f'100.00%\t', s, end='\n')