#! python
"""
Name: Raven A. Alexander
Date: 2022-03-24
Description: This program enciphers a given file with caesar or keyword cipher.
"""

from sys import argv,stdin

def caesar()-> str:
    """Returns caesar cipher of a given text with a given key."""
    l = ""
    for char in PLAIN:
        if char == '\n':
            l+=char
            continue
        l+=_shift(char,func[1])
    return l

def _shift(c: str, k: int)->str:
    """Shifts a given character c by key k."""
    print(c)
    c =(func[2].index(c)+k)%len(func[2])
    return func[2][c]

def keyword()-> str:
    """Returns keyword cipher of a givent text with a given key."""
    l = ""
    new_alpha = _get_newalphabet(func[1])
    for char in PLAIN:
            if char == '\n':
                l+=char
                continue
            l+=_sub(char,new_alpha)
    return l

def _sub(c: str, a: str)-> str:
    """Substitutes a character in a cipher for a character in a alphabet."""    
    return a[func[2].index(c)]

def _get_newalphabet(k: str)-> str:
    """Returns alphabet with new key."""
    alpha = func[2]
    for i in k:
        alpha = alpha.replace(i,'')
    k += alpha
    return k

if __name__ == "__main__":
    # choose correct cipher
    # func contains functions and parameters
    func = []
    A1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "
    #A2 =" -,;:!?/.'\"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ"
    A2 = "1234567890"
    PLAIN = ""

    # get cipher
    if argv[1] == "caesar":
        func.append(caesar)
    elif argv[1] == "keyword":
        func.append(keyword)
    else:
        print("Please provide a cipher (caesar or keyword) as the first argument and key as the second argument.")

    # get key
    try:
        func.append(argv[2])
    except:
        print("Please provide a key as the second argument.")

    if func[0] == caesar:
        func[1] = int(func[1])

    # get alphabet
    try:
        func.append(argv[3])
    except:
        print("Please choose an alphabet:\nA1:{}\nA2:{}".format(A1,A2))
    
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
