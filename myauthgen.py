import numpy as np
import matplotlib.pyplot as plt
	
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
	
f = open(input("Enter in file name: "), 'w')
while 1:
	username = input("input username(stop to stop): ")
	if username == "stop":
		break
	password = input("input password: ")
	password = s_hash(password)
	f.write(username + ' ' + password.decode() + '\n')
	
f.close()