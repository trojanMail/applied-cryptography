#! python
"""
Name: Raven A. Alexander
Date: 2022-03-15
Description: This program brute forces the key of a vigenere ciphered text to produce the plaintext. Given a file containing ciphered
text as well as a file containing a dictionary of words titled "dictionary-03.txt", le-chiffre will decrypt the cipher and return the
plaintext that has the most matches to words in the dictionary or that have a validity that is above the threshold.
Version: Python 3.10.2 64-bit
"""
import re
from sys import exit,stdin
        
def _checkvalid(p: str, k:str, mx:tuple)->tuple:
    """Checks the validity of a given plaintext."""
    v = 0
    l = re.split(r'\n| ',p)
    while(l.count("")): 
        l.remove('')
    for word in l:
        if word.strip("`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/?").lower() in SIMP_DICT:
            v+=1
    if (float(v)/len(l) > mx[1]):
        return p,v/len(l),k
    return mx

def _subcipher(k: str, c: str)->str:
    """Substitutes the characters in a cipher text with the characters in a key."""
    i=0
    l=""
    for letter in c:
        if letter in ALPHABET:
            l+=k[i]
            i = (i+1) % len(k)
        else:
            l+=letter
    return l

def _subkeycipher(c: str)->str:
    """Returns the plaintext from a key substituted cipher."""
    l=""
    for i,letter in enumerate(c):
        if letter in ALPHABET:
            l+=_subchar(letter,i)
        else:
            l+=letter
    return l
            
def _subchar(c: str,i: int)->str:
    """Substitutes a character with another characters from a shifted alphabet."""
    index = ALPHABET.index(c)
    alpha = ALPHABET[index:] + ALPHABET[:index]
    try:
        new_index = alpha.index(CIPHER[i])
    except:
        return CIPHER[i]
    return ALPHABET[new_index]

def _notkey(w: str)->bool:
    """Returns False if a word is a valid key."""
    if len(w) == 1:
        return True
    for letter in w:
        if letter not in ALPHABET:
            return True
    return False

def simp_dict(dict: list):
    """Simplifies dictionary."""
    new_dict=[]
    for word in dict:
        new_dict.append(word.lower())
    return new_dict

def decrypt():
    """Decrypt a given vigenere cipher using a brute force technique with a dictionary."""
    valid = "",0,""
    length = len(CIPHER) 
    if length > 500: length = 500

    for word in DICTIONARY:

        if(_notkey(word)):
            continue

        key = _subcipher(word,CIPHER[:length])
        plain = _subkeycipher(key)
        valid = _checkvalid(plain,word,valid)

        if (valid[1] >= THRESH):
            key = _subcipher(valid[2],CIPHER[length:])
            plain = _subkeycipher(key)
            plain = valid[0]+plain
            return valid[2],plain

    return valid[2],valid[0]


if __name__ == "__main__":
    # GLOBALS 
    #ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "
    ALPHABET = " -,;:!?/.'\"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ"
    DICTIONARY = []
    CIPHER = ""
    THRESH = .75

    # read in dictionary as list
    try:
        with open ('dictionary-03.txt','r') as file:
            for line in file:
                DICTIONARY.append(line.strip('\n'))
    except:
        print("Invalid dictionary!\nEnsure the dictionary is titled dictionary-01.txt, and is in the same directory as the py program.")
        exit()

    SIMP_DICT = simp_dict(DICTIONARY)
   
    # read in file form stdin
    try:
        for line in stdin:
            CIPHER+=line
    except:
        print("File with ciphered text invalid.\nEnsure the cipher text is piped into the program as shown below:\npython et-tu-brute.py < cipher.txt")
        exit()
    
    # decrypt
    key,plaintext = decrypt()

    # display
    print("KEYWORD={}\n{}".format(key,plaintext),end="")




