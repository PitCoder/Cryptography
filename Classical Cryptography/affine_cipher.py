#Implementation of the affine cipher
#Let x,y,a,b belong to Z27
#Encryption: ek(x) = a per x + b mod 26
#Decryption: dk(y) = a' per (y - b) mod 26, with the key k = (a, b), which has the restriction: gdc(a,26) = 1

from math import gcd

alphabet = []
alphabet_size = 0

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
            mul_ab = (a * b) % alphabet_size
            table_row.append(mul_ab)
        mul_table.append(table_row)
    return mul_table

def find_inverse(mul_table, index):
    try:
        inverse_index = mul_table[index].index(1)
        return int(mul_table[0][inverse_index])
    except:
        return -1


def encrypt(plaintext):
    # Then we proceed to do the encryption
    ciphertext = ""
    for i in range(len(plaintext)):
        x = alphabet.index(plaintext[i])
        shifted_char = ((a * x) + b) % alphabet_size
        ciphertext = ciphertext + alphabet[shifted_char]
    return ciphertext


def decrypt(ciphertext):
    # Then we proceed to do the decryption
    dec_plaintext = ""
    for i in range(len(ciphertext)):
        y = alphabet.index(ciphertext[i])
        shifted_char = (a_inverse * (y - b)) % alphabet_size
        dec_plaintext = dec_plaintext + alphabet[shifted_char]
    return dec_plaintext

if __name__ == '__main__':
    print("============= AFFINE CIPHER =============")
    #======== Sample alphabets ========
    #Spanish alphabet: a,b,c,d,e,f,g,h,i,j,k,l,m,n,ñ,o,p,q,r,s,t,u,v,w,x,y,z
    #English alphabet: a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z

    alphabet = str(
        input("\nPlease insert the alphabet you want to use by inserting each letter separated by comma: ")
        .replace("\s", "")).split(",")

    print("Inserted alphabet: ", alphabet)
    alphabet_size = len(alphabet)
    print("Alphabet size: ", alphabet_size)

    key = str(input("Please insert the key (a,b): ").replace(" ", "")).split(",")
    a = int(key[0])
    b = int(key[1])

    #First we calculate the prime factors of the alphabet
    prime_factors = phi(alphabet_size)
    print("Prime factors of ", alphabet_size, ": ", prime_factors)

    #Then we create the multiplication table
    mul_table = create_multable(prime_factors)
    print("Multiplication table for spanish alphabet: ")
    for row in mul_table:
        print(row)

    # We find the inverse of the value a
    a_inverse = find_inverse(mul_table, prime_factors.index(int(a)))

    #We validate that a is a valid value for the key
    if(a_inverse > 0):
        print("Inverse of ", a, " : ", a_inverse)

        #Then we select an operation mode
        operation_mode = int(input("\nSelect an operation mode (0:Encrypt, 1:Decrypt): "))

        if operation_mode == 0:
            file_read = open("plaintext_file.txt", "r", encoding = 'utf-8')
            file_write = open("ciphertext_file.txt", "w", encoding = 'utf-8')

            for line in file_read:
                sentence = "".join(line.split()).lower()
                if len(sentence) > 0:
                    c_sentence = encrypt(sentence)
                    file_write.write(c_sentence + "\n")

            file_read.close()
            file_write.close()
        elif operation_mode == 1:
            file_read = open("ciphertext_file.txt", "r", encoding='utf-8')
            file_write = open("decryptedtext_file.txt", "w", encoding='utf-8')

            for line in file_read:
                sentence = "".join(line.split()).lower()
                if len(sentence) > 0:
                    d_sentence = decrypt(sentence)
                    file_write.write(d_sentence + "\n")

            file_read.close()
            file_write.close()
        else:
            print("Bad selection on operation mode :c")
    else:
        print("Invalid value for a in key")