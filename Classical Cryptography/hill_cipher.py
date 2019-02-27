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

def minor(arr, i, j):
    return np.delete(np.delete(arr, i, axis=0), j, axis=1)

def minorMatrix(matrix, x, y):
    minorM = []
    for i in range(x):
        row = []
        for j in range(y):
            m_minor = minor(matrix, i, j)
            row.append(int(round(np.linalg.det(m_minor))))
        minorM.append(row)
    return np.array(minorM)

def cofactorsMatrix(matrix, x, y):
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

def adjointMatrix(matrix):
    min_matrix = minorMatrix(matrix, BLOCK_SIZE, BLOCK_SIZE)
    cofa_matrix = cofactorsMatrix(min_matrix, BLOCK_SIZE, BLOCK_SIZE)
    adj_matrix = cofa_matrix.transpose()
    return adj_matrix

def readKey(file):
    key_file = open("Texts/" + file + ".txt", "r", encoding='utf-8')
    vals = key_file.readline().replace(" ", "").split(":")
    key_vals = []
    for i in range(0, len(vals)-1, BLOCK_SIZE):
        key_vals.append(list(map(int,vals[i:i+BLOCK_SIZE])))
    return np.array(key_vals)

def keyGeneration(file):
    try:
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

        key_file = open("Texts/" + file + ".txt", "w", encoding='utf-8')
        key_vals = ""
        for i in range(BLOCK_SIZE):
            for j in range(BLOCK_SIZE):
                key_vals += str(key_matrix[i][j]) + ":"
        key_file.write(key_vals)
        key_file.close()
        return True
    except:
        return False

def modularInverseMatrix(key):
    try:
        #KEY MATRIX DETERMINANT GENERATION
        determinant = int(round(np.linalg.det(key))) % ALPHABET_SIZE
        if determinant < 0:
            determinant = determinant + ALPHABET_SIZE
        gcd, s, t = eea(ALPHABET_SIZE, determinant)
        det_inverse = t

        #TRANSPOSE KEY MATRIX GENERATION
        adjoint = adjointMatrix(key)

        #MODULAR KEY INVERSE MATRIX GENERATION
        D = (det_inverse * adjoint) % ALPHABET_SIZE
        return D
    except:
        return "It has no inverse"

def matrixOperations(T, K):
    string = ""
    #INTEGER MATRIX GENERATION
    aux_matrix = []
    for i in range(0, len(T), BLOCK_SIZE):
        chunk = T[0 + i: BLOCK_SIZE + i]
        vector = []
        for j in range(len(chunk)):
            vector.append(ord(chunk[j]))
        aux_matrix.append(vector)
    M = np.array(aux_matrix)

    #MATRIX AND KEY MULTIPLICATION
    EM = np.dot(M, K) % ALPHABET_SIZE

    #TRANSFORMATION TO STRING
    for value in np.nditer(EM):
        string = string + str(chr(value))

    print("Plaintext selected: ", T, "\nMatrix representation", M, "\nCiphertext generated: ", string, "\nMatrix Representation: ", EM)
    return M, EM

def chunks(filename):
    with open("Texts/" + filename, "r", encoding='utf8') as fp:
        chunk = fp.read(BLOCK_SIZE * 3)
        while chunk:
            yield chunk
            chunk = fp.read(BLOCK_SIZE * 3)

def encryption(file, key):
    try:
        #We define the read/write files
        plaintext_file = chunks(file)
        ciphertext_file = open("Texts/" + file + "_hill.py", "w", encoding='utf8')

        #Do encryption by chunks of data to avoid variable overflow
        for chunk in plaintext_file:
            remainder = len(chunk) % BLOCK_SIZE
            if remainder > 0:
                chunk += ' ' * (BLOCK_SIZE - remainder)
            cipher_data = matrixOperations(chunk, key)
            ciphertext_file.write(cipher_data)

        #Finally we close the given files
        plaintext_file.close()
        ciphertext_file.close()
        return True
    except:
        return False

def decryption(file, key):
    try:
        #We define the read/write files
        ciphertext_file = chunks(file)
        plaintext_file = open("Texts/" + file + "_dec.py", "w", encoding='utf8')
        inverse_key = modularInverseMatrix(key)

        #Do decryption by chunks of data to avoid variable overflow
        for chunk in ciphertext_file:
            data = matrixOperations(chunk, inverse_key)
            plaintext_file.write(data)

        #Finally we close the given files
        plaintext_file.close()
        ciphertext_file.close()
        return True
    except:
        return False

if __name__ == '__main__':
    print("========== HILL CIPHER ==========")
    #FILES NAMES
    M = "affine_cipher"
    C = "affine_cipher_hill"
    K = "key_hill"

    #KEY GENERATION
    keyGeneration(K)
    print("KEY MATRIX GENERATION SUCCESSFUL")
    print("Key:\n", readKey(K))

    #ENCRYPTION
    if encryption(M,readKey(K)):
        print("MESSAGE ENCRYPTION SUCCESSFUL")

    #DECRYPTION
    if decryption(C,readKey(K)):
        print("MESSAGE DECRYPTION SUCCESSFUL")