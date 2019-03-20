# Triple DES (or TDES or TDEA or 3DES) is a symmetric block cipher standardized by NIST in SP 800-67 Rev1.
# TDES has a fixed data block size of 8 bytes. It consists of the cascade of 3 Single DES ciphers
# (EDE: Encryption - Decryption - Encryption), where each stage uses an indipendent DES sub-key.

import json
import base64
import time as tm
import numpy as np
import matplotlib.pyplot as plt
from Crypto.Cipher import DES3
from Crypto import Random
from Crypto.Util import Padding
from Crypto.Util import Counter

# Defining constants
# Note: Triple DES keys are 128 bits (Option 1) or 192 bits (Option 2) long. However 1 out of 8 bits
# is used for redundancy and not contribute to security. The effective key length is respectively 112 or 168 bits

KEY_112 = 16  # Size expressed in bytes
KEY_168 = 24  # Size expressed in bytes
SIZE_MODE_EAX = 16  # Expressed in bytes
TEST_FILES = ['test500k.db', 'test1Mb.db', 'test5Mb.db', 'test10Mb.db']
COLORS = ['orange', 'yellow', 'red', 'cyan']
DEMO_FILE = ['']

# Main function declaration
def make_plot(encrypt_times: list, decrypt_times: list, title: str):
    fig, axis = plt.subplots()
    index = np.arange(len(TEST_FILES))
    bar_width = 0.35
    opacity = 0.8

    bars1 = plt.bar(index, encrypt_times, bar_width,
                    alpha=opacity,
                    color='blue',
                    label='Encryption')

    bars2 = plt.bar(index + bar_width, decrypt_times, bar_width,
                    alpha=opacity,
                    color='green',
                    label='Decryption')

    plt.title(title)
    plt.xlabel('File Size')
    plt.ylabel('Time (Seconds)')
    plt.xticks(index + bar_width, TEST_FILES)
    plt.legend()
    plt.show()

def ecb_encryption(file: str, key: bytes) -> list:
    try:
        plaintext = open('3DesFiles/' + file, "rb")
        ciphertext = open('3DesEFiles/' + file, "wb")

        # Encryption
        start = tm.time()
        cipher = DES3.new(key, DES3.MODE_ECB)
        ciphertext.write(cipher.encrypt(Padding.pad(plaintext.read(), DES3.block_size, style='pkcs7')))
        end = tm.time()

        plaintext.close()
        ciphertext.close()
        return True, end-start
    except:
        print("Error at ECB Encryption...")
        exit(1)

def ecb_decryption(file: str, key: bytes) -> list:
    try:
        ciphertext = open('3DesEFiles/' + file, "rb")
        resulttext = open('3DesDFiles/' + file, "wb")

        # Decryption
        start = tm.time()
        cipher = DES3.new(key, DES3.MODE_ECB)
        resulttext.write(Padding.unpad(cipher.decrypt(ciphertext.read()), DES3.block_size, style='pkcs7'))
        end = tm.time()

        ciphertext.close()
        resulttext.close()

        return True, end-start
    except:
        print("Error at ECB Decryption...")
        exit(1)

def cbc_encryption(file: str, key: bytes, iv: bytes) -> list:
    try:
        plaintext = open('3DesFiles/' + file, "rb")
        ciphertext = open('3DesEFiles/' + file, "wb")

        # Encryption
        start = tm.time()
        cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
        ciphertext.write(cipher.encrypt(Padding.pad(plaintext.read(), DES3.block_size, style='pkcs7')))
        end = tm.time()

        plaintext.close()
        ciphertext.close()
        return True, end-start
    except:
        print("Error at CBC Encryption...")
        exit(1)

def cbc_decryption(file: str, key: bytes, iv:bytes) -> list:
    try:
        ciphertext = open('3DesEFiles/' + file, "rb")
        resulttext = open('3DesDFiles/' + file, "wb")

        # Decryption
        start = tm.time()
        cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
        resulttext.write(Padding.unpad(cipher.decrypt(ciphertext.read()), DES3.block_size, style='pkcs7'))
        end = tm.time()

        ciphertext.close()
        resulttext.close()

        return True, end-start
    except:
        print("Error at CBC Decryption...")
        exit(1)

def ofb_encryption(file: str, key: bytes, iv: bytes) -> list:
    try:
        plaintext = open('3DesFiles/' + file, "rb")
        ciphertext = open('3DesEFiles/' + file, "wb")

        # Encryption
        start = tm.time()
        cipher = DES3.new(key, DES3.MODE_OFB, iv=iv)
        ciphertext.write(cipher.encrypt(Padding.pad(plaintext.read(), DES3.block_size, style='pkcs7')))
        end = tm.time()

        plaintext.close()
        ciphertext.close()
        return True, end-start
    except:
        print("Error at OFB Encryption...")
        exit(1)

def ofb_decryption(file: str, key: bytes, iv:bytes) -> list:
    try:
        ciphertext = open('3DesEFiles/' + file, "rb")
        resulttext = open('3DesDFiles/' + file, "wb")

        # Decryption
        start = tm.time()
        cipher = DES3.new(key, DES3.MODE_OFB, iv=iv)
        resulttext.write(Padding.unpad(cipher.decrypt(ciphertext.read()), DES3.block_size, style='pkcs7'))
        end = tm.time()

        ciphertext.close()
        resulttext.close()

        return True, end-start
    except:
        print("Error at OFB Decryption...")
        exit(1)

def ctr_encryption(file: str, key: bytes, ctr) -> list:
    try:
        plaintext = open('3DesFiles/' + file, "rb")
        ciphertext = open('3DesEFiles/' + file, "wb")

        # Encryption
        start = tm.time()
        cipher = DES3.new(key, DES3.MODE_CTR, counter=ctr)
        ciphertext.write(cipher.encrypt(plaintext.read()))
        end = tm.time()

        plaintext.close()
        ciphertext.close()
        return True, end-start
    except:
        print("Error at CFB Encryption...")
        exit(1)

def ctr_decryption(file: str, key: bytes, ctr) -> list:
    try:
        ciphertext = open('3DesEFiles/' + file, "rb")
        resulttext = open('3DesDFiles/' + file, "wb")

        # Decryption
        start = tm.time()
        cipher = DES3.new(key, DES3.MODE_CTR, counter=ctr)
        resulttext.write(cipher.decrypt(ciphertext.read()))
        end = tm.time()

        ciphertext.close()
        resulttext.close()

        return True, end-start
    except:
        print("Error at CFB Decryption...")
        exit(1)

def cfb_encryption(file: str, key: bytes, iv: bytes) -> list:
    try:
        plaintext = open('3DesFiles/' + file, "rb")
        ciphertext = open('3DesEFiles/' + file, "wb")

        # Encryption
        start = tm.time()
        cipher = DES3.new(key, DES3.MODE_CFB, iv=iv, segment_size=8)
        ciphertext.write(cipher.encrypt(plaintext.read()))
        end = tm.time()

        plaintext.close()
        ciphertext.close()
        return True, end-start
    except:
        print("Error at CFB Encryption...")
        exit(1)

def cfb_decryption(file: str, key: bytes, iv:bytes) -> list:
    try:
        ciphertext = open('3DesEFiles/' + file, "rb")
        resulttext = open('3DesDFiles/' + file, "wb")

        # Decryption
        start = tm.time()
        cipher = DES3.new(key, DES3.MODE_CFB, iv=iv, segment_size=8)
        resulttext.write(cipher.decrypt(ciphertext.read()))
        end = tm.time()

        ciphertext.close()
        resulttext.close()

        return True, end-start
    except:
        print("Error at CFB Decryption...")
        exit(1)

if __name__ == '__main__':
    # Generation of our pseudorandom key base64
    print("================ KEY GENERATION ================\n")
    # Store it into a file
    key_file = open('Keys/3des_key.txt', "w", encoding='utf8')
    # Avoid Option 3
    while True:
        try:
            generated_key = DES3.adjust_key_parity(Random.get_random_bytes(KEY_112))
            break
        except ValueError:
            pass

    # Encoding key in base64 and dumping it into a json format
    key64 = base64.b64encode(generated_key).decode('utf-8')
    json_key = json.dumps({'key':key64})
    # Write to file
    key_file.write(json_key)
    # Close file
    key_file.close()

    print("================ INITIALIZATION VECTOR GENERATION ================\n")
    # Store it into a file
    iv_file = open('Keys/3des_iv.txt', "w", encoding='utf8')
    # Initialization vector generation
    iv64 = base64.b64encode(Random.get_random_bytes(DES3.block_size)).decode('utf-8')
    json_iv = json.dumps({'iv':iv64})
    # Write to file
    iv_file.write(json_iv)
    # Close file
    iv_file.close()

    print("================ KEY READ ================\n")
    # Read from file
    key_file = open('Keys/3des_key.txt', "r", encoding='utf8')
    # Extract Json format
    b64 = json.loads(key_file.readline())
    # Decode base64 value
    key = base64.b64decode(b64['key'])

    print("================ INITIALIZATION VECTOR READ ================\n")
    # Read from file
    iv_file = open('Keys/3des_iv.txt', "r", encoding='utf8')
    # Extract Json format
    b64 = json.loads(iv_file.readline())
    # Decode base64 value
    iv = base64.b64decode(b64['iv'])

    # ================ ECB MODE================#
    encrypt_times = []
    decrypt_times = []
    for i in range(len(TEST_FILES)):
        print("\n================ ECB MODE================")
        print("Doing test to: " + TEST_FILES[i])

        print("================ ENCRYPTION ================")
        sucess, exec_time = ecb_encryption(TEST_FILES[i], key)
        if sucess:
            print("Ciphertext Execution time: " + str(exec_time))
            encrypt_times.append(exec_time)

        print("================ DECRYPTION ================")
        sucess, exec_time = ecb_decryption(TEST_FILES[i], key)
        if sucess:
            print("Resulttext: Execution time: " + str(exec_time) + "\n")
            decrypt_times.append(exec_time)

    #Create plot
    make_plot(encrypt_times, decrypt_times, 'ECB MODE')

    # ================ CBC MODE================#
    encrypt_times = []
    decrypt_times = []
    for i in range(len(TEST_FILES)):
        print("\n================ CBC MODE================")
        print("Doing test to: " + TEST_FILES[i])

        print("================ ENCRYPTION ================")
        sucess, exec_time = cbc_encryption(TEST_FILES[i], key, iv)
        if sucess:
            print("Ciphertext Execution time: " + str(exec_time))
            encrypt_times.append(exec_time)

        print("================ DECRYPTION ================")
        sucess, exec_time = cbc_decryption(TEST_FILES[i], key, iv)
        if sucess:
            print("Resulttext: Execution time: " + str(exec_time) + "\n")
            decrypt_times.append(exec_time)

    # Create plot
    make_plot(encrypt_times, decrypt_times, 'CBC MODE')

    # ================ OFB MODE================#
    print("================ OFB MODE================")
    encrypt_times = []
    decrypt_times = []
    for i in range(len(TEST_FILES)):
        print("\n================ OFB MODE================")
        print("Doing test to: " + TEST_FILES[i])

        print("================ ENCRYPTION ================")
        sucess, exec_time = ofb_encryption(TEST_FILES[i], key, iv)
        if sucess:
            print("Ciphertext Execution time: " + str(exec_time))
            encrypt_times.append(exec_time)

        print("================ DECRYPTION ================")
        sucess, exec_time = ofb_decryption(TEST_FILES[i], key, iv)
        if sucess:
            print("Resulttext: Execution time: " + str(exec_time) + "\n")
            decrypt_times.append(exec_time)

    # Create plot
    make_plot(encrypt_times, decrypt_times, 'OFB MODE')

    # ================ CTR MODE================#
    # Fixed nonce value generation
    nonce = Random.new().read(int(DES3.block_size / 2))
    # Counter object generation
    ctr = Counter.new(int(DES3.block_size * 8 / 2), prefix=nonce)

    encrypt_times = []
    decrypt_times = []
    for i in range(len(TEST_FILES)):
        print("\n================ CTR MODE================")
        print("Doing test to: " + TEST_FILES[i])

        print("================ ENCRYPTION ================")
        sucess, exec_time = ctr_encryption(TEST_FILES[i], key, ctr)
        if sucess:
            print("Ciphertext Execution time: " + str(exec_time))
            encrypt_times.append(exec_time)

        print("================ DECRYPTION ================")
        sucess, exec_time = ctr_decryption(TEST_FILES[i], key, ctr)
        if sucess:
            print("Resulttext: Execution time: " + str(exec_time) + "\n")
            decrypt_times.append(exec_time)

    # Create plot
    make_plot(encrypt_times, decrypt_times, 'CTR MODE')

    # ================ CFB MODE================#
    print("================ CFB MODE================")
    encrypt_times = []
    decrypt_times = []
    for i in range(len(TEST_FILES)):
        print("\n================ CFB MODE================")
        print("Doing test to: " + TEST_FILES[i])

        print("================ ENCRYPTION ================")
        sucess, exec_time = cfb_encryption(TEST_FILES[i], key, iv)
        if sucess:
            print("Ciphertext Execution time: " + str(exec_time))
            encrypt_times.append(exec_time)

        print("================ DECRYPTION ================")
        sucess, exec_time = cfb_decryption(TEST_FILES[i], key, iv)
        if sucess:
            print("Resulttext: Execution time: " + str(exec_time) + "\n")
            decrypt_times.append(exec_time)

    # Create plot
    make_plot(encrypt_times, decrypt_times, 'CFB MODE')

    # Close files
    iv_file.close()
    key_file.close()