
# To Implement Later(Features + Fixes)

## 1\. Implement Modes of Operation (This is the biggest one)

Right now, we are using **ECB (Electronic Codebook) mode**. we encrypt each 16-byte block independently. This is insecure because identical plaintext blocks (like blocks of all-zero padding) will produce identical ciphertext blocks, leaving a visible pattern.

To fix this, we should implement a **mode of operation** that chains the blocks together.

  * **CBC (Cipher-Block Chaining):** This is the classic and most well-known mode.
      * **How it works:** Before encrypting a plaintext block, we XOR it with the *previous* ciphertext block.
      * **What we need:**
        1.  An **Initialization Vector (IV)**: A 16-byte random block of data.
        2.  For "Block 0", we XOR the plaintext with the **IV**.
        3.  For "Block 1", we XOR the plaintext with the **ciphertext of Block 0**.
        4.  ...and so on.
      * **To stand out:**
          * Randomly generate a 16-byte IV for every encryption.
          * Write the IV as the *first 16 bytes* of wer output `message.aes` file.
          * When decrypting, read the first 16 bytes as the IV, and the rest as the ciphertext.
  * **CTR (Counter Mode):** This mode is more modern and turns the block cipher into a stream cipher. It's fast and can be parallelized.
      * **How it works:** we don't encrypt the plaintext directly. Instead, we encrypt a **nonce + counter** (which is also an IV) and XOR the *result* with wer plaintext.
      * **What we need:**
        1.  A 16-byte **Nonce** (or IV). A good way to do this is 8 bytes of random data and an 8-byte counter that starts at 0.
        2.  For "Block 0", encrypt `(Nonce + 0)`. XOR the result with Plaintext Block 0.
        3.  For "Block 1", encrypt `(Nonce + 1)`. XOR the result with Plaintext Block 1.
        4.  ...and so on.
      * Decryption is the *exact same process*. There's no separate "decrypt" algorithm.

-----

## 2\. Refactor into an `AES` Class (OOP)

Our `encrypt.cpp` and `decrypt.cpp` files duplicate a lot of code (like `SubBytes`, `ShiftRows`, etc.). A C++ class would be much cleaner.

**Example Structure:**

```cpp
// AES.h
#include "structures.h"

class AES {
private:
    unsigned char expandedKey[176];
    bool verbose;

    // All wer AES primitive functions
    void SubBytes(unsigned char * state);
    void ShiftRows(unsigned char * state);
    void MixColumns(unsigned char * state);
    // ...and their inverses...

    void AddRoundKey(unsigned char * state, unsigned char * roundKey);
    void printState(unsigned char * state);

public:
    // Constructor to set the key and run KeyExpansion
    AES(unsigned char key[16], bool enableVerbose = false);
    
    // Public encrypt/decrypt functions
    void encryptBlock(unsigned char * message, unsigned char * encryptedMessage);
    void decryptBlock(unsigned char * encryptedMessage, unsigned char * decryptedMessage);
};

// AES.cpp
#include "AES.h"

AES::AES(unsigned char key[16], bool enableVerbose) {
    this->verbose = enableVerbose;
    KeyExpansion(key, this->expandedKey); // Run key expansion once
}

void AES::encryptBlock(...) {
    // wer AESEncrypt logic goes here
    // Use this->verbose to control wer step-by-step couts
}

// ... etc. ...
```

This would make our `main()` functions in `encrypt.cpp` and `decrypt.cpp` much simpler. They would just handle I/O and then call something like `aes.encryptBlock(...)`.

-----

## 3\. Add Robust Padding (PKCS\#7)

we are currently padding with `0x00` (null bytes). This is fine, but it has a problem: what if wer *original message* ends with a `0x00`? The decryptor won't know if it's padding or real data.

A "stand out" solution is **PKCS\#7 padding**:

  * **How it works:** If we need to add *N* bytes of padding, we add *N* bytes, each with the value *N*.
  * **Example 1:** we need 5 bytes of padding. we add: `0x05 0x05 0x05 0x05 0x05`.
  * **Example 2:** we need 1 byte of padding. we add: `0x01`.
  * **Example 3 (The clever part):** wer message is *exactly* 16 bytes long (needs 0 padding). we add an *entire new block* of 16 bytes, each with the value `0x10`:
    `0x10 0x10 0x10 0x10 ... 0x10 0x10`.
  * **Why it's better:** When decrypting, we just look at the very last byte. If it's `0x05`, we know we need to strip off 5 bytes of padding. If it's `0x10`, we strip off 16. It's completely unambiguous.

-----

## 4\. Improve the Command-Line Interface (CLI)

Instead of interactive prompts, make it a professional command-line tool using `argc` and `argv`.

**Before:**

```
$ ./encrypt
Enter the message to encrypt: Hello
Enter the 16-byte key...: 01 04 ...
```

**After:**

```bash
# Encrypt file 'plaintext.txt' to 'out.enc' using CBC mode and a specific key
$ ./aes -e -m cbc -k "01 04 02..." -i "plaintext.txt" -o "out.enc"

# Decrypt
$ ./aes -d -m cbc -k "01 04 02..." -i "out.enc" -o "decrypted.txt"

# Add wer verbose logging back in
$ ./aes -e -v -m cbc ... 
```

This is a *massive* improvement in usability and makes our tool feel professional and scriptable.

-----

## 5\. Add Key Derivation (Advanced)

Real users don't enter 16-byte hex keys. They enter passwords. To stand out, we could derive the 16-byte key from a user's password.

  * **The Simple Way:** Use a standard hash function.
    1.  Ask the user for a password string (e.g., "P@ssword123").
    2.  Hash it using **SHA-256** (we would need to find a simple library or implement it).
    3.  A SHA-256 hash is 32 bytes. Just use the **first 16 bytes** of the hash as wer AES-128 key.
  * **The "Pro" Way:** Use a proper **Key Derivation Function (KDF)** like **PBKDF2**. This function is *designed* to turn low-entropy passwords into strong cryptographic keys by making them slow to compute (to resist brute-force attacks). This would also likely require a library (like OpenSSL), but mentioning it or implementing a simple version shows deep knowledge.
