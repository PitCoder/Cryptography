from collections import OrderedDict

old_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
new_alphabet = []

#Use collections
#Function used to remove duplicates from key
def removeDup(string):
    return ''.join(OrderedDict.fromkeys(string))

def encrypt(plaintext):
    ciphertext = ""
    for character in plaintext:
        index = old_alphabet.index(character)
        ciphertext = ciphertext + new_alphabet[index]
    return ciphertext

def decrypt(ciphertext):
    plaintext = ""
    for character in ciphertext:
        index = new_alphabet.index(character)
        plaintext = plaintext + old_alphabet[index]
    return plaintext


if __name__ == '__main__':
    print("============= MIXED ALPHABET CIPHER =============")
    plaintext = str(input("Insert the message to be encrypted: ")).replace(" ", "").lower()
    key = str(input("Please insert the key: ")).replace("\s", "")

    #Clean key as a list
    clean_key = list(removeDup(key))
    print("Clean key: ", clean_key)

    temp_alphabet = old_alphabet.copy()

    for character in clean_key:
        try:
            temp_alphabet.remove(character)
        except:
            print("The character ", character, " from the key is not valid")

    #Old alphabet before character removal
    print("Old alphabet: ", old_alphabet)

    #New alphabet formed (permutation)
    new_alphabet = clean_key.copy()
    for c in temp_alphabet:
        new_alphabet.append(c)
    print("New alphabet: ", new_alphabet)

    #Finally we encrypt/decrypt our message
    ciphertext = encrypt(plaintext)
    print("Message encrypted: ", ciphertext)
    print("Message decrypted: ", decrypt(ciphertext))