#! python
"""
Name: Raven A. Alexander
Date: 2022-03-15
Description: This program brute forces the key of a keyword ciphered text to produce the plaintext. Given a file containing ciphered
text as well as a file containing a dictionary of words titled "dictionary-01.txt", abraxas will decrypt the cipher and return the
plaintext that has the most matches to words in the dictionary.
Version: Python 3.10.2 64-bit
"""
import re
from sys import exit,stdin
from math import floor
from time import time

def _sub(x: str, p: str)-> str:
    """Substitutes a character in a cipher for a character in a alphabet."""    
    try:
        return ALPHABET[p.index(x)]
    except:
        print("Substring not found! Ensure you have uncommented the correct alphabet.")
        exit()
    
def lower_DICT():
    """Simplifies words in global dictionary."""
    for i,j in enumerate(DICT):
        DICT[i] = j.strip("`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/?").lower()

def _check_valid(mx: tuple, p:str, k:str)-> tuple:
    """Return the plaintext string with the most matching words in the dictionary."""
    v = 0
    l = re.split(r'\n| ',p)
    r = floor(len(l)/6)
    if r > 50: r = 50
    for word in l[:r]:
        if word.strip("`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/?").lower() in DICT:
            v+=1
        if (v/r) >= THRESH:
            mx = p,-1,k
            return mx
    if (v > mx[1]):
        mx = p,v,k
    return mx

def decrypt(d: list):
    """Decrypt a given cipher using a brute force technique with a dictionary."""
    l=""
    valid = "",0,1
    for key in d:
        a = _get_newalphabet(key)
        if valid[1] == -1:
            return valid
        for char in CIPHER:
            if char == '\n':
                l+=char
                continue
            l+=_sub(char,a)
        valid = _check_valid(valid,l,key)
        l=""
    if (valid[1]/len(re.split(r'\n| ',valid[0])) < THRESH):
        valid = valid[0],-2,valid[1]
    return valid

def filter_dict(d: list):
    """Filters dictionary by removing non-valid keywords."""
    nd = []
    k = True
    for i in d:
        if len(i) == 1:
            continue
        else:
            word = sorted(i.lower())
            #print(word)
            for j in word:
                if word.count(j) > 1:
                    k = False
                    break
        if k:
            nd.append(i)
        k = True
    return nd
def _get_newalphabet(k: str)-> str:
    """Returns alphabet with new key."""
    alpha = ALPHABET
    for i in k:
        alpha = alpha.replace(i,'')
    k += alpha
    # print(k)
    return k

if __name__ == "__main__":
    # GLOBALS 
    #ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "
    ALPHABET = " -,;:!?/.'\"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ"
    CIPHER = ""
    THRESH = .75
    DICT = []
    # read in dictionary as list
    try:
        with open ('dictionary-01.txt','r') as file:
            for line in file:
                DICT.append(line.strip('\n'))
    except:
        print("Invalid dictionary!\nEnsure the dictionary is titled dictionary-01.txt, and is in the same directory as the py program.")
        exit()
   
    # get filtered dictionary
    new_dict = filter_dict(DICT)

    # read in file form stdin
    try:
        for line in stdin:
            CIPHER+=line
    except:
        print("File with ciphered text invalid.\nEnsure the cipher text is piped into the program as shown below:\npython et-tu-brute.py < cipher.txt")
        exit()
    
    # decrypt
    lower_DICT()
    start = time()
    V = decrypt(new_dict)
    end = time()

    # display
    if V[1] == -2:
        print("No valid plaintext found from words in dictionary! Ensure you have uncommented the correct alphabet.")
    else:
        print("KEY:{}\n{}".format(V[2],V[0]),end="")



