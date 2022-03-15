#! python
# big O of around n^3; not ideal but it gets the job done
"""
Name: Raven A. Alexander
Date: 2022-03-15
Description: This program brute forces the key of a caeser ciphered text to produce the plaintext. Given a file containing ciphered
text as well as a file containing a dictionary of words titled "dictionary-01.txt", et-tu-brute will decrypt the cipher and return the
plaintext that has the most words in the dictionary.
Version: Python 3.10.2 64-bit
"""
import fileinput
import re
from sys import exit,stdin


def _shift(x: str,y: int)-> str:
    """Shifts a given char."""
    x =(ALPHABET.index(x)-y)%len(ALPHABET)
    return ALPHABET[x]

def _check_valid(mx: tuple, p:str, k:int)-> tuple:
    """Return the plaintext string with the most matching words in the dictionary."""
    v = 0
    l = re.split(r'\n| ',p)
    for word in l:
        if word.strip("`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/?") in DICTIONARY:
            v+=1
    if (v > mx[1]):
        mx = p,v,k
    return mx

def decrypt():
    """Decrypt a given caeser cipher using a brute force technique with a dictionary."""
    key = 1
    l=""
    p =""
    valid = "",0,1
    while(key<len(ALPHABET)):
        for char in CIPHER:
            if char == '\n':
                l+=char
                continue
            l+=_shift(char,key)
        valid = _check_valid(valid,l,key)
        l=""
        key+=1
    return valid

if __name__ == "__main__":
    ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "
    #ALPHABET = " -,;:!?/.'\"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ"
    DICTIONARY = []
    CIPHER = ""
    # read in dictionary as list
    try:
        with open ('dictionary-01.txt','r') as file:
            for line in file:
                DICTIONARY.append(line.strip('\n').lower())
    except:
        print("Invalid dictionary!\nEnsure the dictionary is titled dictionary-01.txt, and is in the same directory as the py program.")
        exit()
   
    # read in file form stdin
    try:
        for line in stdin:
            CIPHER+=line
    except:
        print("File with ciphered text invalid.\nEnsure the cipher text is piped into the program as shown below:\npython et-tu-brute.py < cipher.txt")
        exit()
    
    # decrypt
    V = decrypt()
    print("SHIFT={}:\n{}".format(V[2],V[0]),end="")





