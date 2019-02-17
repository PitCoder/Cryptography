import numpy as np #We import numpy for a better management and math-wise operations on matrices
from random import randint #From random library we import random to generate the values of our matrix
from math import gcd #From math library we import the greatest common divisor function to verify the invertibility of the matrix

def generateSquareMatrix(n, module):
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(randint(0, module))
        matrix.append(row)
    return matrix

if __name__ == '__main__':
    ALPHABET_SIZE = 26 #This variable represent the size of the alphabet
    MATRIX_LEN = 3 #This variable represents the value N of our square matrix
    M = [] #This variable is our generated matrix
    determinant = 0
    is_inverse = False #Boolean condition for iterations

    while not is_inverse:
        M = generateSquareMatrix(MATRIX_LEN, ALPHABET_SIZE)
        determinant = int(np.linalg.det(M))
        if gcd(ALPHABET_SIZE, determinant % ALPHABET_SIZE) == 1:
            is_inverse =  True

    print("Matrix:")
    for row in M:
        print(row)
    print("\nDeterminant: ", determinant % ALPHABET_SIZE)