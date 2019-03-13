# Triple DES (or TDES or TDEA or 3DES) is a symmetric block cipher standardized by NIST in SP 800-67 Rev1.
# TDES has a fixed data block size of 8 bytes. It consists of the cascade of 3 Single DES ciphers
# (EDE: Encryption - Decryption - Encryption), where each stage uses an indipendent DES sub-key.

import json
import base64
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

# Main function declaration
if __name__ == '__main__':
    # Generation of our pseudorandom key base64

    # Store it into a file
    key_file = open('Keys/3des_key.txt', "w", encoding='utf8')

    # Avoid Option 3
    while True:
        try:
            key = DES3.adjust_key_parity(Random.get_random_bytes(KEY_112))
            break
        except ValueError:
            pass

    key_file.write(str(base64.b64encode(key), encoding="utf-8"))
    key_file.close()

    # ================ ECB MODE================#
    print("================ ECB MODE================")
    # Encryption
    cipher = DES3.new(key, DES3.MODE_ECB)
    ciphertext = cipher.encrypt(Padding.pad(b'Hello World', DES3.block_size, style='pkcs7'))
    print("Ciphertext: " + str(ciphertext))

    # Decryption
    plaintext = Padding.unpad(cipher.decrypt(ciphertext), DES3.block_size, style='pkcs7')
    print("Plaintext: " + str(plaintext) + "\n")

    # ================ CBC MODE================#
    print("================ CBC MODE================")
    # Initialization vector generation
    initialization_vector = Random.get_random_bytes(DES3.block_size)

    # Encryption
    cipher = DES3.new(key, DES3.MODE_CBC, iv=initialization_vector)
    ciphertext = cipher.encrypt(Padding.pad(b'Hello World', DES3.block_size, style='pkcs7'))
    print("Ciphertext: " + str(ciphertext))

    # Base64 Encoding
    iv_base64 = str(base64.b64encode(initialization_vector), encoding="utf-8")
    print("IV (encoded): " + iv_base64)

    # Base64 Decoding
    iv = base64.b64decode(iv_base64)
    print("IV (decoded): " + str(iv))

    # Decryption
    cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
    plaintext = Padding.unpad(cipher.decrypt(ciphertext), DES3.block_size, style='pkcs7')
    print("Plaintext: " + str(plaintext) + "\n")

    # ================ CTR MODE================#
    print("================ CTR MODE================")
    # Fixed nonce value generation
    nonce = Random.new().read(int(DES3.block_size / 2))

    # Counter object generation
    ctr = Counter.new(int(DES3.block_size * 8 / 2), prefix=nonce)

    # Encryption (Padding is not needed)
    cipher = DES3.new(key, DES3.MODE_CTR, counter=ctr)
    ciphertext = cipher.encrypt(b'Hello World')
    print("Ciphertext: " + str(ciphertext))

    # Decryption (Padding is not needed)
    cipher = DES3.new(key, DES3.MODE_CTR, counter=ctr)
    plaintext = cipher.decrypt(ciphertext)
    print("Plaintext: " + str(plaintext) + "\n")

    # ================ OFB MODE================#
    print("================ CFB MODE================")
    # Initialization vector generation
    initialization_vector = Random.get_random_bytes(DES3.block_size)

    # Encryption
    cipher = DES3.new(key, DES3.MODE_OFB, iv=initialization_vector)
    ciphertext = cipher.encrypt(Padding.pad(b'Hello World', DES3.block_size, style='pkcs7'))
    print("Ciphertext: " + str(ciphertext))

    # Base64 Encoding
    iv_base64 = str(base64.b64encode(initialization_vector), encoding="utf-8")
    print("IV (encoded): " + iv_base64)

    # Base64 Decoding
    iv = base64.b64decode(iv_base64)
    print("IV (decoded): " + str(iv))

    # Decryption
    cipher = DES3.new(key, DES3.MODE_OFB, iv=iv)
    plaintext = Padding.unpad(cipher.decrypt(ciphertext), DES3.block_size, style='pkcs7')
    print("Plaintext: " + str(plaintext) + "\n")

    # ================ CFB MODE================#
    print("================ CFB MODE================")
    # Initialization vector generation
    initialization_vector = Random.get_random_bytes(DES3.block_size)

    # Encryption
    cipher = DES3.new(key, DES3.MODE_CFB, iv=initialization_vector, segment_size=8)
    ciphertext = cipher.encrypt(b'Hello World')
    print("Ciphertext: " + str(ciphertext))

    # Base64 Encoding
    iv_base64 = str(base64.b64encode(initialization_vector), encoding="utf-8")
    print("IV (encoded): " + iv_base64)

    # Base64 Decoding
    iv = base64.b64decode(iv_base64)
    print("IV (decoded): " + str(iv))

    # Decryption
    cipher = DES3.new(key, DES3.MODE_CFB, iv=iv, segment_size=8)
    plaintext = cipher.decrypt(ciphertext)
    print("Plaintext: " + str(plaintext) + "\n")