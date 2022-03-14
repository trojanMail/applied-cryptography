#! python
# big O of around n^3; not ideal but it gets the job done
"""
Name: Raven A. Alexander
Date: 2022-03-14
Description: This program brute forces the key of a caeser ciphered text to produce the plaintext.
"""
import fileinput

DICTIONARY = []
# read in dictionary as list
with open ('dictionary-01.txt','r') as file:
    for line in file:
        DICTIONARY.append(line.strip('\n'))

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "
#ALPHABET = list(ALPHABET)
# read in file form stdin
cipher = []
key = 1
for line in fileinput.input():
    cipher.append(line.split(" "))

plaintext = ""
while(key < len(ALPHABET)):
    for line in cipher:
        temp = ""
        for word in line:
            for char in word:
                if char is '\n':
                    temp += (char)
                    continue
                shift = ((ALPHABET.index(char)-key)%len(ALPHABET))
                temp += ALPHABET[shift]
        
        plaintext += temp
    plaintext = ""
    key += 1
