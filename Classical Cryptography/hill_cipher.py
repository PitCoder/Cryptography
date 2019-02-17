'''
================================== HILL CIPHER ==================================
Hill cipher was invented by Lester S. Hill in 1929, it is a digraph block cipher
that works on a set of letters. Unlike other ciphers of this kind, Hill cipher
is extendable to work with different sizes of block letters.

Hill cipher uses a mathematics subject called Linear Algebra, therefore requires
a basic knowledge of matrix operations an modular arithmetic.

The following code proposes an implementation of this algorithm.

Author: Eric Alejandro Lopez Ayala
Language: Python3
Date: February 13th 2019
'''

import numpy as np
from random import randint
from extended_euclidean_algorithm import *

#BLOCK SIZE DEFINITION
BLOCK_SIZE = 3
#ALPHABET SIZE DEFINITION
ALPHABET_SIZE = 256
#ALPHABET
ALPHABET = []

def minor(arr, i, j):
    return np.delete(np.delete(arr, i, axis=0), j, axis=1)

def minor_matrix(matrix, x, y):
    minorM = []
    for i in range(x):
        row = []
        for j in range(y):
            m_minor = minor(matrix, i, j)
            row.append(int(round(np.linalg.det(m_minor))))
        minorM.append(row)
    return np.array(minorM)

def cofactors_matrix(matrix, x, y):
    cofaM = []
    sign = 1
    for i in range(x):
        row = []
        for j in range(y):
            if (i+j) % 2 == 0:
                sign = 1
            else:
                sign = -1
            row.append(matrix[i][j] * sign)
        cofaM.append(row)
    return np.array(cofaM)

def adjoint_matrix(matrix):
    min_matrix = minor_matrix(matrix, BLOCK_SIZE, BLOCK_SIZE)
    print("Minors Matrix: ", min_matrix)

    cofa_matrix = cofactors_matrix(min_matrix, BLOCK_SIZE, BLOCK_SIZE)
    print("Cofactors Matrix: ", cofa_matrix)

    adj_matrix = cofa_matrix.transpose()
    print("Adjoint Matrix: ", adj_matrix)

    return adj_matrix

def keyGeneration():
    #VARIABLE DEFINITION
    key_matrix = []
    is_inverse = False

    while not is_inverse:
        #CANDIDATE MATRIX GENERATION
        key_matrix = []
        for i in range(BLOCK_SIZE):
            row = []
            for j in range(BLOCK_SIZE):
                row.append(randint(0, ALPHABET_SIZE))
            key_matrix.append(row)

        #CANDIDATE MATRIX VALIDATION
        determinant = int(round(np.linalg.det(key_matrix))) % ALPHABET_SIZE
        if determinant < 0:
            determinant = determinant + ALPHABET_SIZE

        gdc, s, t = eea(ALPHABET_SIZE, determinant)
        if  gdc == 1:
            is_inverse = True

    return np.array(key_matrix)

def modularInverseMatrix(key):
    #KEY MATRIX DETERMINANT GENERATION
    determinant = int(round(np.linalg.det(key))) % ALPHABET_SIZE
    if determinant < 0:
        determinant = determinant + ALPHABET_SIZE
    gcd, s, t = eea(ALPHABET_SIZE, determinant)

    det_inverse = t
    print("KEY MATRIX DETERMINANT GENERATION SUCCESSFUL")
    print("Determinant inverse:\n", det_inverse)

    # TRANSPOSE KEY MATRIX GENERATION
    adjoint = adjoint_matrix(key)
    print("ADJOINT MATRIX GENERATION SUCCESSFUL")
    print("Adjoint key matrix:\n", adjoint)

    #MODULAR KEY INVERSE MATRIX GENERATION
    D = (det_inverse * adjoint) % ALPHABET_SIZE
    print("MODULAR KEY INVERSE MATRIX GENERATION SUCCESSFUL")
    print("Modular Key Inverse Matrix:\n", D)
    return D

def encryption(plaintext, K):
    string = ""

    #INTEGER MATRIX GENERATION
    aux_matrix = []
    for i in range(0, len(plaintext), BLOCK_SIZE):
        chunk = plaintext[0 + i: BLOCK_SIZE + i]
        vector = []
        for j in range(len(chunk)):
            vector.append(ord(chunk[j]))
        aux_matrix.append(vector)
    #print(m)  # This print help us to debug how the vector is been constructed

    M = np.array(aux_matrix)
    print("INTEGER MATRIX GENERATION SUCCESSFUL")
    print("Matrix:\n", M)

    #MATRIX AND KEY MULTIPLICATION
    EM = np.dot(M, K) % ALPHABET_SIZE
    print("MATRIX MULTIPLICATION GENERATION SUCCESSFUL")
    print("Multiplied Matrix:\n", EM)

    #TRANSFORMATION TO STRING
    for value in np.nditer(EM):
        string = string + str(chr(value))

    return string

def decryption(ciphertext, key):
    return encryption(ciphertext, modularInverseMatrix(key))

if __name__ == '__main__':
    #MESSAGE
    M = "Meet me at dawn"
    print("Plaintext: ", M)

    #ALPHABET ARRAY GENERATION (ASCII CODE) represented as integer numbers
    for i in range(ALPHABET_SIZE):
        ALPHABET.append(i)

    #KEY GENERATION
    K = keyGeneration()
    print("KEY MATRIX GENERATION SUCCESSFUL")
    print("Key:\n", K)

    #ENCRYPTION
    C = encryption(M,K)
    print("MESSAGE ENCRYPTION SUCCESSFUL")
    print("Ciphertext: ", C)

    #DECRYPTION
    D = decryption(C,K)
    print("MESSAGE DECRYPTION SUCCESSFUL")
    print("Plaintext: ", D)