#! python
# big O of around n^3; not ideal but it gets the job done
"""
Name: Raven A. Alexander
Date: 2022-03-15
Description: This program brute forces the key of a caeser ciphered text to produce the plaintext. Given a file containing ciphered
text as well as a file containing a dictionary of words titled "dictionary-01.txt", et-tu-brute will decrypt the cipher and return the
plaintext that best corresponds with the words in the dictionary file.
"""
import fileinput
import re


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
            print(word)
            v+=1
    if (v > mx[1]):
        mx = p,v,k
    return mx

def decrypt():
    """Decrypt a given caeser cipher using a brute force technique with a dictionary."""
    key = 1
    nl=""
    p =""
    valid = "",0,1
    while(key<len(ALPHABET)):
        for line in CIPHER:
            for char in line:
                if char == '\n':
                    nl+=char
                    continue
                nl+=_shift(char,key)
            p+=nl
            nl=""
        valid = _check_valid(valid,p,key)
        p=""
        key+=1
    return valid

if __name__ == "__main__":
    DICTIONARY = []
    # read in dictionary as list
    with open ('dictionary-01.txt','r') as file:
        for line in file:
            DICTIONARY.append(line.strip('\n').lower())

    ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "

    # read in file form stdin
    CIPHER = []
    for line in fileinput.input():
        CIPHER.append(line)

    print(decrypt())




