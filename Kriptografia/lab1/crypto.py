#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: Boda Norbert
SUNet: <SUNet ID>

Replace this with a description of the program.
"""
import math

import utils


# Caesar Cipher
# Encrypt plaintext using a Caesar cipher
def encrypt_caesar(plaintext):
    cipher = ""
    if len(plaintext) == 0:
        return cipher
    for letter in plaintext:
        if ord(letter) < ord('A') or ord(letter) > ord('Z'):
            cipher = cipher + letter
            continue

        newLetterValue = (ord(letter) + 3)
        if newLetterValue > ord('Z'):
            newLetterValue = newLetterValue - (ord('Z') - ord('A') + 1)
        cipher = cipher + chr(newLetterValue)
    return cipher


# Decrypt a ciphertext using a Caesar cipher.
def decrypt_caesar(ciphertext):
    plaintext = ""
    if len(ciphertext) == 0:
        return plaintext
    for letter in ciphertext:
        letter = letter.upper()
        if ord(letter) < ord('A') or ord(letter) > ord('Z'):
            plaintext = plaintext + letter
            continue

        newLetterValue = (ord(letter) - 3)
        if newLetterValue < ord('A'):
            newLetterValue = newLetterValue + (ord('Z') - ord('A') + 1)
        plaintext = plaintext + chr(newLetterValue)
    return plaintext


# Vigenere Cipher
def clean_keyword(keyword):
    new_keyword = ""
    for letter in keyword:
        if ord(letter.upper()) >= ord('A') or ord(letter.upper()) <= ord('Z'):
            new_keyword = new_keyword + letter.upper()
    return new_keyword


# Encrypt plaintext using a Vigenere cipher with a keyword.
def encrypt_vigenere(plaintext, keyword):
    cipher = ""
    if len(plaintext) == 0:
        return cipher
    keyword = clean_keyword(keyword)
    number_of_non_letters = 0
    for i in range(len(plaintext)):
        letter = plaintext[i].upper()
        if ord(letter) < ord('A') or ord(letter) > ord('Z'):
            cipher = cipher + letter
            continue
        plaintextLetterValue = ord(letter) - ord('A')
        keywordLetterValue = ord(keyword[(i - number_of_non_letters) % len(keyword)]) - ord('A')
        newLetterValue = plaintextLetterValue + keywordLetterValue + ord('A')
        if newLetterValue > ord('Z'):
            newLetterValue = newLetterValue - (ord('Z') - ord('A') + 1)
        cipher = cipher + chr(newLetterValue)
    return cipher


# Decrypt ciphertext using a Vigenere cipher with a keyword.
def decrypt_vigenere(ciphertext, keyword):
    plaintext = ""
    if len(ciphertext) == 0:
        return plaintext
    keyword = clean_keyword(keyword)
    number_of_non_letters = 0
    for i in range(len(ciphertext)):
        letter = ciphertext[i].upper()
        if ord(letter) < ord('A') or ord(letter) > ord('Z'):
            plaintext = plaintext + str(letter)
            continue
        ciphertextLetterValue = ord(letter) - ord('A')
        keywordLetterValue = ord(keyword[(i - number_of_non_letters) % len(keyword)]) - ord('A')
        newLetterValue = ciphertextLetterValue - keywordLetterValue + ord('A')
        if newLetterValue < ord('A'):
            newLetterValue = newLetterValue + (ord('Z') - ord('A') + 1)
        plaintext = plaintext + chr(newLetterValue)
    return plaintext


# Encrypt plaintext using a Scytale cipher with a circumference.
def encrypt_scytale(plaintext, circumference, mode):
    if len(plaintext) == 0:
        return '' if mode == str else b''
    rows = [''] * circumference if mode == str else [b''] * circumference
    for i in range(len(plaintext)):
        rows[i % circumference] = mode(rows[i % circumference]) + mode(plaintext[i])
    return ''.join(rows) if mode == str else b''.join(rows)


# Decrypt ciphertext using a Scytale cipher with a circumference.
def decrypt_scytale(ciphertext, circumference, mode):
    if len(ciphertext) == 0:
        return '' if mode == str else b''
    characters_per_row = [0] * circumference
    row_index = 0
    # calculate how many characters per row
    for i in range(len(ciphertext)):
        characters_per_row[row_index] = characters_per_row[row_index] + 1
        row_index = row_index + 1
        if row_index >= circumference:
            row_index = 0

    rows = [''] * circumference if mode == str else [b''] * circumference
    character_index = 0
    # fill rows
    for i in range(circumference):
        while characters_per_row[i] > 0:
            rows[i] = mode(rows[i]) + mode(ciphertext[character_index])
            character_index = character_index + 1
            characters_per_row[i] = characters_per_row[i] - 1

    plaintext = '' if mode == str else b''
    current_row = 0
    row_indexes = [0] * circumference
    # read from rows in correct order: go downwards until you reached bottom, then go jump back to the top
    for i in range(len(ciphertext)):
        plaintext = mode(plaintext) + mode(rows[current_row][row_indexes[current_row]])
        row_indexes[current_row] = row_indexes[current_row] + 1
        current_row = current_row + 1
        if current_row >= circumference:
            current_row = 0
    return plaintext


# Encrypt plaintext using a Railfence cipher with number of rails.
def encrypt_railfence(plaintext, num_rails):
    if len(plaintext) == 0:
        return ''
    rows = [''] * num_rails
    current_row_index = 0
    increment = 1
    for i in range(len(plaintext)):
        rows[current_row_index] = rows[current_row_index] + str(plaintext[i])
        current_row_index = current_row_index + increment
        if current_row_index >= num_rails or current_row_index < 0:
            increment = -increment
            current_row_index = current_row_index + 2 * increment
    return ''.join(rows)


# Decrypt ciphertext using a Railfence cipher with number of rails.
def decrypt_railfence(ciphertext, num_rails):
    if len(ciphertext) == 0:
        return ''
    characters_per_row = [0] * num_rails
    row_index = 0
    increment = 1
    # calculate how many characters per row
    for i in range(len(ciphertext)):
        characters_per_row[row_index] = characters_per_row[row_index] + 1
        row_index = row_index + increment
        if row_index >= num_rails or row_index < 0:
            increment = -increment
            row_index = row_index + 2 * increment

    rows = [''] * num_rails
    character_index = 0
    # fill rows
    for i in range(num_rails):
        while characters_per_row[i] > 0:
            rows[i] = rows[i] + str(ciphertext[character_index])
            character_index = character_index + 1
            characters_per_row[i] = characters_per_row[i] - 1

    plaintext = ""
    current_row = 0
    row_indexes = [0] * num_rails
    increment = 1
    # read from rows in correct order: go downwards until you reached bottom, then go upwards
    for i in range(len(ciphertext)):
        plaintext = plaintext + str(rows[current_row][row_indexes[current_row]])
        row_indexes[current_row] = row_indexes[current_row] + 1
        current_row = current_row + increment
        if current_row >= num_rails or current_row < 0:
            increment = -increment
            current_row = current_row + 2 * increment
    return plaintext


# Merkle-Hellman Knapsack Crypto system
def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    raise NotImplementedError  # Your implementation here


def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    raise NotImplementedError  # Your implementation here


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    raise NotImplementedError  # Your implementation here


def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    raise NotImplementedError  # Your implementation here
