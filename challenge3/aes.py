#! python
"""
Name: Raven A. Alexander
Date: 2022-05-02
Description: This program implements the Rijndael algorithm to dictionary attack a given ciphertext.
"""
import re
from sys import stdin,stdout,argv,exit
from hashlib import sha256
from Crypto import Random
from Crypto.Cipher import AES
from math import floor

NOT_TEXT = True # set true if file is not text
BLOCK_SIZE = 16 # the AES block size to use
PAD_WITH = "#" # padding character for plaintext
THRESHOLD = .75 
DICT = 'dictionary.txt' #dictionary4, dictionary1-3, dictionary5
FILE_TYPE = b'%PDF-1.4' # file header to look for
FILTER = b"" # comment out if no filter or replace with ""

def simp_dict(dict:list):
	"""Simplifies dictionary."""
	new_dict=[]
	for word in dict:
		new_dict.append(word.decode().lower())
	return new_dict

def get_keys()->list[str]:
	"""Get a list of words from a file."""
	k = []
	with open(DICT,'rb') as f:
		k = f.read().split(b'\n')
	return k

def simp_keys(k:list[bytes])->list[bytes]:
	sk = []
	for i in k:
		if i.lower().startswith(b'j'):
			sk.append(i)
	return sk

def _checkValid(p:str,dict:list)->bool:
	v = 0
	filter_p = re.split(r'\n| ',p)
	while(filter_p.count("")):
		filter_p.remove('')
	for word in filter_p:
		if word.strip("`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/?").lower() in dict:
			continue
		else:
			v+=1
		if ((len(filter_p)-float(v))/len(filter_p)<THRESHOLD):
			return False
	return True

def decrypt(text:bytes, k:list[bytes])->tuple:
	"""Dictionary attack a given AES encrypted cipher(text) with a given list of keys(k)."""
	# get iv
	iv = text[:16]

	# get partition for plaintext
	index = floor(len(text[16:])*3/4)
	if index > 480: index = 480

	# simplified dictionary to be used for parsing
	dictionary = simp_dict(k)

	# simplify key list with filter
	try:
		if (FILTER != b""):
			k = simp_keys(k)
	except:
		pass

	plain = ""
	for i in k:
		# hash the key (SHA-256) to ensure that it is 32 bytes long
		key = sha256(i).digest()
		
		# decrypt the ciphertext with the key using CBC block cipher mode
		cipher = AES.new(key,AES.MODE_CBC,iv)

		# the ciphertext is after the IV (so, skip 16 bytes)
		plain = cipher.decrypt(text[16:])

		# check if valid plaintext
		if NOT_TEXT:
			if (FILE_TYPE in plain[:10]): return plain,i
		else:	
			temp = plain.decode('utf-8','ignore')[16:index]
			if _checkValid(temp,dictionary): return plain,i
			
def encrypt(plaintext: bytes, key: bytes)->str:

	pad = bytes(PAD_WITH,'utf-8')
	# hash the key (SHA-256) to ensure that it is 32 bytes long
	key = sha256(key).digest()
	# generate a random 16-byte IV
	iv = Random.new().read(BLOCK_SIZE)

	# encrypt the ciphertext with the key using CBC block cipher mode
	cipher = AES.new(key, AES.MODE_CBC, iv)
	# if necessary, pad the plaintext so that it is a multiple of BLOCK SIZE in length
	plaintext += (BLOCK_SIZE - len(plaintext) % BLOCK_SIZE) * pad
	# add the IV to the beginning of the ciphertext
	# IV is at [:16]; ciphertext is at [16:]
	ciphertext = iv + cipher.encrypt(plaintext)

	return ciphertext

if __name__ == "__main__":
	try:
		if argv[1] == '-h':
			print("""This program brute forces aes encryption using a dictionary attack.\n./aes.py --options\n-e : encrypt with aes. Must pass a key as the next options as follows:\n\t./aes.py -e [key]\n-d : decrypt with aes. Ensure the dictionary name is correct inside of the program""")
			exit()
			
		elif argv[1] == '-d':
			try:
			# get keys from dictionary
				keys = get_keys()
			except:
				print('[!] Parsing dictionary failed. Ensure the dictionary is inside the same directory as the program and that it is named correctly.')
				exit()

			ciphertext = stdin.buffer.read().rstrip(b"\n")

			# decrypt
			plaintext,key = decrypt(ciphertext,keys)

			# if file is anything other than text
			if NOT_TEXT:
				p = plaintext.strip(bytes(PAD_WITH,'utf-8'))
				stdout.write(f"KEY={key.decode()}\n")
				stdout.buffer.write(p)
			else:
				p = plaintext.decode('utf-8','ignore')
				if p[-1] == PAD_WITH: p=p.strip(PAD_WITH)
				stdout.write(f"KEY={key.decode()}\n{p}")	

		elif argv[1] == '-e':
			key = argv[2].encode()

			plaintext = stdin.buffer.read().rstrip(b"\n")

			ciphertext = encrypt(plaintext,key)

			stdout.buffer.write(ciphertext)

	except IndexError as e:
		print(e,'\nUse -h for help.',end='')
		exit()