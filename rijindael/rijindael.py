#! python
"""
Name: Raven A. Alexander
Date: 2022-05-02
Description: This program implements the Rijndael algorithm to brute force a given ciphertext.
"""
from os import remove
from PyPDF2 import PdfFileReader
import re
from sys import stdin
from hashlib import sha256
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode
from math import floor
import magic

# the AES block size to use
BLOCK_SIZE = 16
# the padding character to use to make the plaintext a multiple of BLOCK_SIZE in length
PAD_WITH = "#"
THRESHOLD = .75

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
	with open('dictionary5.txt','rb') as f:
		k = f.read().split(b'\n')
	return k

def _checkValid(p:str,dict:list)->bool:
	v = 0
	filter_p = re.split(r'\n| ',p)
	while(filter_p.count("")):
		filter_p.remove('')
	for word in filter_p:
		if word.strip("`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/?").lower() in dict:
			v += 1
		if (float(v)/len(filter_p)>=THRESHOLD):
			return True
	return False

def _checkPDF(f:str)-> None:
	"""Attempts to read pdf. If an error occurs the check failed."""
	PdfFileReader(f(f,'rb'))

def decrypt(text:bytes, k:list[bytes]):
	iv = text[:16]
	# ensurses the partitioned cipher is a factor of block size
	index = floor(len(text[16:])*3/4)
	if index > 480: index = 480

	# simplified dictionary to be used for parsing
	dictionary = simp_dict(k)
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
		if (file_type == 'PDF'):
			filename = f"{k.index(i)}.{file_type.lower()}"
			with open(filename,'wb') as file:
				file.write(plain.strip(bytes(PAD_WITH,'utf-8')))
			try:
				_checkPDF(filename)
				fkey = i.decode()
				break
			except:
				remove(filename)
				continue
		else:	
			temp = plain.decode('utf-8','ignore')[16:index]
			if _checkValid(temp,dictionary):
				fkey = i.decode()
				break


	# decode plaintext and ignore non decipherable characters
	plain = plain.decode('utf-8','ignore')
	
	# remove padding
	if plain[-1] == PAD_WITH:
		plain=plain.strip(PAD_WITH)

	return plain,fkey
			
def encrypt(plaintext, key):
	# hash the key (SHA-256) to ensure that it is 32 bytes long
	key = sha256(key).digest()
	# generate a random 16-byte IV
	iv = Random.new().read(BLOCK_SIZE)

	# encrypt the ciphertext with the key using CBC block cipher mode
	cipher = AES.new(key, AES.MODE_CBC, iv)
	# if necessary, pad the plaintext so that it is a multiple of BLOCK SIZE in length
	plaintext += (BLOCK_SIZE - len(plaintext) % BLOCK_SIZE) * PAD_WITH
	# add the IV to the beginning of the ciphertext
	# IV is at [:16]; ciphertext is at [16:]
	ciphertext = iv + cipher.encrypt(plaintext)

	return ciphertext

if __name__ == "__main__":
	keys = get_keys()

	ciphertext = stdin.buffer.read().rstrip(b"\n")
	# print(chardet.detect(ciphertext[16:]))

	# #print(ciphertext.decode('cp1253'))
	# # iv = Random.new().read(BLOCK_SIZE)
	
	# # print(chardet.detect(iv))
	# #print(ciphertext.split(b'\x'))

	plaintext,key = decrypt(ciphertext, keys)

	print(f"KEY={key}\n{plaintext}")
