# Baby Rijndael
# Scaled down version of Rijndael (AES Cipher).
# Similar algorithms, but smaller algebraic structures

# Author: Eric Alejandro López Ayala
# Date: March 11th 2019

from bitstring import BitArray, BitStream
import numpy as np

# Define algorithm constants
# Number of rounds
ROUNDS_NO = 4
HEX_SIZE = 4

# Sustitution Box
'''
SBOX = ['1010','0100','0011','1011',
         '1000','1110','0010','1100',
         '0101','0111','0110','1111',
         '0000','0001','1001','1101']
'''
SBOX = [10, 4, 3, 11,
        8, 14, 2, 12,
        5, 7, 6, 15,
        0, 1, 9, 13]

# Inverse Sustitution Box
INVERSE_SBOX = ['1100', '1101', '0110', '0010',
                '0001', '1000', '1010', '1001',
                '0100', '1110', '0000', '0011',
                '0111', '1111', '0101', '1011']

'''
#Transformation matrix
T = ['10100011',
     '11010001',
     '11101000',
     '01010111',
     '00111010',
     '00011101',
     '10001110',
     '01110101']
'''
T = np.array([163, 209, 232, 87, 58, 29, 142, 117])

# Inverse transformation matrix
'''
INVERSE_T = ['00100101',
     '10011010',
     '11001101',
     '01001011',
     '01010010',
     '10101001',
     '11011100',
     '10110100']
'''
INVERSE_T = np.array([37, 154, 205, 75, 82, 169, 220, 180])


def sustitution(values: np.array) -> np.array:
    for i in range(0, len(values)):
        values[i] = SBOX[values[i]]
    return values


def reverse(values: np.array) -> np.array:
    if len(values) == 2:
        temp = values[0]
        values[0] = values[1]
        values[1] = temp
    else:
        temp = values[1]
        values[1] = values[3]
        values[3] = temp
    return values


def constant(round: int) -> np.array:
    return np.array([2 ** (round - 1), 0])


def roundKeyGeneration(key: BitArray) -> np.array:
    input_key = str(key.bin)
    init_w = []

    for i in range(0, len(input_key), HEX_SIZE):
        init_w.append(int(input_key[0 + i: HEX_SIZE + i], 2))

    w = np.array([])

    for i in range(0, ROUNDS_NO + 1):
        if i == 0:
            w0 = np.array(init_w[0:2])
            w1 = np.array(init_w[2:4])
            w = np.vstack((w0, w1))
        else:
            w2i = w[2 * i - 2] ^ sustitution(reverse(list(w[2 * i - 1]))) ^ constant(i)
            w = np.vstack((w, w2i))
            w2i_1 = w[2 * i] ^ w[(2 * i) - 1]
            w = np.vstack((w, w2i_1))
    return w

def transform(state: np.array) -> np.array:
    return np.dot(state, T)

def encryption(plaintext: BitArray, key: BitArray) -> BitArray:
    # Step 1: load the input block into the state
    input_block = str(plaintext.bin)

    state = []
    for i in range(0, len(input_block), HEX_SIZE):
        state.append(int(input_block[0 + i: HEX_SIZE + i], 2))

    a = np.array(state)

    # a = matrix_representation(list(state))
    sub_keys = roundKeyGeneration(key)
    round_key = np.append(sub_keys[0], sub_keys[1])

    a = a ^ round_key

    # Step 2: Apply the sustitution box to the state
    a = sustitution(a)
    # Step 3: Apply the reverse function the the state
    a = reverse(a)
    # Step 4: Apply the transformation "t" to the state
    print(a.shape)
    #a = transform(a)

    print(a)


# def decryption(ciphertext: BitArray, key: BitArray) -> BitArray:

if __name__ == '__main__':
    plaintext = BitArray("0x2ca5")
    key = BitArray("0x6b5d")

    encryption(plaintext, key)
