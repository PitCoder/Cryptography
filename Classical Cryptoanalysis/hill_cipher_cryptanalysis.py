from tkinter.filedialog import askopenfilename
from hill_cipher_operations import *


def generate_datalist(data, block_size):
    datalist = []
    for chunk in data:
        remainder = len(chunk) % block_size
        if remainder > 0:
            chunk += ' ' * (block_size - remainder)
        matrix_data = integer_convertion(chunk, block_size)
        datalist.append(matrix_data)
    return datalist

def is_invertible(matrix: np.array) -> bool:
    ALPHABET_SIZE = 256
    is_inverse = False

    # CANDIDATE MATRIX VALIDATION
    determinant = int(round(np.linalg.det(matrix))) % ALPHABET_SIZE
    if determinant < 0:
        determinant = determinant + ALPHABET_SIZE

    gdc, s, t = eea(ALPHABET_SIZE, determinant)
    if gdc == 1:
        is_inverse = True

    return is_inverse

def do_matrix_analysis(plaintext_filename: str, ciphertext_filename: str, block_size: int):
    print("=============== PROCESSING FILES ================")
    analysistext = open('Texts/analysis.txt', "w", encoding='utf8')
    plaintext_datalist = generate_datalist(chunks(plaintext_filename, block_size), block_size)
    ciphertext_datalist = generate_datalist(chunks(ciphertext_filename, block_size), block_size)

    print("=============== GENERATION OF POSSIBLE KEYS ================")
    for i in range(len(plaintext_datalist)):
        E = plaintext_datalist[i]
        C = ciphertext_datalist[i]

        if(len(E) % block_size == 0):
            if is_invertible(E):
                E_inverse = inverse_matrix(E, 256)
                K = np.dot(E_inverse, C) % 256
                analysistext.write(key_convertion(K, block_size) + "\n")
            else:
                analysistext.write("Key not suitable\n")

    # Finally we close the given files
    analysistext.close()
    return True


if __name__ == '__main__':
    # Read plaintext file
    M = str(askopenfilename())
    path = M[: M.rfind('/') + 1]

    # Original key filename
    K = path + "key.txt"
    # Ciphertext filename
    C =  path + "ciphertext.txt"
    # Resulttext filename
    D = path + "resulttext.txt"
    # Block size
    BLOCK_SIZE = 3

    # Do keygen
    if key_generation(K, BLOCK_SIZE):
        print("KEYGEN SUCCESSFUL")
    else:
        print("KEYGEN FAILURE")

    #Do encryption
    if encryption(M, C, K, BLOCK_SIZE):
        print("ENCRYPTION SUCCESSFUL")
    else:
        print("ENCRYPTION FAILURE")

    '''
    #Do decryption
    if decryption(C, D, K, BLOCK_SIZE):
        print("DECRYPTION SUCCESSFUL")
    else:
        print("DECRYPTION FAILURE")
        '''

    if do_matrix_analysis(M, C, BLOCK_SIZE):
        print("ANALYSIS COMPLETED")
    else:
        print("ENCRYPTION FAILURE")

