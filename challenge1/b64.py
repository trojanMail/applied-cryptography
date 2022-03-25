#! python
"""This program decodes and encodes a given file."""
from base64 import b64decode as b64d
from base64 import b64encode as b64e
from array import array
from sys import stdin, argv

if __name__ == "__main__":
    B64 = ""
    try:
        for line in stdin:
            B64+=line
    except:
        print("File with text invalid.\nEnsure the cipher text is piped into the program as shown below:\npython et-tu-brute.py < cipher.txt")
        exit()

    if len(argv) < 3:
          print("Please enter an option (-d/-e).")  
          
    # if argv[1] == "-d":
    #     results = bytearray(B64.encode('ascii')).decode()
    #     # results = results.decode('utf-8')
    

    # if argv[1] == "-e":
    #     results = bytearray(B64.encode('ascii'))
    #     results = b64e(results)

    
    if argv[2] == "-o":
        with open("results.txt","w") as test:
            test.write(str(results))
    elif argv[2] == "-p": 
            print(results)