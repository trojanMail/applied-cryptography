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

def _sub(x: str, p: str)-> str:
    """Substitutes a character in a cipher for a character in a alphabet."""    
    try:
        return ALPHABET[p.index(x)]
    except:
        return x

def _check_valid(mx: tuple, p:str, k)-> tuple:
    """Return the plaintext string with the most matching words in the dictionary."""
    v = 0
    l = re.split(r'\n| ',p)
    r = floor(len(l)/6)
    if r > 50: r = 10
    for word in l[:r]:
        if word.strip("`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/?").lower() in DICT:
            v+=1
        if (v/r) >= THRESH:
            mx = p,-1,k
            return mx
    if (v > mx[1]):
        mx = p,v,k
    return mx
  
def _send_file(p: str, k: int):
    with open(str(k),"w") as test:
                test.write(p)

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

def caesar():
    """Decrypt a given caeser cipher using a brute force technique with a dictionary."""
    key = 1
    l=""
    valid = "",0,1
    while(key<len(ALPHABET)):
        if valid[1] == -1:
            return valid
        for char in CIPHER:
            if char == '\n':
                l+=char
                continue
            l+=_shift(char,key)
        valid = _check_valid(valid,l,key)
        #_send_file(l,key)
        l=""
        key+=1
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
            for j in word:
                if word.count(j) > 1:
                    k = False
                    break
        if k:
            nd.append(i)
        k = True
    return nd

def simple_DICT():
    """Simplifies words in global dictionary."""
    for i,j in enumerate(DICT):
        DICT[i] = j.strip("`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/?").lower()

def simp_dict(dict: list):
    """Simplifies dictionary."""
    new_dict=[]
    for word in dict:
        new_dict.append(word.lower())
    return new_dict

if __name__ == "__main__":
    # GLOBALS 
    #ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "
    #ALPHABET = " -,;:!?/.'\"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ"
    ALPHABET = "7JZv. 964jMLh)5QtAS2PXWaFU8,/cpkY'O(Tqr?dsEmbRwINVKBez1=3+H0GyfxCiD\"lg:!uo"
    #ALPHABET = "GHXJ+g5y6Asd3ZB4D12NT8mQEcarbSIo7zwjltOWu9eP/pFVL0KYqx=hRUCkviMf"
    CIPHER = ""
    THRESH = .35
    DICT = []
    # read in dictionary as list
    try:
        with open ('dictionary-unique-letters.txt','r') as file:
            for line in file:
                DICT.append(line.strip('\n'))
    except:
        print("Invalid dictionary!\nEnsure the dictionary is titled dictionary-01.txt, and is in the same directory as the py program.")
        exit()
   
    # get filtered dictionary
    

    # read in file form stdin
    try:
        for line in stdin:
            CIPHER+=line
    except:
        print("File with ciphered text invalid.\nEnsure the cipher text is piped into the program as shown below:\npython et-tu-brute.py < cipher.txt")
        exit()
    
    # decrypt
    simple_DICT()

    # choose correct cipher
    if argv[1] == "-c":
        V = caesar()
    if argv[1] == "-k":
        k_dict = filter_dict(DICT)
        V = keyword(k_dict)
    # if argv[1] == "-v":
    #     v_dict = simp_dict()
    #     V = viginere(v_dict)
    if argv[1] == "-h":
        print("./decipher -c/k/v -o/p < cipher.txt")
        exit()

    # display
    if V[1] == -2:
        print("No valid plaintext found from words in dictionary! Ensure you have uncommented the correct alphabet.")
    else:
        if argv[2] == "-o":
            with open("plain2.txt","w") as test:
                test.write(V[0])
        elif argv[2] == "-p":
            print("KEY:{}\n{}".format(V[2],V[0]),end="")






