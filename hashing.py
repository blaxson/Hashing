from Crypto.Hash import SHA256
import os
import sys
import time

def main(): 
    for i in range(8, 51, 2):
        find_collisions(i)
    #hash_two("different5", "testing27")

def hash_two(str1, str2):
    hexDigest1 = hash_SHA256(str1)
    hexDigest2 = hash_SHA256(str2)
    print(bytes(hexDigest1))
    print()
    print(bytes(hexDigest2))

def hash_SHA256(input_str):
    h = SHA256.new()
    input_b = str.encode(input_str)
    h.update(input_b)
    digest = h.digest()
    digest_array = bytearray(digest)
    return digest_array

def find_collisions(num_bits):
    str1 = 'different%d'
    str2 = 'testing%d'
    seen = {}
    n = 0
    init_time = time.time()
    while True:
        h1 = hash_SHA256(str1 % n)
        h2 = hash_SHA256(str2 % n)

        h1 = and_digest(h1, num_bits) # get only first num_bits
        h2 = and_digest(h2, num_bits) # get only first num_bits
        
        seen[bytes(h1)] = n
        
        if bytes(h2) in seen:
            print("digest size: {} bits".format(num_bits))
            print("number of inputs: {}".format(2*n))
            print("took {} seconds".format(time.time() - init_time))
            return 
        n+=1
        

""" takes in a bytearray digest and the first num_bits we want from
    the digest, and returns that as a bytearray """
def and_digest(digest, num_bits):
    num_bytes = num_bits // 8
    remainder = num_bits % 8
    if remainder != 0:
        output = bytearray(num_bytes + 1)
    else:
        output = bytearray(num_bytes)
    if remainder == 1:
        remainder = 128
    elif remainder == 2:
        remainder = 192
    elif remainder == 3:
        remainder = 224
    elif remainder == 4:
        remainder = 240
    elif remainder == 5:
        remainder = 248
    elif remainder == 6:
        remainder = 252
    elif remainder == 7:
        remainder = 254
    for i in range(0, num_bytes):
        output[i] = digest[i] & 255 # and with ff
    if remainder != 0:
        output[num_bytes] = digest[num_bytes] & remainder
    return output
"""
10 //  = 2
10 % 4 = 2
8 = 1000
12 = 1100
14 = 1110 '\x0e'


1000 0000 b'\80'
1100 0000 b'\c0'
1110 0000 b'\e0'
1111 0000 b'\f0'
1111 1000 b'\f8'
1111 1100 b'\fc'
1111 1110 b'\fe' b[i] & 254

0001 0010
0011 0100

0001 0000
"""





if __name__ == "__main__":
    main()