#! python
"""
Name: Raven A. Alexander
Date: 2022-05-02
Description: This program implements the Rijndael algorithm to brute force a given ciphertext.
"""
import re
from sys import stdin
from hashlib import sha256
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode
from math import floor
from io import TextIOWrapper as TW

# the AES block size to use
BLOCK_SIZE = 16
# the padding character to use to make the plaintext a multiple of BLOCK_SIZE in length
PAD_WITH = "#"
THRESHOLD = .75
def simp_dict(dict:list):
	"""Simplifies dictionary."""
	new_dict=[]
	for word in dict:
		new_dict.append(word.lower())
	return new_dict

def get_keys()->list[str]:
	k = []
	with open('dictionary1-3.txt','r',encoding='utf-8') as f:
		k = f.read().split('\n')
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
# decrypts a ciphertext with a key
def decrypt(ciphertext:bytes, k:list):
	iv = ciphertext[:16]
	# ensurses the partitioned cipher is a factor of block size
	index = floor((len(ciphertext[16:])/BLOCK_SIZE)*3/4)*BLOCK_SIZE
	if index > 480: index = 480
	part_cipher = ciphertext[16:index]
	# simplified dictionary to be used for parsing
	dictionary = simp_dict(k)
	plaintext = ""
	fkey=""
	for i in k:
		# hash the key (SHA-256) to ensure that it is 32 bytes long
		key = sha256(i.encode('utf-8')).digest()
		
		# decrypt the ciphertext with the key using CBC block cipher mode
		cipher = AES.new(key, AES.MODE_CBC,iv)

		# the ciphertext is after the IV (so, skip 16 bytes)
		plaintext = cipher.decrypt(part_cipher)
		if _checkValid(plaintext.decode('utf-8','ignore'),dictionary):
			plaintext = cipher.decrypt(ciphertext[16:])
			fkey = i
			break

	# decode plaintext and ignore non decipherable characters
	plaintext = plaintext.decode('utf-8','ignore')
	
	# remove padding
	if plaintext[-1] == PAD_WITH:
		plaintext=plaintext.strip(PAD_WITH)

	return plaintext,fkey
			

# encrypts a plaintext with a key
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

	ciphertext = stdin.buffer.read().strip()

	plaintext,key = decrypt(ciphertext, keys)

	print(f"KEY={key}\n{plaintext}")
