from bitstring import BitArray, BitStream

PERMUTATION_TABLE = [4, 0, 3, 1, 6, 2, 7, 5]
SUBSTITUTION_TABLE = ['1110', '0111', '1000', '0100',
                      '0001', '1001', '0010', '1111',
                      '0101', '1010', '1011', '0000',
                      '0110', '1100', '1101', '0011']
BLOCK_SIZE = 4
NUM_BLOCKS = 8
KEY_SIZE = 128
ROUNDS = 32

#======================  GRANULE F FUNCTION ======================
#============ IMPLEMENTATION OF THE PERMUTATION LAYER ============
def permutationLayer(pt_block):
    bit_block = str(pt_block.bin)
    perm_blocks = [0] * NUM_BLOCKS
    blocks = []

    for i in range(0, len(bit_block), BLOCK_SIZE):
        blocks.append(bit_block[0 + i: BLOCK_SIZE + i])

    for i in range(NUM_BLOCKS):
        perm_blocks[(NUM_BLOCKS - 1) - PERMUTATION_TABLE[i]] = blocks[(NUM_BLOCKS - 1) - i]

    permuted_block = BitArray('0b' + ''.join(perm_blocks[:]))

    return permuted_block

#============ IMPLEMENTATION OF THE SUBSTITUTION LAYER ============
def substitutionLayer(pt_block):
    bit_block = str(pt_block.bin)
    subt_blocks = []

    for i in range(0, len(bit_block), BLOCK_SIZE):
        subt_blocks.append(SUBSTITUTION_TABLE[int(bit_block[0 + i: BLOCK_SIZE + i], 2)])

    substituted_block = BitArray('0b' + ''.join(subt_blocks[:]))

    return substituted_block

#============ IMPLEMENTATION OF THE PR LAYER ============
def pr_layer(bitblock):
    temp0 = bitblock[:] #With this we made a full through copy
    temp1 = bitblock[:] #With this we made a full through copy

    temp0.rol(2)
    temp1.ror(7)

    return temp0 ^ temp1
#==================================================================

#=====================  ROUND KEY GENERATION ======================
def generateRoundKey(key, round):
    #Extraction of the key round
    round_key = key[KEY_SIZE-32:]
    #Update of the key
    key.rol(31)
    #Substitution of K[3,2,1,0]
    print(key[:])
    key[KEY_SIZE-4:] = substitutionLayer(key[KEY_SIZE-4:])
    #Substitution of K[7,6,5,4]
    key[KEY_SIZE - 8:KEY_SIZE - 4] = substitutionLayer(key[KEY_SIZE - 8:KEY_SIZE - 4])
    #Substitution of K[70,69,68,67,66]
    key[KEY_SIZE - 71:KEY_SIZE - 66] = key[KEY_SIZE - 71:KEY_SIZE - 66] ^ BitArray('0b'+'{:05b}'.format(round))

    return key, round_key

#===================  GRANULE FEISTEL STRUCTURE ===================
def granuleFeistel(pt0, pt1, key):
    upper_block = pt1[:]
    lower_block = pt0[:]
    up_key = key

    for i in range(ROUNDS):
        up_key, round_key = generateRoundKey(up_key, i)
        temp_block = permutationLayer(upper_block)
        temp_block = substitutionLayer(temp_block)
        temp_block = pr_layer(temp_block)
        temp_block = temp_block ^ lower_block ^ round_key

        lower_block = upper_block[:]
        upper_block = temp_block[:]
    
    return upper_block + lower_block

if __name__ == '__main__':
    #Creating a new bit stream
    #([0] + b).hex Example of padding
    #ffffffffffffffff
    pt = BitArray('0xffffffffffffffff')
    key = BitArray('0xffffffffffffffffffffffffffffffff')

    #Modify the bitstring
    pt1 = pt[:32] #Upper part of the stream MSB
    pt0 = pt[32:] #Lower part of the stream LSB

    '''
    print("Upper part: ", pt1.bin)
    print("Lower part: ", pt0.bin)
    print("Data: ", (pt1 + pt0).bin)

    #Doing the permutation
    perm_pt1 = permutationLayer(pt1)
    print("Permuted upper part: ", perm_pt1.hex)

    #Doing the substitution
    sub_pt1 = substitutionLayer(pt1)
    print("Substitued upper part: ", sub_pt1.hex)

    #Doing the pr
    pr_pt1 = pr_layer(pt1)
    print("Rotated upper part: ", pr_pt1.hex)

    #Doing the generation of the key for round 0
    key, round_key = generateRoundKey(key, 1)
    print("Generated round key: ", round_key.hex)
    print("Updated key: ", key.hex)
    '''

    ct = granuleFeistel(pt0, pt1, key)
    print("ciphertext: ", ct)