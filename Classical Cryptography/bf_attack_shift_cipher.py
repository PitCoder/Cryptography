alphabet = ['a', 'b', 'c', 'd', 'e',  'f',  'g', 'h', 'i',  'j', 'k',  'l', 'm', 'n', 'o',  'p', 'q' ,  'r', 's',  't', 'u', 'v', 'w', 'x', 'y', 'z']

plaintext = str(input()).replace(" ", "")
decoded_plaintexts = []

for i in range (0, 26):
    shift = i + 1
    new_word = ""
    for j in range(len(plaintext)):
        index  = alphabet.index(plaintext[j])
        shifted_char = (index - shift) % 26
        new_word = new_word + alphabet[shifted_char]
    decoded_plaintexts.append(new_word)

for result in decoded_plaintexts:
    print(result)
