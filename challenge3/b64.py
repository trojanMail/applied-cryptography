#! python
from base64 import b64decode as dec
from base64 import b64encode as enc
from sys import stdin, stdout, argv
def ben(t:str):
    """Encode string in base64."""
    return enc(t)
def bde(t:str):
    """Decode string from base64."""
    return dec(t)


if __name__ == "__main__":
    if (argv[1] == '-e'):
        text = stdin.buffer.read().strip(b'\n')
        stdout.buffer.write(ben(text))
    if (argv[1] == '-d'):
        text = stdin.buffer.read().strip(b'\n')
        stdout.buffer.write(bde(text))
    