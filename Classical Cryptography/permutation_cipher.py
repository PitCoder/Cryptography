'''
Permutation Cipher (Transposition Cipher)

The basic idea of a permutation cipher is to keep the plaintext characters unchanged, but to alter their
positions by rearranging them using a permutation.

The permutation cipher is considered as a special case of the hill cipher, because we just need to generate
a permuation matrix of ones and operate as we do in hill cipher

@Author: Eric Alejandro López Ayala
@Date: February 17th 2019
'''

import numpy as np
import itertools as it
from random import randint
from extended_euclidean_algorithm import *

#BLOCK SIZE DEFINITION
BLOCK_SIZE = 5
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

def generatePermutationMatrix():
    M = []
    for i in range(BLOCK_SIZE):
        M.append([1 if j == i else 0 for j in range(BLOCK_SIZE)])
    return M

def keyGeneration(file):
    try:
        #DIAGONAL MATRIX GENERATION
        diagonal_matrix = generatePermutationMatrix()
        #GENERATION OF MATRIX'S PERMUTATIONS
        P = list(it.permutations(diagonal_matrix))
        #SELECTION OF THE KEY PERMUTATION
        key_matrix = np.array(P[randint(1, len(P) - 1)])

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

def modularInverseMatrix(P):
    #KEY MATRIX DETERMINANT GENERATION
    determinant = int(round(np.linalg.det(P))) % ALPHABET_SIZE
    if determinant < 0:
        determinant = determinant + ALPHABET_SIZE
    gcd, s, t = eea(ALPHABET_SIZE, determinant)
    det_inverse = t

    #TRANSPOSE KEY MATRIX GENERATION
    adjoint = adjointMatrix(P)

    #MODULAR KEY INVERSE MATRIX GENERATION
    D = (det_inverse * adjoint) % ALPHABET_SIZE
    return D

def matrixOperations(T, P):
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
    EM = np.dot(M, P) % ALPHABET_SIZE

    #TRANSFORMATION TO STRING
    for value in np.nditer(EM):
        string = string + str(chr(value))
    return string

def chunks(filename):
    with open("Texts/" + filename + ".txt", "r", encoding='utf8') as fp:
        chunk = fp.read(BLOCK_SIZE * 3)
        while chunk:
            yield chunk
            chunk = fp.read(BLOCK_SIZE * 3)

def encryption(file, key):
    try:
        #We define the read/write files
        plaintext_file = chunks(file)
        ciphertext_file = open("Texts/" + file + "_perm.txt", "w", encoding='utf8')

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
        plaintext_file = open("Texts/" + file + "_dperm.txt", "w", encoding='utf8')
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


def decryption(file, key):
    try:
        #We define the read/write files
        ciphertext_file = chunks(file)
        plaintext_file = open("Texts/" + file + "_dec.txt", "w", encoding='utf8')
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
    print("========== PERMUTATION CIPHER ==========")
    # FILES NAMES
    M = "cicero_letter"
    C = "cicero_letter_perm"
    K = "key_perm"

    # KEY GENERATION
    keyGeneration(K)
    print("KEY PERMUTATION MATRIX GENERATION SUCCESSFUL")
    print("Key:\n", readKey(K))

    # ENCRYPTION
    if encryption(M, readKey(K)):
        print("MESSAGE ENCRYPTION SUCCESSFUL")

    # DECRYPTION
    if decryption(C, readKey(K)):
        print("MESSAGE DECRYPTION SUCCESSFUL")