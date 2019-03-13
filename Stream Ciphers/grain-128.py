from bitstring import BitArray, BitStream

# Definition of constants
KEY_SIZE = 128
REGISTER_SIZE = 128
LAST_INDEX = 127
INITIALIZATION_CLOCKS = 256


def cipher_clocking(register_b, register_s, counter):
    fx = register_s[counter % REGISTER_SIZE] \
         ^ register_s[(LAST_INDEX - (counter + 7)) % REGISTER_SIZE] \
         ^ register_s[(LAST_INDEX - (counter + 38)) % REGISTER_SIZE] \
         ^ register_s[(LAST_INDEX - (counter + 70)) % REGISTER_SIZE] \
         ^ register_s[(LAST_INDEX - (counter + 81)) % REGISTER_SIZE] \
         ^ register_s[(LAST_INDEX - (counter + 93)) % REGISTER_SIZE]

    gx = register_s[(LAST_INDEX - counter) % REGISTER_SIZE] ^ register_b[(LAST_INDEX - counter) % REGISTER_SIZE] \
         ^ register_b[(LAST_INDEX - (counter + 26)) % REGISTER_SIZE] \
         ^ register_b[(LAST_INDEX - (counter + 56)) % REGISTER_SIZE] \
         ^ register_b[(LAST_INDEX - (counter + 91)) % REGISTER_SIZE] \
         ^ register_b[(LAST_INDEX - (counter + 96)) % REGISTER_SIZE] \
         ^ register_b[(LAST_INDEX - (counter + 3)) % REGISTER_SIZE] and register_b[
             (LAST_INDEX - (counter + 67)) % REGISTER_SIZE] \
         ^ register_b[(LAST_INDEX - (counter + 11)) % REGISTER_SIZE] and register_b[
             (LAST_INDEX - (counter + 13)) % REGISTER_SIZE] \
         ^ register_b[(LAST_INDEX - (counter + 17)) % REGISTER_SIZE] and register_b[
             (LAST_INDEX - (counter + 18)) % REGISTER_SIZE] \
         ^ register_b[(LAST_INDEX - (counter + 27)) % REGISTER_SIZE] and register_b[
             (LAST_INDEX - (counter + 59)) % REGISTER_SIZE] \
         ^ register_b[(LAST_INDEX - (counter + 40)) % REGISTER_SIZE] and register_b[
             (LAST_INDEX - (counter + 48)) % REGISTER_SIZE] \
         ^ register_b[(LAST_INDEX - (counter + 61)) % REGISTER_SIZE] and register_b[
             (LAST_INDEX - (counter + 65)) % REGISTER_SIZE] \
         ^ register_b[(LAST_INDEX - (counter + 68)) % REGISTER_SIZE] and register_b[
             (LAST_INDEX - (counter + 64)) % REGISTER_SIZE]

    hx = register_b[(LAST_INDEX - (counter + 12)) % REGISTER_SIZE] and register_s[
        (LAST_INDEX - (counter + 8)) % REGISTER_SIZE] \
         ^ register_s[(LAST_INDEX - (counter + 13)) % REGISTER_SIZE] and register_s[
             (LAST_INDEX - (counter + 20)) % REGISTER_SIZE] \
         ^ register_b[(LAST_INDEX - (counter + 95)) % REGISTER_SIZE] and register_s[
             (LAST_INDEX - (counter + 42)) % REGISTER_SIZE] \
         ^ register_s[(LAST_INDEX - (counter + 60)) % REGISTER_SIZE] and register_s[
             (LAST_INDEX - (counter + 79)) % REGISTER_SIZE] \
         ^ register_s[(LAST_INDEX - (counter + 12)) % REGISTER_SIZE] and register_b[
             (LAST_INDEX - (counter + 95)) % REGISTER_SIZE] and register_s[
             (LAST_INDEX - (counter + 95)) % REGISTER_SIZE]

    A = [15,36,45,64,73,89]
    z = register_b[(LAST_INDEX - (counter + 2)) % REGISTER_SIZE]
    print(register_b)
    print(register_s)

    #for j in A:
        #z = z ^ register_b[(LAST_INDEX - (counter + A[j])) % REGISTER_SIZE]
    z = z ^ hx ^ register_s[(LAST_INDEX - (counter + 93)) % REGISTER_SIZE]

    return fx, gx, z

def initialization(nfsr, lfsr):
    for i  in range(0,INITIALIZATION_CLOCKS):
        fx_i, gx_i, zi = cipher_clocking(nfsr, lfsr, i)
        nfsr = nfsr << 1; nfsr[LAST_INDEX] = fx_i ^ zi;
        lfsr = lfsr << 1; lfsr[LAST_INDEX] = gx_i ^ zi;
    return  nfsr, lfsr

def cipher(nfsr, lfsr):
    hx_0, gx_0, z_0 = cipher_clocking(nfsr, lfsr, 0)
    output = z_0

    for i in range(1, KEY_SIZE):
        fx_i, gx_i, zi = cipher_clocking(nfsr, lfsr, i)
        nfsr = nfsr << 1; nfsr[LAST_INDEX] = fx_i;
        lfsr = lfsr << 1; lfsr[LAST_INDEX] = gx_i;
        output = output + zi
    print(output)
    return output


if __name__ == '__main__':
    # Define number of rounds
    NO_ROUNDS = 25
    ONES_PADDING = BitArray('0xFFFFFFFF')

    # Test vector of GRAIN(128 bit key)
    #           IV                          Key                             Keystream
    # 000000000000000000000000 00000000000000000000000000000000   0fd9deefeb6fad437bf43fce35849cfe   Big-Endian
    # 000000000000000000000000 00000000000000000000000000000000   db032aff3788498b57cb894fffb6bb96   Little-Endian
    # =====================================
    # 0123456789abcdef12345678 0123456789abcdef123456789abcdef0   f09b7bf7d7f6b5c2de2ffc73ac21397f   Big-Endian
    # 0123456789abcdef12345678 0123456789abcdef123456789abcdef0   afb5babfa8de896b4b9c6acaf7c4fbfd   Little-Endian
    # =====================================

    initialization_vector = BitArray('0x000000000000000000000000')
    key = BitArray('0x00000000000000000000000000000000')

    # Key and IV Initialization
    nfsr = key[:]
    lfsr = ONES_PADDING + initialization_vector[:]

    nfsr, lfsr = initialization(nfsr, lfsr)
    keystream = cipher(nfsr, lfsr)

    print("IV: ", initialization_vector.hex)
    print("key: ", key.hex)
    print("keystream: ", keystream.hex)
