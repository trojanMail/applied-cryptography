"""
Name: Raven A. Alexander
Date: 2022-04-13
Description:
"""
#! python
from sys import stdin,exit

def parsestdin(c: str)->tuple:
    """Parses input to return a seperated cipher and n value."""
    c = c.split('\n')
    cipher = []
    n = int(c[0])
    for i in c[1].split(','): cipher.append(int(i))
    return n,cipher

def _factor(a: int)->tuple:
    """Factors a number n as the product of two primes."""
    return b,d

def _getz(a: int,b:int)->int:
    """Returns the lcm of p-1 and q-1."""
    return z

def _getes(i: int)->list:
    """Return all valid e values for a given z."""
    return es

def _getmodinverse(a: int,b: int)->int:
    """Return the modular inverse of numbers and b."""
    return d

def _getascii(c: int,k_priv: int):
    """Returns """

def _exception()->None:
    print("Error: invalid plaintext.")

def decrypt(n: int,cipher: list):
    p,q = _factor(n)
    z = _getz(p,q)
    es = _getes(z)

    for e in es:
        print("Trying e={}".format(e))
        print("d={}".format(d))

        d = _getmodinverse(e)
        k_priv = "" #d,n?
        plain = ""

        for c in cipher:
            try:
                p = _getascii(c,k_priv)
                plain+=p
            except:
                _exception()
                continue
    return plain
if __name__ == "__main__":
    CIPHER = ""
    # read in file form stdin
    try:
        for line in stdin:
            CIPHER+=line
    except:
        print("File with ciphered text invalid.\nEnsure the cipher text is piped into the program as shown below:\npython et-tu-brute.py < cipher.txt")
        exit()

    N,pcipher = parsestdin(CIPHER)
    V = decrypt

    # display
    print(V)
