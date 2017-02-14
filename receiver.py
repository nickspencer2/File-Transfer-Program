#receiver
import sys
from itertools import cycle
from bitstring import BitArray
import socket
import hashlib
mimetable = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']
_KEY = open(input("Enter in key filename: "), 'rb')
FILE_NAME = "myauth.txt"
FN = input("Enter authentication file name: ")
if FN != "":
	FILE_NAME = FN
print("Using authentication file " + FILE_NAME)



def mimeencode(s, debug=False):
	if type(s) is not bytearray and type(s) is not bytes:
		s = bytearray(s, 'utf-8')
	s = BitArray(s)
	s = list(s)
	pad = len(s)
	while len(s)%24 != 0:
		s.append(False)
	s_6bits = []
	padded = []#list of chars resulting entirely from padding
	j = 0
	for i in range(0, len(s), 6):
		s_6bits.append(s[i:i+6])
		if i >= pad - 1:
			padded.append(j)
		j += 1
	encoded = ""
	for i in range(len(s_6bits)):
		if i not in padded:
			a = ""
			for j in range(len(s_6bits[i])):
				a += str(int(s_6bits[i][j]))
			a = int(a, 2)
			encoded += mimetable[a]
		else:
			encoded += "="
	return bytes(encoded, 'utf-8')
	
def mimedecode(s, debug=False):
	if type(s) is bytes or type(s) is bytearray:
		s = str(s)[2:-1]
	s = str(s)
	s2 = [mimetable.index(c) for c in s if c != "="]
	sbits = [bin(s2i)[2:] for s2i in s2]
	s_6bits = ""
	for sbi in sbits:
		a = ""
		if len(sbi) < 6:
			a = "0"*(6-len(sbi))
		s_6bits += a + str(sbi)
	s_8bits = [int(s_6bits[i:i+8], 2) for i in range(0, len(s_6bits), 8) if i+8<=len(s_6bits)]
	decoded = bytearray()
	for s_8i in s_8bits:
		decoded.append(s_8i)
	return decoded

def s_hash(s=""):
	while len(s) < 20:
		if type(s) is not bytes and type(s) is not bytearray:
			sbits = s.encode()
		else:
			sbits = s
		i = 0
		j = 0
		if len(sbits) > 20:
			h_bits = [0]*20
			for c in sbits:
				h_bits[i%len(h_bits)] += ((c + i)**2)
				h_bits[i%len(h_bits)] =  h_bits[i%len(h_bits)]%240 + 16
				i += 1
		else:
			h_bits = [0]*len(sbits)
			for c in sbits:
				h_bits[i] = ((c + i)**2)
				h_bits[i] = h_bits[i]%240 + 16
				i += 1

		h_string = b""
		for h in h_bits:
			h_string += bytes('{0:x}'.format(h), 'utf-8')
		if len(s) < 20:
			s = h_string
	if len(s) >= 20:
		if type(s) is not bytes and type(s) is not bytearray:
			sbits = s.encode()
		else:
			sbits = s
		i = 0
		j = 0
		if len(sbits) > 20:
			h_bits = [0]*20
			for c in sbits:
				h_bits[i%len(h_bits)] += ((c + i)**2)
				h_bits[i%len(h_bits)] =  h_bits[i%len(h_bits)]%240 + 16
				i += 1
		else:
			h_bits = [0]*len(sbits)
			for c in sbits:
				h_bits[i] = ((c + i)**2)
				h_bits[i] = h_bits[i]%240 + 16
				i += 1

		h_string = b""
		for h in h_bits:
			h_string += bytes('{0:x}'.format(h), 'utf-8')
		if len(s) < 20:
			h_string = my_hash2(h_string)
		return h_string
	return s
	
def xor_file_encrypt(data, key):
	key_as_bytes = key.read(len(data))
	key.seek(0, 0)
	kabl = len(key_as_bytes)
	return bytearray(((data[i] ^ key_as_bytes[i%kabl]) for i in range(0,len(data))))
	
def xor_encrypt(data, key): 
	# result = bytearray()
	# dataisbyteformat = type(data) is bytes or type(data) is bytearray
	# keyisbyteformat  = type(key) is bytes or type(key) is bytearray
	#if type(key) is _io.BufferedReader:
	return xor_file_encrypt(data, key)
	# print("data: " + str(dataisbyteformat))
	# print("key : " + str(type(key)))
	# if dataisbyteformat and keyisbyteformat:
		# result.extend(a^b for a,b in zip(data, cycle(key)))
	# elif dataisbyteformat and not keyisbyteformat:
		# result.extend(a^ord(b) for a,b in zip(data, cycle(key)))
	# elif not dataisbyteformat and type(key) is keyisbyteformat:
		# result.extend(ord(a)^b for a,b in zip(data, cycle(key)))
	# else:	
		# result.extend(ord(a)^ord(b) for a,b in zip(data, cycle(key)))
	# return result

	
def send(s, ascii_armor=False, hash=True):
	if type(s) is not bytes and type(s) is not bytearray:
		s = bytes(s, 'utf-8')
	if hash:
		hashed = s_hash(s)
		s_and_hash = s + b"*HASH*" + hashed
		encrypted = xor_encrypt(s_and_hash, key=_KEY)
	else:
		encrypted = xor_encrypt(s, key=_KEY)
	if ascii_armor:
		tosend = b"ascii_armor=True, " + mimeencode(encrypted)
	else:
		tosend = b"ascii_armor=Fals, " + encrypted
	sender.send(tosend)
	
def recv(failtest=False, nonempty=False, verbose=False, showascii=False):
	msg = sender.recv(4096)
	if not msg:
		if nonempty:
			while not msg:
				msg = sender.recv(4096)
		else:
			return b"complete"
	if failtest:
		return b"*HASHING FAILED*"
	chunks = msg.split(b"ascii_armor=")
	chunks = [chunks_i for chunks_i in chunks if chunks_i != b""]
	armors = [chunks_i[:4] for chunks_i in chunks]
	chunks = [chunks_i[6:] for chunks_i in chunks]
	i = 0
	if showascii:
		print("received data (in ascii form): " + str(chunks[:]))
	while i < len(chunks):
		if armors[i] == b"True":
			chunks[i] = mimedecode(chunks[i])
		i += 1
	chunks = [xor_encrypt(chunks_i, _KEY) for chunks_i in chunks]
	if verbose:
		print("received data: " + str(chunks))
	rcvd_hashes = [chunks_i[chunks_i.find(b"*HASH*")+6:] for chunks_i in chunks]
	msgs = [chunks_i[:chunks_i.find(b"*HASH*")] for chunks_i in chunks]
	new_hashes  = [s_hash(msgs_i) for msgs_i in msgs]
	hash_checks = [nhi == rhi for nhi, rhi in zip(new_hashes, rcvd_hashes)]
	finalmsg = bytearray()
	[finalmsg.extend(msgs_i) for msgs_i in msgs]
	if False in hash_checks:
		return b"*HASHING FAILED*"
	return finalmsg


def login(username, password, filename=FILE_NAME):
	password = s_hash(password)
	if type(username) is not bytes and type(username) is not bytearray:
		username = bytes(username, 'utf-8')
	f = open(filename, 'rb')
	for line in f:
		if line.find(username) != -1:#username found
			if line.find(password) != -1:#password found on same line as username
				return True
			else:
				return False
	return False
	
def filesendrequest(filename):
	accept = input(str(sender_address) + " wants to send you file " + str(filename) + ". Would you like to (accept/decline)? ")
	send(accept)
	if accept == "accept":
		newfilename = input("Enter in what you would like to name the file: ")
		send(newfilename)
		return True, newfilename
	return False, None
	
	
def recvfile(sender_command, filename="", tries=0, failtest=False, verbose=False, showascii=False):
	filename = sender_command.split()[1]
	accept, newfilename = filesendrequest(filename)
	if not accept:
		sys.exit()
	f = open(newfilename, 'wb')
	printloading = True
	while 1:
		data = recv(nonempty=True, failtest=failtest, verbose=verbose, showascii=showascii)#get nonempty chunk
		if printloading:
			print("Receiving file...")
			printloading = False
		retrycount = 0
		while data == b"*HASHING FAILED*" and retrycount <= 3:
			retrycount += 1
			print("*HASHING FAILED*, retrying. Attempt #" + str(retrycount))
			send("retry")
			#data = recv(nonempty=True, verbose=verbose, showascii=showascii)#retry data receipt#if fail test, then will perform partial hash fail test
			data = recv(nonempty=True, failtest=failtest, verbose=verbose, showascii=showascii)#if fail test, then will perform full hash fail test
		if retrycount > 3:
			print("Stopping transfer due to exceeding retries.")
			send("stop")
			print("Maximum number of retries exceeded. File receive failed.")
			f.close()
			return False
		if data.find(b"end of file") != -1:
			f.write(data.strip(b"end of file"))
			f.close()
			break
		send("cont")
		f.write(data)
	send("success")
	print("File successfully received.")
	return True

sock = socket.socket()
host = socket.gethostname()
print("Welcome, " + str(host))
port = 12345
sock.bind(('0.0.0.0', port))
sock.listen(5)
sender, sender_address = sock.accept()
print(str(sender_address) + " connected.")
sender_command = ""
logged_in = False
while sender_command != "disconnect":
	sender_command = recv()
	print("sender: " + sender_command.decode())
	if sender_command.startswith(b"login"):
		username = recv()
		password = recv()
		success = login(username, password)
		if success:
			logged_in = True
			send("login successful")
		else:
			logged_in = False
			send("login unsuccessful")
	elif sender_command.startswith(b"send") and logged_in:
		success = recvfile(sender_command, failtest=("-hf" in sys.argv), verbose=("-v" in sys.argv), showascii=("-sa" in sys.argv))
		sys.exit()
	elif sender_command.startswith(b"disconnect"):
		sys.exit()
	else:
		send("Invalid command or access denied.")
		




