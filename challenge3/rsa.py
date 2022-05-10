#! python
"""
Name: Raven A. Alexander
Date: 2022-05-02
Description: This program implements the Rijndael algorithm to dictionary attack a given ciphertext.
"""
from os import remove
from typing import BinaryIO
from PyPDF2 import PdfFileReader
import re
from sys import stdin,stdout,argv,exit
from hashlib import sha256
from Crypto import Random
from Crypto.Cipher import AES
from math import floor
import magic

# the AES block size to use
BLOCK_SIZE = 16
# the padding character to use to make the plaintext a multiple of BLOCK_SIZE in length
PAD_WITH = "#"
THRESHOLD = .75
DICT = 'dictionary5.txt' #dictionary4, dictionary1-3, dictionary5

def checkFile(p:bytes)->str:
	"""Returns file type of bytes"""
	return magic.from_buffer(p)

def simp_dict(dict:list):
	"""Simplifies dictionary."""
	new_dict=[]
	for word in dict:
		new_dict.append(word.decode().lower())
	return new_dict

def get_keys()->list[str]:
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

def _checkPDF(f:str)-> None:
	"""Attempts to read pdf. If an error occurs the check failed."""
	PdfFileReader(open(f,'rb'))

def decrypt(text:BinaryIO, k:list[bytes]):
	iv = text[:16]
	# ensurses the partitioned cipher is a factor of block size
	index = floor(len(text[16:])*3/4)
	if index > 480: index = 480

	# simplified dictionary to be used for parsing
	dictionary = simp_dict(k)
	# simplify key list for cipher4
	if DICT == 'dictionary4.txt':
		k = simp_keys(k)

	plain = ""
	fkey=""
	for i in k:
		# hash the key (SHA-256) to ensure that it is 32 bytes long
		key = sha256(i).digest()
		
		# decrypt the ciphertext with the key using CBC block cipher mode
		cipher = AES.new(key,AES.MODE_CBC,iv)

		# the ciphertext is after the IV (so, skip 16 bytes)
		plain = cipher.decrypt(text[16:])

		# get filetype
		file_type=re.split(r' |\n|\\|/|\t',checkFile(plain))[0]
		# check if pdf
		if ('PDF' in file_type):
			filename = f"{k.index(i)}.{file_type.lower()}"
			with open(filename,'wb') as file:
				file.write(plain.strip(bytes(PAD_WITH,'utf-8')))
			try:
				_checkPDF(filename)
				fkey = i
				remove(filename)
				return plain,fkey
			except:
				remove(filename)
				continue
		else:	
			temp = plain.decode('utf-8','ignore')[16:index]
			if _checkValid(temp,dictionary):
				fkey = i
				return plain,fkey
			
def encrypt(plaintext: BinaryIO, key: bytes):

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
			print("""This program brute forces rsa encryption using a dictionary attack.\n./rsa.py --options\n-e : encrypt with rsa. Must pass a key as the next options as follows:\n\t./rsa.py -e [key]\n-d : decrypt with rsa. Ensure the dictionary name is correct inside of the program""")
			exit()
	except IndexError as e:
		print(e,'\nUse -h for help.',end='')
		exit()

	try:
		if argv[1] == '-d':
			try:
			# get keys from dictionary
				keys = get_keys()
			except:
				print('[!] Parsing dictionary failed. Ensure the dictionary is inside the same directory as rsa.py and that it is named correctly inside of rsa.py.')
				exit()

			# get ciphertext from stdin
			ciphertext = stdin.buffer.read().rstrip(b"\n")

			# decrypt
			plaintext,key = decrypt(ciphertext, keys)

			# decode plaintext and ignore non decipherable characters
			p = plaintext.decode('utf-8','ignore')
			
			# remove padding
			if p[-1] == PAD_WITH:
				p=p.strip(PAD_WITH)

			# display
			stdout.write(f"KEY={key.decode()}\n{p}")	

		elif argv[1] == '-e':
			key = argv[2].encode()

			plaintext = stdin.buffer.read().rstrip(b"\n")

			ciphertext = encrypt(plaintext,key)

			stdout.buffer.write(ciphertext)
	except IndexError as e:
		print(e,'\nUse -h for help.',end='')
		exit()