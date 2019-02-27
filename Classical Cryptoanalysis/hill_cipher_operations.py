import numpy as np
from random import randint
from extended_euclidean_algorithm import *


# UTILS OPERATIONS
# ===============================================================

# This function converts a data stream string into its representation as matrix of integers
def integer_convertion(data_stream: int, block_size: int) -> np.array:
    integer_matrix = []
    for i in range(0, len(data_stream), block_size):
        chunk = data_stream[0 + i:block_size + i]
        vector = []
        for j in range(len(chunk)):
            vector.append(ord(chunk[j]))
        integer_matrix.append(vector)
    return np.array(integer_matrix)


# This function converts an integer matrix into its representation as data stream string
def character_convertion(matrix: np.array) -> str:
    string = ""
    for value in np.nditer(matrix):
        string += str(chr(value))
    return string


# This function represents an integer matrix into its key representation as data stream string
def key_convertion(matrix: np.array, block_size: int) -> str:
    string = ""
    for value in np.nditer(matrix):
        string += str(value) + ":"
    return string


# This function performs a dot matrix operation between matrix a and matrix b
def matrix_operation(matrix_a: np.array, matrix_b: np.array, modulo: int) -> np.array:
    return np.dot(matrix_a, matrix_b) % modulo


# This function split the data of a file into chucks
def chunks(filename: str, block_size: int) -> []:
    with open(filename, "r", encoding='utf8') as fp:
        chunk = fp.read(block_size ** 2)
        while chunk:
            yield chunk
            chunk = fp.read(block_size ** 2)


# This function generates a new key given a block size and stores it into a file
def key_generation(filename, block_size):
    try:
        # VARIABLE DEFINITION
        key_matrix = []
        is_inverse = False

        while not is_inverse:
            # CANDIDATE MATRIX GENERATION
            key_matrix = []
            for i in range(block_size):
                row = []
                for j in range(block_size):
                    row.append(randint(0, 256))
                key_matrix.append(row)

            # CANDIDATE MATRIX VALIDATION
            determinant = int(round(np.linalg.det(key_matrix))) % 256
            if determinant < 0:
                determinant = determinant + 256

            gdc, s, t = eea(256, determinant)
            if gdc == 1:
                is_inverse = True

        key_file = open(filename, "w", encoding='utf-8')
        key_vals = ""
        for i in range(block_size):
            for j in range(block_size):
                key_vals += str(key_matrix[i][j]) + ":"
        key_file.write(key_vals)
        key_file.close()
        return True
    except:
        return False


# This function read a given key file and transform it into a integer matrix
def read_key(filename: str, block_size: int) -> np.array:
    key_file = open(filename, "r", encoding='utf-8')
    values = key_file.readline().replace(" ", "").split(":")
    key_values = []
    for i in range(0, len(values) - 1, block_size):
        key_values.append(list(map(int, values[i:i + block_size])))
    return np.array(key_values)


# ===============================================================

# MATRIX OPERATIONS
# ===============================================================

# This function extract the submatrix(given the x,y index)
def sub_matrix(arr: np.array, i: int, j: int) -> np.array:
    return np.delete(np.delete(arr, i, axis=0), j, axis=1)


# This function computes the minor matrix of a given matrix
def minor_matrix(matrix: np.array, x: int, y: int) -> np.array:
    min_matrix = []
    for i in range(x):
        row = []
        for j in range(y):
            minor = sub_matrix(matrix, i, j)
            row.append(int(round(np.linalg.det(minor))))
        min_matrix.append(row)
    return np.array(min_matrix)


# This function computes the cofactor matrix of a given matrix
def cofactor_matrix(matrix: np.array, x: int, y: int) -> np.array:
    cof_matrix = []
    sign_value = 1
    for i in range(x):
        row = []
        for j in range(y):
            if (i + j) % 2 == 0:
                sign_value = 1
            else:
                sign_value = -1
            row.append(matrix[i][j] * sign_value)
        cof_matrix.append(row)
    return np.array(cof_matrix)


# This function computes the adjoint matrix of a given matrix
def adjoint_matrix(matrix: np.array, x: int, y: int) -> np.array:
    min_matrix = minor_matrix(matrix, x, y)
    cof_matrix = cofactor_matrix(min_matrix, x, y)
    return cof_matrix.transpose()


# This function computes the inverse matrix of a given matrix
def inverse_matrix(matrix: np.array, modulo: int) -> np.array:
    try:
        # Matrix determinant calculus
        determinant = int(round(np.linalg.det(matrix))) % modulo
        if determinant < 0:
            determinant = determinant + modulo
        gcd, s, t = eea(modulo, determinant)
        determinant_inverse = t

        # Adjoint matrix generation
        adjoint = adjoint_matrix(matrix, len(matrix), len(matrix))

        # Inverse matrix calculus
        inverse_matrix = (determinant_inverse * adjoint) % modulo
        return inverse_matrix
    except:
        return np.array([])


# ===============================================================

# MATRIX OPERATIONS
# ===============================================================

# This function do the encryption process by implementing the hill cipher algorithm
def encryption(plaintext_filename: str, ciphertext_filename: str, key_filename: str, block_size: int) -> bool:
    plaintext = chunks(plaintext_filename, block_size)
    ciphertext = open(ciphertext_filename, "w", encoding='utf8')
    key = read_key(key_filename, block_size)

    # Do encryption by chunks of data to avoid variable overflow
    for chunk in plaintext:
        remainder = len(chunk) % block_size
        if remainder > 0:
            chunk += ' ' * (block_size - remainder)
        cipher_data = character_convertion(matrix_operation(integer_convertion(chunk, block_size), key, 256))
        ciphertext.write(cipher_data)

    # Finally we close the given files
    plaintext.close()
    ciphertext.close()
    return True


# This function do the encryption process by implementing the hill cipher algorithm
def decryption(ciphertext_filename: str, resulttext_filename: str, key_filename: str, block_size: int) -> bool:
    ciphertext = chunks(ciphertext_filename, block_size)
    resulttext = open(resulttext_filename, "w", encoding='utf8')
    inverse_key = inverse_matrix(read_key(key_filename, block_size), 256)

    # Do decryption by chunks of data to avoid variable overflow
    for chunk in ciphertext:
        data = character_convertion(matrix_operation(integer_convertion(chunk, block_size), inverse_key, 256))
        resulttext.write(data)

    # Finally we close the given files
    ciphertext.close()
    resulttext.close()
    return True

# ===============================================================
