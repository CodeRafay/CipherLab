## The Data Encryption Standard (DES)

### Historical and Cryptographic Context

The **Data Encryption Standard (DES)**, adopted in **1977** by the **U.S. National Bureau of Standards (NBS)** (now known as **NIST**), represents one of the most influential developments in modern cryptography. Based on IBM’s **Lucifer cipher** (developed by Horst Feistel in the early 1970s), DES was selected as the first federal standard for encrypting unclassified information. Its adoption marked the beginning of a new era, transitioning from classical manual ciphers to automated, computer-based encryption systems.

DES was designed for efficiency in both hardware and software, balancing mathematical rigor with practical implementation constraints of that era. Despite later controversy over its **56-bit key length** (perceived as too short), the algorithm’s internal structure—particularly its **S-boxes** and **Feistel network**—has proven remarkably robust. The design principles of DES became foundational for subsequent ciphers such as **Triple DES (3DES)**, **AES**, and even modern symmetric-key cryptography as a whole.

---

Complete overview of encryption:
![DES Encryption Procedure](https://media.geeksforgeeks.org/wp-content/uploads/20250416155622491215/DES-Encryption-Algorithm.webp)
Inside each round , the following happens:
![DES Encryption Procedure](https://media.geeksforgeeks.org/wp-content/uploads/20250418102739119979/Rounds-in-DES.webp)

---

# Mechanism of Operation

## High level overview of procedure

DES is a **symmetric block cipher** that:

- Operates on **64-bit blocks** of plaintext.
- Uses a **56-bit key** (the 64-bit input key has 8 parity bits, one per byte, which are discarded).
- Performs **16 rounds** of complex transformations using a **Feistel structure**.

Each round mixes the data with a **unique subkey** derived from the main key through a **key schedule**. The Feistel design ensures that the same structure can be used for both encryption and decryption, with only the subkey order reversed.

The core of DES lies in the **Feistel structure**, which divides the data block into two halves and repeatedly applies substitution and permutation operations across **16 rounds**.

#### Step 1: Initial Permutation (IP)

The 64-bit plaintext undergoes an initial permutation, which rearranges the bits according to a fixed table. This step increases diffusion, ensuring that bit positions are well mixed before the actual encryption rounds begin.

#### Step 2: 16 Feistel Rounds

Each of the 16 rounds applies the **Feistel function (F)** using a unique 48-bit subkey derived from the main 56-bit key.
The block is divided into:

- **Left half (L)**
- **Right half (R)**

For each round _i_:
[
L_i = R_{i-1}
]
[
R_i = L_{i-1} \oplus F(R_{i-1}, K_i)
]

Here:

- ( F ) is a complex function involving **expansion, substitution, and permutation**.
- ( K_i ) is the round subkey.

![key generation](https://media.geeksforgeeks.org/wp-content/uploads/20250418102511508506/DES-Key-Transformation.webp)

#### Inside the Feistel Function (F)

1. **Expansion (E-box):**
   The 32-bit right half is expanded to 48 bits using an _expansion permutation table_, duplicating some bits.

2. **Key Mixing:**
   The expanded data is XORed with the 48-bit round key ( K_i ).

3. **Substitution (S-boxes):**
   The 48-bit result is divided into eight 6-bit blocks. Each block passes through a unique **S-box**, which compresses it to 4 bits according to a substitution table. These S-boxes introduce **non-linearity**, making DES resistant to linear attacks.

4. **Permutation (P-box):**
   The 32-bit output of all S-boxes is permuted again, further mixing the bits.

#### Step 3: Final Permutation (FP)

After completing all 16 rounds, the two halves are recombined (with the last swap undone) and passed through a **final permutation**, which is the inverse of the initial one. The result is the **64-bit ciphertext**.

---

## Step-by-Step Operation of DES

### 1. Input Preparation

DES takes:

- A **64-bit plaintext block**
- A **64-bit key** (only 56 bits used for encryption)

Example:

```
Plaintext: 0123456789ABCDEF (in hexadecimal)
Key:       133457799BBCDFF1
```

Both are converted to binary before processing.

---

### 2. Initial Permutation (IP)

Before the rounds begin, DES applies a **fixed initial permutation** to the plaintext. This rearranges the 64 bits according to a predefined table (known as the IP Table).

Although the IP itself doesn’t add cryptographic strength, it prepares the data for the Feistel rounds by shuffling the bit positions to improve **diffusion**.

For instance, the first few bits are rearranged as follows:

| Original Bit Position | New Bit Position |
| --------------------: | ---------------: |
|                    58 |                1 |
|                    50 |                2 |
|                    42 |                3 |
|                    34 |                4 |
|                   ... |              ... |

After applying IP, the 64-bit block is split into two halves:

- **Left Half (L₀):** first 32 bits
- **Right Half (R₀):** last 32 bits

---

### 3. Key Generation (Key Scheduling)

The 64-bit key undergoes two permutations and several **left circular shifts** to generate **16 subkeys**, each 48 bits long.

#### Step 3.1: Permuted Choice 1 (PC-1)

Removes the parity bits and permutes the remaining 56 bits.

#### Step 3.2: Left Shifts

The 56 bits are divided into two halves (C and D), each shifted left by 1 or 2 positions per round according to a shift schedule.

#### Step 3.3: Permuted Choice 2 (PC-2)

From the shifted halves, 48 bits are selected to form the **round key Kᵢ**.

Each round thus uses a distinct key derived from the master key:

```
K₁, K₂, …, K₁₆
```

---

### 4. The 16 Feistel Rounds

Each of the 16 rounds performs the following transformations:

[
L_i = R_{i-1}
]
[
R_i = L_{i-1} \oplus F(R_{i-1}, K_i)
]

where **F** is the **Feistel function** that introduces non-linearity and confusion.

Let’s explore **F(R, K)** in detail.

---

### 5. The Feistel Function (F)

The Feistel function is the core of DES, combining **expansion, key mixing, substitution**, and **permutation**.

#### Step 5.1: Expansion (E-box)

The 32-bit right half ( R\_{i-1} ) is expanded to 48 bits using an **Expansion Table (E)**. This duplicates certain bits to increase redundancy and prepare the data for XOR with the 48-bit key.

Example (first few positions):

```
R = 32 bits → E(R) = 48 bits
```

#### Step 5.2: Key Mixing

The expanded 48-bit data is XORed with the 48-bit subkey for that round:
[
B = E(R_{i-1}) \oplus K_i
]

#### Step 5.3: Substitution (S-boxes)

The result (48 bits) is split into eight 6-bit blocks:
[
B_1, B_2, …, B_8
]

Each block passes through a unique **Substitution Box (S-box)**. Each S-box maps a 6-bit input to a 4-bit output based on predefined substitution tables.

Each S-box lookup:

- Uses the **first and last bits** to select a **row**.
- Uses the **middle four bits** to select a **column**.

Example (for S₁):

```
Input: 011011
Row = (0,1) = binary 01 = 1
Column = 1101 = binary 13
Output = S₁[1][13] = 5 (binary 0101)
```

After all 8 S-boxes, the 32-bit result is formed.
![S boxes](https://media.geeksforgeeks.org/wp-content/uploads/20250417151222605042/SBox.webp)

#### Step 5.4: Permutation (P-box)

The combined 32-bit output from all S-boxes is then permuted using a **P-box**, rearranging the bits to spread the influence of each S-box across the next round.

---

### 6. Combining the Results

The output of F(R₍ᵢ₋₁₎, Kᵢ) is XORed with the left half (L₍ᵢ₋₁₎), and the halves are swapped.

After 16 rounds:

```
L₁₆ and R₁₆ are concatenated as R₁₆ || L₁₆ (note the final swap)
```

---

### 7. Final Permutation (FP)

The concatenated 64-bit block is permuted again using the **inverse of the Initial Permutation table**. The output is the **ciphertext**.

For the earlier example:

| Input                       | Output                       |
| --------------------------- | ---------------------------- |
| Plaintext: 0123456789ABCDEF | Ciphertext: 85E813540F0AB405 |

This ciphertext matches the official DES example from the Federal Information Processing Standard (FIPS) publication.

---

## Example Summary (Plaintext = 0123456789ABCDEF, Key = 133457799BBCDFF1)

| Step | Operation           | Output (Hexadecimal) |
| ---- | ------------------- | -------------------- |
| 1    | Initial Permutation | C0B7A8D05F3A829C     |
| 2    | After Round 1       | 85E813540F0AB405     |
| 3    | After 16 Rounds     | 85E813540F0AB405     |
| 4    | Final Permutation   | **85E813540F0AB405** |

---

## Decryption Process

Decryption in DES uses the **same algorithm** as encryption, but the **subkeys are applied in reverse order**:
[
K_{16}, K_{15}, …, K_1
]
Because of the Feistel structure’s symmetric nature, this design ensures the same hardware or software implementation can perform both operations efficiently.

---

## Security Analysis

### Strengths

1. **Feistel Structure:**
   Enables reversible encryption and decryption with the same logic.

2. **Confusion and Diffusion:**
   Achieved through substitution (S-boxes) and permutation operations, respectively.

3. **Well-studied Design:**
   DES’s structure influenced generations of cryptographic research and design, including AES and block cipher theory.

---

### Weaknesses

1. **Short Key Length (56 bits):**
   Brute-force attacks are practical today. The EFF’s “Deep Crack” machine (1998) broke DES in **less than three days**.

2. **Small Block Size (64 bits):**
   Vulnerable to block repetition in large data volumes (e.g., ECB mode).

3. **Vulnerability to Modern Cryptanalysis:**
   Techniques such as **differential** and **linear cryptanalysis** can exploit structural weaknesses if sufficient plaintext-ciphertext pairs are known.

---

## Successor: Triple DES (3DES)

To enhance security without redesigning the algorithm, **Triple DES (3DES)** was introduced:
[
C = E_{K_3}(D_{K_2}(E_{K_1}(P)))
]
This effectively uses a 168-bit key (three 56-bit keys) and significantly improves resistance to brute-force attacks.

---

### Security and Limitations

#### Strengths:

- **Complex internal structure** based on substitution and permutation principles.
- **Feistel design** ensures invertibility and flexibility.
- **Widespread adoption** made DES a benchmark for evaluating new ciphers.

#### Weaknesses:

- **Small key size (56 bits):**
  In the modern era of computing, a brute-force attack can test all ( 2^{56} ) keys in a matter of hours.
- **Block size limitation (64 bits):**
  Vulnerable to patterns when encrypting large datasets.
- **Susceptibility to differential and linear cryptanalysis**, developed in the 1990s.

## To address these, **Triple DES (3DES)** was introduced, applying DES encryption three times with different keys, effectively increasing the key length to 112 or 168 bits.

## Educational Significance

Studying DES offers critical insight into:

- The architecture of symmetric key ciphers.
- The Feistel model’s role in ensuring reversibility.
- How key scheduling and S-box design contribute to cryptographic strength.

Although obsolete for practical security, DES remains a **pedagogical cornerstone** for understanding the mathematical foundations of modern encryption algorithms.

---

## Summary Table

| Property        | Description                        |
| --------------- | ---------------------------------- |
| Cipher Type     | Symmetric Block Cipher             |
| Block Size      | 64 bits                            |
| Key Length      | 56 bits (64 bits including parity) |
| Structure       | 16-round Feistel network           |
| Key Scheduling  | Permutation + left circular shifts |
| Main Operations | Substitution, Permutation, XOR     |
| Security        | Inadequate by modern standards     |
| Successor       | 3DES, AES                          |

---
