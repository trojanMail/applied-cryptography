#! python
"""
Name: Raven A. Alexander
Date: 2022-03-24
Description: This program enciphers a given file with caesar or keyword cipher.
"""

from sys import argv,stdin,exit

"""PRIVATE FUNCTIONS"""
def _shift(c: str, k: int)->str:
    """Shifts a given character c by key k."""
    print(c)
    c =(func[2].index(c)+k)%len(func[2])
    return func[2][c]

def _subchark(c: str, a: str)-> str:
    """Substitutes a character in a cipher for a character in a alphabet."""    
    try:
        return a[func[2].index(c)]
    except:
        return c

def _get_newalphabet(k: str)-> str:
    """Returns alphabet with new key."""
    alpha = func[2]
    for i in k:
        alpha = alpha.replace(i,'')
    k += alpha
    return k

def _subplain(k: str, p: str)-> str:
    """Substitutes the characters in a plain text with the characters in a key."""
    i=0
    l=""
    for letter in p:
        if letter in func[2]:
            l+=k[i]
            i = (i+1) % len(k)
        else:
            l+=letter
    return l

def _subkeyplain(p: str)->str:
    """Returns the ciphertext from a key substituted plaintext."""
    l=""
    for i,letter in enumerate(p):
        if letter in func[2]:
            l+=_subcharv(letter,i)
        else:
            l+=letter
    return l

def _subcharv(c: str,i: int)-> str:
    """Substitutes a character with another characters from a shifted alphabet."""
    index = func[2].index(c)
    alpha = func[2][index:]+func[2][:index]
    try:
        return alpha[func[2].index(PLAIN[i])]
    except:
        return c
        
"""PUBLIC FUNCTIONS"""
def caesar()-> str:
    """Returns caesar cipher of a given text with a given key."""
    l = ""
    for char in PLAIN:
        if char == '\n':
            l+=char
            continue
        l+=_shift(char,func[1])
    return l

def keyword()-> str:
    """Returns keyword cipher of a given text with a given key."""
    l = ""
    new_alpha = _get_newalphabet(func[1])
    for char in PLAIN:
            if char == '\n':
                l+=char
                continue
            l+=_subchark(char,new_alpha)
    return l
    
def viginere() -> str:
    """Enciphers a given text with a viginere cipher."""
    key = _subplain(func[1],PLAIN)
    cipher = _subkeyplain(key)
    return cipher


if __name__ == "__main__":
    # choose correct cipher
    # func contains functions and parameters
    func = [] #cipher, key, alphabet
    A1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "
    A2 =" -,;:!?/.'\"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ"
    #A2 = "1234567890"
    PLAIN = ""

    # get cipher
    try:
        if argv[1] == "-c":
            func.append(caesar)
        elif argv[1] == "-k":
            func.append(keyword)
        elif argv[1] == "-v":
            func.append(viginere)
        elif argv[1] == "-h":
            print("./encipher.py --cipher --key --alphabet")
    except:
        print("./encipher.py --cipher --key --alphabet/nAvailable ciphers are caesar:/n/tkeyword/ncaeser/nviginere")
        exit()

    # get key
    try:
        func.append(argv[2])
    except:
        print("Please provide a key as the second argument.")
        exit()

    if func[0] == caesar:
        func[1] = int(func[1])

    # get alphabet
    try:
        func.append(argv[3])
    except:
        print("Please choose an alphabet:\nA1:{}\nA2:{}".format(A1,A2))
        exit()

    if func[2] == "A1":
        func[2] = A1
    elif func[2] == "A2":
        func[2] = A2

    #print(func[2])
    # read in file form stdin
    try:
        for line in stdin:
            PLAIN+=line
    except:
        print("File with ciphered text invalid.\nEnsure the cipher text is piped into the program as shown below:\npython et-tu-brute.py < cipher.txt")
        exit()

    # excute code
    CIPHER = func[0]()
    
    with open("cipher.txt","w") as test:
        test.write(CIPHER)
