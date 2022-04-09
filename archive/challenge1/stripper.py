#! python
"""This program strips the dictionary words from a given file."""
from sys import stdin
import re

def stripper()->str:
    """Strips the dicitonary words from a given plaintext."""
    l = re.split(r'\n| ',PLAIN)
    for word in l:
        if word.strip("`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/?").lower() in DICTIONARY:
            l.remove(word)
    return ' '.join(l)
            
if __name__ == "__main__":
    PLAIN = ""
    DICTIONARY = []
    # read in dictionary as list
    try:
        with open ('dictionary-01.txt','r') as file:
            for line in file:
                DICTIONARY.append(line.strip("\n`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/?").lower())
    except:
        print("Invalid dictionary!\nEnsure the dictionary is titled dictionary-01.txt, and is in the same directory as the py program.")
        exit()

    try:
        for line in stdin:
            PLAIN+=line
    except:
        print("File with ciphered text invalid.\nEnsure the cipher text is piped into the program as shown below:\npython et-tu-brute.py < cipher.txt")
        exit()

    stripped = stripper()
    print(stripped)
    