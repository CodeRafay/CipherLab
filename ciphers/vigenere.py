# ciphers/vigenere.py
from typing import Dict, Any, List

# -------------------------
# Utilities
# -------------------------


def generate_full_key(message: str, key: str) -> str:
    """Generate repeated key matching message length (ignoring non-letters)."""
    key = key.upper()
    message_letters = [c for c in message if c.isalpha()]
    if len(message_letters) == 0:
        return key
    repeated = (key * ((len(message_letters) // len(key)) + 1)
                )[:len(message_letters)]
    return repeated


def shift_char_encrypt(c: str, k: str) -> str:
    """Encrypt single character using Vigenere shift."""
    if c.isupper():
        return chr(((ord(c) - 65 + ord(k) - 65) % 26) + 65)
    elif c.islower():
        return chr(((ord(c) - 97 + ord(k.upper()) - 65) % 26) + 97)
    else:
        return c


def shift_char_decrypt(c: str, k: str) -> str:
    """Decrypt single character using Vigenere shift."""
    if c.isupper():
        return chr(((ord(c) - 65 - (ord(k) - 65) + 26) % 26) + 65)
    elif c.islower():
        return chr(((ord(c) - 97 - (ord(k.upper()) - 65) + 26) % 26) + 97)
    else:
        return c


# -------------------------
# Encryption / Decryption
# -------------------------
def encrypt(plaintext: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Encrypt using Vigenere Cipher.
    parameters: expects {'key': 'KEYSTRING'}
    Returns dict with ciphertext, key, and step-by-step transformations.
    """
    key = str(parameters.get("key", "")).upper()
    if not key:
        raise ValueError("Key is required for Vigenere encryption.")

    # Generate key matching message
    filtered_letters = [c for c in plaintext if c.isalpha()]
    full_key = generate_full_key(plaintext, key)
    steps: List[str] = []

    ciphertext = []
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            enc = shift_char_encrypt(char, full_key[key_index])
            steps.append(f"{char} + {full_key[key_index]} -> {enc}")
            ciphertext.append(enc)
            key_index += 1
        else:
            ciphertext.append(char)
            steps.append(f"{char} (non-alpha, unchanged)")

    return {
        "ciphertext": "".join(ciphertext),
        "key": key,
        "steps": steps
    }


def decrypt(ciphertext: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decrypt using Vigenere Cipher.
    parameters: expects {'key': 'KEYSTRING'}
    Returns dict with plaintext, key, and step-by-step transformations.
    """
    key = str(parameters.get("key", "")).upper()
    if not key:
        raise ValueError("Key is required for Vigenere decryption.")

    filtered_letters = [c for c in ciphertext if c.isalpha()]
    full_key = generate_full_key(ciphertext, key)
    steps: List[str] = []

    plaintext = []
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            dec = shift_char_decrypt(char, full_key[key_index])
            steps.append(f"{char} - {full_key[key_index]} -> {dec}")
            plaintext.append(dec)
            key_index += 1
        else:
            plaintext.append(char)
            steps.append(f"{char} (non-alpha, unchanged)")

    return {
        "plaintext": "".join(plaintext),
        "key": key,
        "steps": steps
    }


# -------------------------
# Standalone test (run as script)
# -------------------------
if __name__ == "__main__":
    print("=== Vigenere Cipher ===")
    message = input("Enter plaintext: ")
    key = input("Enter key: ")

    params = {"key": key}
    enc = encrypt(message, params)
    print("\n--- Encryption ---")
    print("Ciphertext:", enc["ciphertext"])
    print("Steps:")
    for s in enc["steps"]:
        print(" ", s)

    dec = decrypt(enc["ciphertext"], params)
    print("\n--- Decryption ---")
    print("Plaintext:", dec["plaintext"])
    print("Steps:")
    for s in dec["steps"]:
        print(" ", s)
