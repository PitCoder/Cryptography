#Implementation of the affine cipher
#Let x,y,a,b belong to Z27
#Encryption: ek(x) = a per x + b mod 26
#Decryption: dk(y) = a' per (y - b) mod 26, with the key k = (a, b), which has the restriction: gdc(a,26) = 1

from math import gcd

alphabet = ['a', 'b', 'c', 'd', 'e',  'f',  'g', 'h', 'i',  'j', 'k',  'l', 'm', 'n', 'ñ', 'o',  'p', 'q' , 'r', 's',  't', 'u', 'v', 'w', 'x', 'y', 'z']

def phi(n):
    phi_values = [1]
    for p in range(2, n):
        if gcd(p, n) == 1:
            phi_values.append(p)
    return phi_values

def create_multable(prime_factors):
    # We start the constrution of the multiplication table for Zn
    mul_table = []

    # Naive implementation for the construction of the multiplication table
    for i in range(len(prime_factors)):
        a = prime_factors[i]
        table_row = []
        for j in range(len(prime_factors)):
            b = prime_factors[j]
            mul_ab = (a * b) % 27
            table_row.append(mul_ab)
        mul_table.append(table_row)
    return mul_table

def find_inverse(mul_table, index):
    inverse_index = mul_table[index].index(1)
    return int(mul_table[0][inverse_index])


def encrypt(plaintext):
    # Then we proceed to do the encryption
    ciphertext = ""
    for i in range(len(plaintext)):
        x = alphabet.index(plaintext[i])
        shifted_char = ((a * x) + b) % 27
        ciphertext = ciphertext + alphabet[shifted_char]
    return ciphertext


def decrypt(ciphertext):
    # Then we proceed to do the decryption
    dec_plaintext = ""
    for i in range(len(ciphertext)):
        y = alphabet.index(ciphertext[i])
        shifted_char = (a_inverse * (y - b)) % 27
        dec_plaintext = dec_plaintext + alphabet[shifted_char]
    return dec_plaintext

if __name__ == '__main__':
    '''
    plaintext = str(input("Please insert the plaintext message: ").replace(" ",""))
    '''
    key = str(input("Please insert the key (a,b): ").replace(" ","")).split(",")

    a = int(key[0])
    b = int(key [1])

    #First we calculate the prime factors of the alphabet
    prime_factors = phi(27)
    print("Prime factors of 27: ", prime_factors)

    #Then we create the multiplication table
    mul_table = create_multable(prime_factors)
    print("Multiplication table for spanish alphabet: ")
    for row in mul_table:
        print(row)

    #We find the inverse of the value a
    a_inverse = find_inverse(mul_table, prime_factors.index(int(a)))
    print("Inverse of ", a, " : ", a_inverse)

    '''
    ciphertext = encrypt(plaintext)
    dec_plaintext = decrypt(ciphertext)

    # Printing the results
    print("Original text: ", plaintext)
    print("Encrypted text: ", ciphertext)
    print("Decrypted text: ", dec_plaintext)
    '''

    # Test
    ciphertext = str(input("Please insert the ciphertext message: ").replace(" ",""))
    dec_plaintext = decrypt(ciphertext)

    # Printing the results
    print("Encrypted text: ", ciphertext)
    print("Decrypted text: ", dec_plaintext)