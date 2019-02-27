#Implementation of the affine cipher
#Let x,y,a,b belong to Z27
#Encryption: ek(x) = a per x + b mod 26
#Decryption: dk(y) = a' per (y - b) mod 26, with the key k = (a, b), which has the restriction: gdc(a,26) = 1

from math import gcd
from extended_euclidean_algorithm import *

ASCII_SIZE = 256

def encrypt(plaintext):
    # Then we proceed to do the encryption
    ciphertext = ""
    for i in range(len(plaintext)):
        x = ord(plaintext[i])
        shifted_char = ((a * x) + b) % ASCII_SIZE
        ciphertext = ciphertext + str(chr(shifted_char))
    return ciphertext

def decrypt(ciphertext):
    # Then we proceed to do the decryption
    dec_plaintext = ""
    for i in range(len(ciphertext)):
        y = ord(ciphertext[i])
        shifted_char = (a_inverse * (y - b)) % ASCII_SIZE
        dec_plaintext = dec_plaintext + str(chr(shifted_char))
    return dec_plaintext

if __name__ == '__main__':
    print("============= AFFINE CIPHER =============")
    key = str(input("Please insert the key (a,b): ").replace(" ", "")).split(",")
    a = int(key[0])
    b = int(key[1])

    # We find the inverse of the value a
    # We validate that a is a valid value for the key
    if a >= 0 and a <= ASCII_SIZE:
        gcd, s, t = eea(ASCII_SIZE, a)
        if(gcd == 1):
            print("a is a valid value for the key :)")
            if(t < 0):
                a_inverse = int(ASCII_SIZE) + t
            else:
                a_inverse = t

            print("Inverse of ", a, " : ", a_inverse)
            #Then we select an operation mode
            operation_mode = int(input("\nSelect an operation mode (0:Encrypt, 1:Decrypt): "))

            if operation_mode == 0:
                file_read = open("Texts/plaintext_file.txt", "r", encoding = 'utf-8')
                file_write = open("Texts/ciphertext_file.txt", "w", encoding = 'utf-8')

                for sentence in file_read:
                    if len(sentence) > 0:
                        c_sentence = encrypt(sentence)
                        file_write.write(c_sentence)

                file_read.close()
                file_write.close()
            elif operation_mode == 1:
                file_read = open("Texts/ciphertext_file.txt", "r", encoding='utf-8')
                file_write = open("Texts/decryptedtext_file.txt", "w", encoding='utf-8')

                for sentence in file_read:
                    if len(sentence) > 0:
                        d_sentence = decrypt(sentence)
                        file_write.write(d_sentence)
                file_read.close()
                file_write.close()
            else:
                print("Bad selection on operation mode :c")
        else:
            print("Invalid value for a in key")