#! python
"""
Name: Raven A. Alexander
Date: 2022-04-27
Description: This program performs bitwise operations on RGB values obtained from an inputted image.
Python Version: 3.10.2 64-bit
"""
from random import randint
from PIL import Image
from sys import argv

# the images
INPUT_IMAGE = "input.png"
AND_IMAGE = "and.png"
OR_IMAGE = "or.png"
XOR_IMAGE = "xor.png"

def getKey()->tuple:
    """Gets and parses a key file to be used for bitwise operations."""
    key=[]
    with open('input.key','r',encoding='utf-8') as f:
        for line in f:
            temp = tuple(map(int,line.strip('\n').split(',')))
            key.append(temp)
    return key
                

def makeKey()->tuple:
    """Creates the next key to be used for bitwise operations."""
    return (randint(0,255),randint(0,255),randint(0,255))
def andOp(a:tuple,b:tuple)->tuple:
    """Performs and operations on two tuples of RGB values."""
    return (a[0] & b[0], a[1] & b[1], a[2] & b[2])
def orOp(a:tuple,b:tuple)->tuple:
    """Performs or operations on two tuples of RGB values."""
    return (a[0] | b[0], a[1] | b[1], a[2] | b[2])
def xorOp(a:tuple,b:tuple)->tuple:
    """Performs xor operations on two tuples of RGB values."""
    return (a[0] ^ b[0], a[1] ^ b[1], a[2] ^ b[2])


def encipher()->None:
    input_key = ""
    
    # get the input image
    img = Image.open(INPUT_IMAGE)
    and_img = img.copy()
    or_img = img.copy()
    xor_img = img.copy()

    # load pixeles
    and_pixels = and_img.load()
    or_pixels = or_img.load()
    xor_pixels = xor_img.load()

    rows, cols = img.size

    # operate on pixels
    i = 0
    while i < rows:
        j = 0
        while j < cols:
            key = makeKey()
            and_pixels[i,j] = andOp(and_pixels[i,j],key)
            or_pixels[i,j] = orOp(or_pixels[i,j],key)
            xor_pixels[i,j] = xorOp(xor_pixels[i,j],key)
            input_key+=(f"{key[0]},{key[1]},{key[2]}\n")
            j+=1
        i+=1

    # write the new image
    and_img.save(AND_IMAGE)
    or_img.save(OR_IMAGE)
    xor_img.save(XOR_IMAGE)

    with open('input.key','w') as f:
        f.write(input_key)

def decipher(k:list[tuple])->None:
    # open images
    # and_img = Image.open(AND_IMAGE)
    # or_img = Image.open(OR_IMAGE)
    xor_img = Image.open(XOR_IMAGE)
    
    # load images
    # and_pixels = and_img.load()
    # or_pixels = or_img.load()
    xor_pixels = xor_img.load()

    # assume all images are the same size
    rows,cols = xor_img.size

    # operate on pixels
    l = 0
    i = 0
    while i < rows:
        j = 0
        while j < cols:
            # and and or operations are destructive
            # and_pixels[i,j] = andOp(and_pixels[i,j],k[l])
            # or_pixels[i,j] = orOp(or_pixels[i,j],k[l])
            xor_pixels[i,j] = xorOp(xor_pixels[i,j],k[l])
            j+=1
            l +=1
        i += 1

    # and_img.save(AND_IMAGE)
    # or_img.save(OR_IMAGE)
    xor_img.save(XOR_IMAGE)

if __name__ == "__main__":
    if argv[1] == '-e':
        encipher()
    elif argv[1] == '-d':
        key = getKey()
        decipher(key)