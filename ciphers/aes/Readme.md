

# AES-128 Step-by-Step Educational Tool

This project is a C++ implementation of the **AES-128 (Rijndael)** encryption and decryption algorithm using **ECB (Electronic Codebook)**(Each 16-byte block is encrypted and decrypted independently) designed specifically as an educational tool.
 
Its primary purpose is to provide a highly verbose, step-by-step output of the entire cryptographic process, allowing users to see exactly how the data state changes during key expansion, encryption, and decryption.

**⚠️ Security Warning:** This implementation is for **educational and illustrative purposes ONLY**. It is **NOT cryptographically secure** and should **NEVER** be used to protect real-world sensitive data. It uses the insecure **ECB mode** and a simple **null-padding** scheme.

-----

## Features

  * **Full AES-128 Encryption & Decryption:** Implements the complete 10-round AES-128 algorithm.
  * **Verbose Step-by-Step Output:** 📜 This is the core feature. The console prints the 4x4 state matrix after *every single transformation* (e.g., `SubBytes`, `ShiftRows`, `MixColumns`, `AddRoundKey`) for all 10 rounds of encryption and decryption.
  * **Detailed Key Expansion:** Shows the generation of all 11 round keys (Round 0 to Round 10) from the initial 16-byte key.
  * **Interactive Input:** Prompts the user to enter their message and a 16-byte (128-bit) key.
  * **File I/O:** Encrypted ciphertext is written in raw binary to `message.aes`, which is then read by the decryption program.

-----

## Files in This Project

  * `encrypt.cpp`: Contains the `main()` function and logic for the encryption process. It takes a user's message, pads it, and runs it through the AES encryption algorithm, printing every step.
  * `decrypt.cpp`: Contains the `main()` function and logic for the decryption process. It reads the `message.aes` file and runs it through the inverse AES algorithm, printing every step.
  * `structures.h`: A header file containing all the core components of AES, including:
      * The S-box (`s`) and Inverse S-box (`inv_s`).
      * All look-up tables for `MixColumns` (`mul2`, `mul3`) and `InverseMixColumns` (`mul9`, `mul11`, `mul13`, `mul14`).
      * The Round Constant (`rcon`) array.
      * The `KeyExpansion()` function, which generates the round keys.
      * Helper functions (`printState`, `printRoundKey`) for the verbose output.

-----

## How to Compile

You can compile the two main programs using a C++ compiler like `g++`. It's recommended to compile them as separate executables.

```bash
# Compile the encryption program
g++ encrypt.cpp -o encrypt

# Compile the decryption program
g++ decrypt.cpp -o decrypt
```

This will create two executable files: `encrypt` and `decrypt`.

-----

## How to Use

Follow these steps to encrypt and then decrypt a message.

### 1\. Run Encryption

First, run the `encrypt` executable:

```bash
./encrypt
```

The program will ask you for two things:

1.  **Enter the message to encrypt:** Type any message and press Enter.
2.  **Enter the 16-byte key:** You must provide a 16-byte (128-bit) key as **space-separated hexadecimal values**.

**Example Key:** A common test key is all zeros:
`00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00`

Another example:
`2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c`

The program will then print the entire key expansion process, followed by the step-by-step encryption for each 16-byte block of your message. Finally, it will save the raw ciphertext to a file named `message.aes`.

### 2\. Run Decryption

Next, run the `decrypt` executable:

```bash
./decrypt
```

The program will automatically read the `message.aes` file. It will then ask you for one thing:

1.  **Enter the 16-byte key:** Enter the **exact same key** you used for encryption.

The program will then print the entire step-by-step decryption process (in reverse order, from Round 10 to Round 0) for each block. Finally, it will print the original plaintext message to the console.

-----

## Example Walkthrough

```bash
$ g++ encrypt.cpp -o encrypt
$ g++ decrypt.cpp -o decrypt

$ ./encrypt
=============================
 128-bit AES Encryption Tool
=============================
Enter the message to encrypt (max 1023 chars): This is a test
Padded message in hex:
0x54 0x68 0x69 0x73 0x20 0x69 0x73 0x20 0x61 0x20 0x74 0x65 0x73 0x74 0x00 0x00

Enter the 16-byte key as space-separated hex values (e.g., 01 04 02...): 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f
--- Key Expansion ---
Original Key (Round 0 Key):
0x00 0x01 0x02 0x03 0x04 0x05 0x06 0x07 0x08 0x09 0x0a 0x0b 0x0c 0x0d 0x0e 0x0f

Round 1 Key:
0x62 0x63 0x61 0x60 0x66 0x64 0x67 0x67 0x6e 0x6d 0x69 0x6c 0x62 0x60 0x67 0x63
...
(many steps omitted for brevity)
...
--- Encryption Process Finished ---

========================================
Final Encrypted message in hex:
0x69 0x98 0x0f 0x01 0x93 0x0f 0x09 0x6f 0xa2 0x4f 0x98 0xba 0x1f 0xeb 0x36 0x8a
========================================
Wrote encrypted message to file message.aes

$ ./decrypt
=============================
 128-bit AES Decryption Tool
=============================
Read 16 bytes from message.aes
Encrypted message in hex:
0x69 0x98 0x0f 0x01 0x93 0x0f 0x09 0x6f 0xa2 0x4f 0x98 0xba 0x1f 0xeb 0x36 0x8a

Enter the 16-byte key as space-separated hex values (e.g., 01 04 02...): 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f
--- Key Expansion ---
(Key expansion output is shown again)
...
========================================
 Decrypting Block 0
========================================
--- Decryption Process Started ---
Initial Ciphertext Block:
0x69 0x93 0xa2 0x1f
0x98 0x0f 0x4f 0xeb
0x0f 0x09 0x98 0x36
0x01 0x6f 0xba 0x8a
...
(many steps omitted for brevity)
...
--- Final Round (Round 0) ---
...
After SubRoundKey (Final Plaintext):
0x54 0x68 0x69 0x73
0x20 0x69 0x73 0x20
0x61 0x20 0x74 0x65
0x73 0x74 0x00 0x00

--- Decryption Process Finished ---

========================================
Final Decrypted message (ASCII):
This is a test
========================================
```

-----

## Technical Details & Limitations

  * **Algorithm:** AES-128.
  * **Mode of Operation:** **ECB (Electronic Codebook)**. Each 16-byte block is encrypted and decrypted independently. This mode is **insecure** because identical plaintext blocks will always result in identical ciphertext blocks, leaving patterns.
  * **Padding:** **Null Padding**. The input message is padded with `0x00` (null) bytes to become a multiple of 16. This is ambiguous if the original message is intended to end with null bytes.

-----

## Potential Future Improvements

This project is a great foundation. To make it a more robust and secure tool, consider adding the following features:

1.  **Implement Secure Modes of Operation:**
      * **CBC (Cipher-Block Chaining):** The classic, secure mode. Requires a random **Initialization Vector (IV)** to be generated and chained between blocks.
      * **CTR (Counter Mode):** A modern, fast, and parallelizable mode that turns the block cipher into a stream cipher.
2.  **Add PKCS\#7 Padding:** This is the standard, unambiguous padding scheme where *N* bytes of padding are added, each with the value *N*.
3.  **Refactor into a Class:** Move the AES logic into a C++ `AES` class to eliminate code duplication between `encrypt.cpp` and `decrypt.cpp` and create a cleaner, object-oriented design.
4.  **Improve Key Handling:**
      * **Key Derivation:** Implement a **KDF** (Key Derivation Function) like **PBKDF2** or use **SHA-256** to turn a user-friendly *password* into a 16-byte cryptographic key.
      * **Command-Line Arguments:** Change the program to accept file paths and keys as command-line arguments (`argv`) instead of interactive prompts, making it scriptable.