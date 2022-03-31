#! python
"""
Name: Raven A. Alexander
Date: 2022-03-15
Description: This program deciphers a given file using a specific cipher.
"""
import re
from sys import exit,stdin
from sys import argv
from math import floor

def _shift(x: str,y: int)-> str:
    """Shifts a given char."""
    try:
        x =(ALPHABET.index(x)-y)%len(ALPHABET)
    except:
        return x
    return ALPHABET[x]

def _subchark(x: str, p: str)-> str:
    """Substitutes a character in a cipher for a character in a alphabet."""    
    try:
        return ALPHABET[p.index(x)]
    except:
        return x

def _subcharv(c: str,i: int)->str:
    """Substitutes a character with another characters from a shifted alphabet."""
    index = ALPHABET.index(c)
    alpha = ALPHABET[index:] + ALPHABET[:index]
    try:
        new_index = alpha.index(CIPHER[i])
    except:
        return CIPHER[i]
    return ALPHABET[new_index]

def _checkvalid(mx: tuple, p:str, k)-> tuple:
    """Return the plaintext string with the most matching words in the dictionary."""
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
  
def _send_file(p: str, k: int):
    with open(str(k),"w") as test:
                test.write(p)

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
            l+=_subcharv(letter,i)
        else:
            l+=letter
    return l

def _notkey(w: str)->bool:
    """Returns False if a word is a valid key."""
    if len(w) == 1:
        return True
    for letter in w:
        if letter not in ALPHABET:
            return True
    return False

def _get_newalphabet(k: str)-> str:
    """Returns alphabet with new key."""
    alpha = ALPHABET
    for i in k:
        alpha = alpha.replace(i,'')
    k += alpha
    return k

def keyword(d: list):
    """Decrypt a given cipher using a brute force technique with a dictionary."""
    l=""
    valid = "",0,""
    length=len(CIPHER)
    if length > 500: length = 500

    for key in d:
        a = _get_newalphabet(key)

        for char in CIPHER[:length]:
            if char == '\n':
                l+=char
                continue
            l+=_subchark(char,a)
        valid = _checkvalid(valid,l,key)
        if valid[1] >= THRESH:
            l = valid[0]
            for char in CIPHER[length:]:
                if char == '\n':
                    l+=char
                    continue
                l+=_subchark(char,a)
            return valid[2],l
        l=""
    return valid[2],l

def caesar():
    """Decrypt a given caeser cipher using a brute force technique with a dictionary."""
    key = 1
    l=""
    valid = "",0,1
    length = len(CIPHER)
    if length > 500: length = 500

    while(key<len(ALPHABET)):
        for char in CIPHER[:length]:
            if char == '\n':
                l+=char
                continue
            l+=_shift(char,key)
        valid = _checkvalid(valid,l,key)

        if valid[1] >= THRESH:
            l = valid[0]
            for char in CIPHER[length:]:
                if char == '\n':
                    l+=char
                    continue
                l+=_shift(char,key)
            return valid[2],l
        #_send_file(l,key)
        l=""
        key+=1
    return valid[2],l

def viginere():
    """Decrypt a given vigenere cipher using a brute force technique with a dictionary."""
    valid = "",0,""
    length = len(CIPHER) 
    if length > 500: length = 500

    for word in DICT:

        if(_notkey(word)):
            continue

        key = _subcipher(word,CIPHER[:length])
        plain = _subkeycipher(key)
        valid = _checkvalid(valid,plain,word)

        if (valid[1] >= THRESH):
            key = _subcipher(valid[2],CIPHER)
            plain = _subkeycipher(key)
            return valid[2],plain

    return valid[2],valid[0]

def filter_dict(d: list):
    """Filters dictionary by removing non-valid keywords."""
    nd = []
    k = True
    for i in d:
        if len(i) == 1:
            continue
        else:
            word = sorted(i.lower())
            for j in word:
                if word.count(j) > 1:
                    k = False
                    break
        if k:
            nd.append(i)
        k = True
    return nd

def simple_dict(dict: list):
    """Simplifies words in global dictionary."""
    new_dict = []
    for i,j in enumerate(dict):
        new_dict.append(j.strip("`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/?").lower())
    return new_dict

if __name__ == "__main__":
    # GLOBALS 
    #ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "
    ALPHABET = " -,;:!?/.'\"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ"
    
    # challenge1 alphabets
    #ALPHABET = "7JZv. 964jMLh)5QtAS2PXWaFU8,/cpkY'O(Tqr?dsEmbRwINVKBez1=3+H0GyfxCiD\"lg:!uo"
    #ALPHABET = "GHXJ+g5y6Asd3ZB4D12NT8mQEcarbSIo7zwjltOWu9eP/pFVL0KYqx=hRUCkviMf"
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


    # read in file form stdin
    try:
        for line in stdin:
            CIPHER+=line
    except:
        print("File with ciphered text invalid.\nEnsure the cipher text is piped into the program as shown below:\npython et-tu-brute.py < cipher.txt")
        exit()
    
    # decrypt
    k_dict = filter_dict(DICT)
    SIMP_DICT = simple_dict(DICT)

    # choose correct cipher
    if argv[1] == "-c":
        V = caesar()
    if argv[1] == "-k":
        V = keyword(k_dict)
    if argv[1] == "-v":
        V = viginere()

    if argv[1] == "-h":
        print("./decipher -c/k/v -o/p < cipher.txt")
        exit()

    # display
    if argv[2] == "-o":
        with open("plain2.txt","w") as test:
            test.write(V[0])
    elif argv[2] == "-p":
        print("KEY:{}\n{}".format(V[0],V[1]),end="")






