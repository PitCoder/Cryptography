# Cryptography
> This repository contains many contents of the cryptography course 2019-1 ESCOM IPN, as well some implementations of number theory, probabilistic and many other algorithms.

### Content

- Introduction to Crytopgraphy
- Classical Ciphers
- Block Ciphers
- Stream Ciphers

### Introduction to Cryptography
Cryptography is the science of secret writing with the goal of hiding the meaning of a message. Cryptography itself splits into three main branches:

- **Symmetric Algorithms:** are what many people assume cryptography is about two parties have an encryption and decryption method for which they share a secret key.
- **Asymetric (or Public Key) Algorithms:** user possesses a secret key as in symmetric cryptog-raphy but also a public key.
- **Cryptographic Protocols:** roughly speaking, crypto protocols deal with the application  of  cryptographic  algorithms.

In this repository only simetric algorithms have been implemented so far, in the future more algorithms will be added.

#### Symmetric Algorithms
Symmetric key ciphers are valuable because:

    - It is relatively inexpensive to produce a strong key for these ciphers.
    - The keys tend to be much smaller for the level of protection they afford.
    - The algorithms are relatively inexpensive to process.

Therefore, implementing symmetric cryptography (particularly with hardware) can be highly effective because you do not experience any significant time delay as a result of the encryption and decryption. Symmetric cryptography also provides a degree of authentication because data encrypted with one symmetric key cannot be decrypted with any other symmetric key. 

### License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2018 © <a href="https://github.com/PitCoder" target="_blank">Eric Alejandro López Ayala</a>.
