#sender
import sys
from bitstring import BitArray
from itertools import cycle
import socket
import hashlib
mimetable = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']
_KEY = open(input("Enter in key filename: "), 'rb')

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
	decoded = ""
	for s_8i in s_8bits:
		decoded += chr(s_8i)
	return bytes(decoded, 'utf-8')

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
	
def send(s, ascii_armor=False, hash=True, verbose=False, showascii=False):
	if verbose:
		print("sending data: " + str(s))
	if type(s) is not bytes and type(s) is not bytearray:
		s = bytes(s, 'utf-8')
	if hash:
		hashed = s_hash(s)
		#print("with hash: " + str(hashed))
		#print(type(s), type(hashed))
		s_and_hash = s + b"*HASH*" + hashed
		encrypted = xor_encrypt(s_and_hash, key=_KEY)
	else:
		encrypted = xor_encrypt(s, key=_KEY)
	if ascii_armor:
		tosend = b"ascii_armor=True, " + mimeencode(encrypted)
	else:
		tosend = b"ascii_armor=Fals, " + encrypted
	if showascii:
		print("sending data (in ascii form): " + str(tosend))
	#print("size of send: " + str(len(tosend)))#debug
	sock.send(tosend)
	
def recv(failtest=False, nonempty=False):
	msg = sock.recv(4096)
	if not msg:
		if nonempty:
			while not msg:
				msg = sock.recv(4096)
		else:
			return b"complete"
	if failtest:
		return b"*HASHING FAILED*"
	chunks = msg.split(b"ascii_armor=")
	chunks = [chunks_i for chunks_i in chunks if chunks_i != b""]
	armors = [chunks_i[:4] for chunks_i in chunks]
	chunks = [chunks_i[6:] for chunks_i in chunks]
	i = 0
	while i < len(chunks):
		if armors[i] == b"True":
			chunks[i] = mimedecode(chunks[i])
		i += 1
	chunks = [xor_encrypt(chunks_i, _KEY) for chunks_i in chunks]
	rcvd_hashes = [chunks_i[chunks_i.find(b"*HASH*")+6:] for chunks_i in chunks]
	msgs = [chunks_i[:chunks_i.find(b"*HASH*")] for chunks_i in chunks]
	new_hashes  = [s_hash(msgs_i) for msgs_i in msgs]
	hash_checks = [nhi == rhi for nhi, rhi in zip(new_hashes, rcvd_hashes)]
	finalmsg = bytearray()
	[finalmsg.extend(msgs_i) for msgs_i in msgs]
	if False in hash_checks:
		return b"*HASHING FAILED*"
	return finalmsg

def login():
	username = input("Enter username: ")
	password = input("Enter password: ")
	send(username)
	send(password)
	response = recv()
	print(response.decode())
	return response == b"login successful"
	
def sendrequest(request):
	send(request)
	response = recv(nonempty=True)
	if response == b"accept":
		filenamed = recv(nonempty=True)
	print("" + str(response[:]))
	return response == b"accept"
		
def sendfile(command, tries=0, ascii_armor=False, verbose=False, showascii=False):
	filename = command.split()[1]
	if tries > 0:
		f = open(filename, 'rb')
		print("Sending failed, retrying. Attempt #" + str(tries))
	else:
		failed = True
		while failed:
			try:
				f = open(filename, 'rb')
				failed = False
			except FileNotFoundError:
				failed = True
				retry = input("File not found, would you like to retry? (y/n) ")
				if retry != 'y':
					return "FNF"
				filename = input("Enter file name: ")
		if not sendrequest(command):
			sys.exit()
		ascii_armor = input("Would you like to ascii armor chunks? (y/n) ")
		if ascii_armor == 'y':
			ascii_armor = True
		else:
			ascii_armor = False
	readsize = 4032
	if ascii_armor:
		readsize = 3005
	chunk = f.read(readsize)
	retry = False
	print("Sending file...")
	while chunk:
		send(chunk, ascii_armor=ascii_armor, verbose=verbose, showascii=showascii)
		response = recv(nonempty=True)#receive a nonempty response with instructions
		retrycount = 0
		while response == b"retry":
			retrycount += 1
			print("*HASHING FAILED*, retrying. Attempt #" + str(retrycount))
			send(chunk, ascii_armor=ascii_armor, verbose=verbose, showascii=showascii)
			response = recv(nonempty=True)
			if response == b"stop":
				f.close()
				print("Maximum number of retries exceeded. File send failed.")
				return False
		chunk = f.read(readsize)
		if not chunk:
			chunk = "end of file"
		if response == b"success":
			print("File successfully sent.")
			f.close()
			return True
	
sock = socket.socket()
host = input("Enter in host name: ")
port = 12345
sock.connect((host, port))
logged_in = False
command = ""
while command != "disconnect" and command != "failure":
	command = input("Enter command: ")
	if command == "login":
		send(command)
		logged_in = login()
	elif command.startswith("send") and logged_in:
		success = sendfile(command, verbose=("-v" in sys.argv), showascii=("-sa" in sys.argv))
		if type(success) is not str:
			sys.exit()
	else:
		send(command)
		print(str(recv().decode()))
		