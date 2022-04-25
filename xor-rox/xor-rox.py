#! python
"""
Name: Raven A. Alexander
Date: 2022-04-27
Description: This program performs bitwise operations on RGB values obtained from an image.
Python Version: 3.10.2 64-bit
"""
from random import randint
from PIL import Image

# the images
INPUT_IMAGE = "input.png"
AND_IMAGE = "and.png"
OR_IMAGE = "or.png"
XOR_IMAGE = "xor.png"
INPUT_KEY = ""

def getKey()->tuple:
    """Gets the next key to be used for bitwise operations."""
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


if __name__ == "__main__":

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
            key = getKey()
            and_pixels[i,j] = andOp(and_pixels[i,j],key)
            or_pixels[i,j] = orOp(or_pixels[i,j],key)
            xor_pixels[i,j] = xorOp(xor_pixels[i,j],key)
            print(f"{key[0]},{key[1]},{key[2]}")
            j+=1
        i+=1

    # write the new image
    and_img.save(AND_IMAGE)
    or_img.save(OR_IMAGE)
    xor_img.save(XOR_IMAGE)


