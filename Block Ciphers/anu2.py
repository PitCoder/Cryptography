'''
Encryption Flow
For i=0 to 24 do
    Apply S-Box at P_MSBi
    P_MSBi = S(P_MSBi)

    XOR key, S-Box output and right circularity shifted
    P_LSBi
    P_MSBi = P_MSBi xor RKi xor (P_LSBi >>> 3)

    XOR key, P_LSBi and left circularly shifted
    P_MSBi(Updated P_MSBi)
    P_LSBi = P_LSBi xor RKi2 xor (P_MSBi <<< 10)

    Swap P_MSBi and P_LSBi

    Update key

    Increment i by 1
'''
from bitstring import BitArray

# Definition of constants
BLOCK_SIZE = 4
KEY_SIZE = 128  # For ANU-II can be 80/128
KEY_HALF = int(KEY_SIZE/2)
KEY_QUARTER = int(KEY_HALF/2)

# Defintion of tables (S-Box for ANU II)
SUBSTITUTION_TABLE = ['1110', '0100', '1011', '0001',
                      '0111', '1001', '1100', '1010',
                      '1101', '0010', '0000', '1111',
                      '1000', '0101', '0011', '0110']


def sustitution_box(data_block):
    bit_block = str(data_block.bin)
    sustitution_block = []

    for i in range(0, len(bit_block), BLOCK_SIZE):
        sustitution_block.append(SUBSTITUTION_TABLE[int(bit_block[0 + i: BLOCK_SIZE + i], 2)])

    return BitArray('0b', ''.join(sustitution_block[:]))


def key_update(key, round):
    # Left circular shift by 13
    update = key << 13
    # S-Box of LSB 8-bits
    # KEY[K3,K2,K1,K0] = S[K3,K2,K1,K0]
    # KEY[K7,K6,K5,K4] = S[K7,K6,K5,K4]
    update[KEY_SIZE - 4:] = sustitution_box(update[KEY_SIZE - 4:])
    update[KEY_SIZE - 8:KEY_SIZE - 4] = sustitution_box(update[KEY_SIZE - 8:KEY_SIZE - 4])
    # 5 bit XOR with round counter
    # KEY[K63,K62,K61,K60,K59] = [K63,K62,K61,K60,K59] xor RC
    update[KEY_SIZE - 64:KEY_SIZE - 59] = update[KEY_SIZE - 64:KEY_SIZE - 59] ^ BitArray('0b' + '{:05b}'.format(round))

    return update


if __name__ == '__main__':
    # Define number of rounds
    NO_ROUNDS = 25

    #Test vector of ANU-II(128 bit key)
    #Plaintext      Key         Ciphertext
    #00000000 0000000000000000   5aac94c2
    #00000000 0000000000000000   b4dcb8c6
    #=====================================
    #00000000 ffffffffffffffff   0d5abbc9
    #00000000 ffffffffffffffff   d572802a
    #=====================================
    #ffffffff 0000000000000000   125d2f37
    #ffffffff 0000000000000000   b4dcb8c6


    plaintext = BitArray('0xffffffffffffffff')
    key = BitArray('0xffffffffffffffffffffffffffffffff')

    # Spliting the block data into halves
    p_msb = plaintext[:32]  # Most significant bits from the block p
    p_lsb = plaintext[32:]  # Less significant bits from the block p

    for i in range(0, 24):
        # Apply S-Box at p_msb
        p_msb = sustitution_box(p_msb)
        # XOR key, S-Box output and right circularity shifted
        p_msb = p_msb ^ key[KEY_HALF:KEY_HALF+KEY_QUARTER] ^ (p_lsb >> 3)
        # XOR key, P_LSBi and left circularity shifted
        p_lsb = p_lsb ^ key[KEY_HALF+KEY_QUARTER:] ^ (p_msb << 10)
        # Swap
        temp = p_msb;
        p_msb = p_lsb;
        p_lsb = temp;
        # Key update
        key = key_update(key, round)

    c_msb = p_msb
    c_lsb = p_lsb

    print("ciphertext: ", (c_msb + c_lsb).hex)
    print("ciphertext: ", (c_msb + c_lsb).hex)
    print("ciphertext: ", (c_msb+c_lsb).hex)
