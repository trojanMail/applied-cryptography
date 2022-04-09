#! python
"""
Name: Raven A. Alexander
Date: 2022-04-13
Description:
"""

from sys import stdin,exit
from math import lcm, gcd

def parsestdin(c: str)->tuple:
    """Parses input to return a seperated cipher and n value."""
    c = c.split('\n')
    cipher = []
    n = int(c[0])
    for i in c[1].split(','): cipher.append(int(i))
    return n,cipher

def _factor(a: int)->tuple:
    """Factors a number n as the product of two primes."""
    for i in range(3,int(a**1/2)+1,2):
        if not (a%i):
            return i, a//i
    return _exception(1)

def _getz(a: int,b:int)->int:
    """Returns the lcm of p-1 and q-1."""
    z = lcm(a-1,b-1)
    return z

def _isprime(a:int) -> bool:
    """Returns True if a number a is prime."""
    for i in range(2,a):
        if not (a%i):
            return False
    return True
def _valide(a:int,b:int)->bool:
    """Determines if an exponent a is valid."""
    return _isprime(a) and (gcd(a,b)==1)

def _getes(a: int)->list:
    """Return all valid e values for a given z."""
    es = []
    for i in range(3,a-1,2):
        if (_valide(i,a)):
            es.append(i)
    return es

def _getmodinverse(a: int,b: int)->int:
    """Return the modular inverse of a and b. -> naive approach required by course (see Fermat's Little Theorem)"""
    for i in range(1,b-1):
        if (a*i) % b == 1:
            return i
        
def _getascii(a: int,b: tuple)->str:
    """Returns the decrypted ascii character using a private key."""
    return chr(a**b[0] % b[1])
    
def _exception(a: int)->None:
    if a == 1:
        print("Error: No factor found.")
        exit()
    elif a == 0:
        print("Error: Invalid plaintext.")
    

def decrypt(n: int,cipher: list):
    p,q = _factor(n)
    print("p={}, q={}".format(p,q))
    print("n={}".format(n))
    z = _getz(p,q)
    print("z={}\n--".format(z))
    
    es = _getes(z)

    for e in es:
        print("Trying e={}".format(e))
        d = _getmodinverse(e,z)
        print("d={}".format(d))
        k_priv = (d,n)
        print("Public Key: {}\nPrivate Key: {}\n--".format((65537,n),k_priv))
        plain = ""

        for c in cipher:
            try:
                p = _getascii(c,k_priv)
                if not p.isascii():
                    plain = ""
                    _exception(0)
                    break
                plain+=p
            except KeyboardInterrupt:
                exit()
        if plain != "":
            return plain
    return plain

if __name__ == "__main__":
    CIPHER = ""
    # read in file form stdin
    try:
        for line in stdin:
            CIPHER+=line
    except:
        print("File with ciphered text invalid.\nEnsure the cipher text is piped into the program as shown below:\npython decipherer.py < cipher")
        exit()

    N,pcipher = parsestdin(CIPHER)
    V = decrypt(N,pcipher)

    # display
    print(V)
