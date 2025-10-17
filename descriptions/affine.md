## The Affine Cipher

### Historical and Mathematical Context

The Affine cipher occupies an important position in the development of classical encryption techniques, representing a progression from the simpler Caesar cipher to a more mathematically structured method. Unlike ciphers attributed to historical figures, the Affine cipher is grounded in fundamental concepts of number theory and modular arithmetic.

Its encryption mechanism combines two mathematical operations—multiplication and addition—performed modulo 26, corresponding to the letters of the English alphabet. This combination enhances the basic substitution cipher, introducing complexity that anticipates principles found in modern cryptographic systems, including the use of modular inverses fundamental to public-key cryptography.

---

### Mechanism of Operation

The Affine cipher employs **two keys**:

- A multiplicative key, ( a ), which must be coprime with 26 (i.e., share no common divisors other than 1 with 26). This ensures the cipher is reversible.
- An additive key, ( b ), which serves as a fixed shift analogous to the Caesar cipher.

The encryption function for a plaintext letter represented by ( x ) (where ( A=0, B=1, \ldots, Z=25 )) is defined as:

[
E(x) = (a \times x + b) \mod 26
]

Decryption requires the modular inverse of ( a ), denoted ( a^{-1} ), satisfying ( a \times a^{-1} \equiv 1 \pmod{26} ). The plaintext letter ( x ) is recovered from ciphertext letter ( y ) by:

[
D(y) = a^{-1} \times (y - b) \mod 26
]

---

### Example

Consider encrypting the word **"AFFINE"** with keys ( a=5 ) and ( b=8 ):

- First, compute the modular inverse of ( a=5 ), which is ( 21 ), since:

[
5 \times 21 = 105 \equiv 1 \pmod{26}
]

- Apply the encryption formula to each letter:

| Letter | ( x ) | ( E(x) = (5x + 8) \mod 26 )          | Ciphertext Letter |
| ------ | ----- | ------------------------------------ | ----------------- |
| A      | 0     | (5 × 0 + 8) mod 26 = 8               | I                 |
| F      | 5     | (5 × 5 + 8) mod 26 = 33 mod 26 = 7   | H                 |
| F      | 5     | 7                                    | H                 |
| I      | 8     | (5 × 8 + 8) mod 26 = 48 mod 26 = 22  | W                 |
| N      | 13    | (5 × 13 + 8) mod 26 = 73 mod 26 = 21 | V                 |
| E      | 4     | (5 × 4 + 8) mod 26 = 28 mod 26 = 2   | C                 |

- The resulting ciphertext is **"IHHWVC"**.

---

### Decryption Example

To decrypt the ciphertext **"IHHWVC"** with the same keys ( a=5 ) and ( b=8 ):

- Use the modular inverse of ( a=5 ), which is ( 21 ).
- Apply the decryption formula for each ciphertext letter ( y ):

[
D(y) = 21 \times (y - 8) \mod 26
]

| Ciphertext Letter | ( y ) | ( D(y) = 21 \times (y - 8) \mod 26 )                                 | Plaintext Letter |
| ----------------- | ----- | -------------------------------------------------------------------- | ---------------- |
| I                 | 8     | 21 × (8 - 8) mod 26 = 0                                              | A                |
| H                 | 7     | 21 × (7 - 8) mod 26 = 21 × (-1 mod 26=25) = 21 × 25 = 525 mod 26 = 5 | F                |
| H                 | 7     | 5                                                                    | F                |
| W                 | 22    | 21 × (22 - 8) = 21 × 14 = 294 mod 26 = 8                             | I                |
| V                 | 21    | 21 × (21 - 8) = 21 × 13 = 273 mod 26 = 13                            | N                |
| C                 | 2     | 21 × (2 - 8) = 21 × (-6 mod 26=20) = 420 mod 26 = 4                  | E                |

- The decrypted plaintext is **"AFFINE"**.

---

### Security Analysis

Despite its educational value, the Affine cipher is inadequate for securing sensitive information in contemporary contexts due to the following reasons:

- **Susceptibility to Frequency Analysis**: Each plaintext letter maps to a single ciphertext letter, preserving frequency patterns exploitable by cryptanalysts.
- **Limited Key Space**: The possible number of key pairs ( (a,b) ) is restricted (312 valid pairs), making brute-force attacks feasible.

---

### Educational Significance

Studying the Affine cipher facilitates understanding of essential cryptographic concepts such as modular arithmetic, linear transformations, and the role of invertible keys. It serves as a foundational example bridging elementary substitution ciphers and more sophisticated encryption methods used in modern secure communications.
