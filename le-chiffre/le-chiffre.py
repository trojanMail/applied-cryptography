#! python
"""
Name: Raven A. Alexander
Date: 2022-03-15
Description: This program brute forces the key of a vigenere ciphered text to produce the plaintext. Given a file containing ciphered
text as well as a file containing a dictionary of words titled "dictionary-03.txt", le-chiffre will decrypt the cipher and return the
plaintext that has the most matches to words in the dictionary.
Version: Python 3.10.2 64-bit
"""
import re
from sys import exit,stdin


def _check_valid(mx: tuple, p:str, k:int)-> tuple:
    """Return the plaintext string with the most matching words in the dictionary."""
    v = 0
    l = re.split(r'\n| ',p)
    for word in l:
        if word.strip("`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/?").lower() in DICTIONARY:
            v+=1
        if (v/len(l)) >= THRESH:
            mx = p,-1,k
            return mx
    if (v > mx[1]):
        mx = p,v,k
    return mx

def decrypt():
    """Decrypt a given vigenere cipher using a brute force technique with a dictionary."""

if __name__ == "__main__":
    # GLOBALS 
    ALPHABET = " -,;:!?/.'\"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ"
    DICTIONARY = []
    CIPHER = ""
    THRESH = .75

    # read in dictionary as list
    try:
        with open ('dictionary-03.txt','r') as file:
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

    # display
    print("SHIFT={}:\n{}".format(V[2],V[0]),end="")





