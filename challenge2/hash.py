#! python
from sys import stdin,exit
from hashlib import sha256
"""
This program takes in a text file with one hash per line and determines the corresponding plaintext word from a dictionary.
hash identfier: https://www.tunnelsup.com/hash-analyzer/
"""
def getPlainText(hash:list[str],dict:list[str]) -> list[str]:
    """Attempts to return the plaintext representation from a hash."""
    p = []
    n = True
    for i in hash:
        for j in dict:
            h = sha256(j.encode()).hexdigest()
            if h == i:
                n = False
                p.append(j)
                break
        if n:
            p.append("None")
        n = True
    return p

def display(p: list,h: list)->None:
    for i,j in enumerate(p):
        print("{}: {} -> {}".format(i,h[i],j))

if __name__== "__main__":
    hashes = []
    dictionary = []
    plaintexts = []

    try:
        for line in stdin:
            hashes.append(line)
    except:
        print("Reading in hashes failed.")
        exit()

    try:
        with open ('dictionary-04.txt','r') as file:
            for line in file:
                dictionary.append(line.strip('\n'))
    except:
        print("Invalid dictionary!\nEnsure the dictionary is titled dictionary-04.txt, and is in the same directory as the program.")
        exit()

    plaintexts = getPlainText(hashes,dictionary)
    display(plaintexts,hashes)