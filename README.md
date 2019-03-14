# Cryptography
> This repository contains many contents of the cryptography course 2019-1 ESCOM IPN, as well some implementations of number theory, probabilistic and many other algorithms.

### Content

- Introduction to Crytopgraphy
- Classical Ciphers
- Block Ciphers
- Stream Ciphers

<p align="center">
  <img src="https://thumbs.gfycat.com/ViciousEnchantedHairstreak-size_restricted.gif" alt="Crytography"/>
</p>

### Introduction to Cryptography
Cryptography is the science of secret writing with the goal of hiding the meaning of a message. Cryptography itself splits into three main branches:

- **Symmetric Algorithms:** are what many people assume cryptography is about two parties have an encryption and decryption method for which they share a secret key.
- **Asymetric (or Public Key) Algorithms:** user possesses a secret key as in symmetric cryptog-raphy but also a public key.
- **Cryptographic Protocols:** roughly speaking, crypto protocols deal with the application  of  cryptographic  algorithms.

In this repository only symmetric algorithms have been implemented so far, in the future more algorithms will be added.

#### Symmetric Algorithms
Symmetric key ciphers are valuable because:

    - It is relatively inexpensive to produce a strong key for these ciphers.
    - The keys tend to be much smaller for the level of protection they afford.
    - The algorithms are relatively inexpensive to process.

Therefore, implementing symmetric cryptography (particularly with hardware) can be highly effective because you do not experience any significant time delay as a result of the encryption and decryption. Symmetric cryptography also provides a degree of authentication because data encrypted with one symmetric key cannot be decrypted with any other symmetric key.

### Classical Ciphers

Even though this repository is still under construction, the section about classical ciphers is almost complete. It covers an introduction to Monoalphabetic Sustitution Ciphers, Simple Transposition Ciphers, Polyalphabetic Sustitution Ciphers and Fractioning Ciphers.

The implemented algorithms are:

    - Caesar Shift Cipher
    - Affine Cipher
    - Mixed Alphabet Cipher
    - Permutation Cipher
    - Simple Columnar Transposition Cipher
    - Hill Cipher
    - Polybus Square Cipher
    
### Block Ciphers
Block ciphersencrypt an entire block of plaintext bits at a time with the samekey. This means that the encryption of any plaintext bit in a given block dependson every other plaintext bit in the same block. This section covers the implementation of the following algorithms:
    
    - Triple DES Cipher
    - ANU II Cipher
    - Baby AES (Advanced Encryption Standard)
    - Granule
   
   <p align="center">
      <img src="https://raw.githubusercontent.com/PitCoder/Cryptography/master/Img/aes.gif" alt="AES"/>
   </p>

### Stream Ciphers
Stream ciphers encrypt bits individually. This is achieved by adding a bit from a key  stream to  a  plaintext  bit.  There  are  synchronous  stream  ciphers  wherethe key stream depends only on the key, and asynchronous ones where the keystream also depends on the ciphertext. This section covers the implementation of the following algorithm:

    - Grain 128
    
   
   <p align="center">
      <img src="https://raw.githubusercontent.com/PitCoder/Cryptography/master/Img/cipher.gif" alt="Stream Cipher"/>
   </p>
    

### License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2019 © <a href="https://github.com/PitCoder" target="_blank">Eric Alejandro López Ayala</a>.
