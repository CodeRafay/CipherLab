# ciphers/OneTimePad.py
import random
import string
from typing import Dict, Any


def generate_random_key(length: int) -> str:
    """Generate a random key of given length (uppercase A-Z)."""
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))


def string_encryption(plaintext: str, key: str) -> Dict[str, Any]:
    """Encrypt plaintext using One-Time Pad (Vernam Cipher)."""
    plaintext = plaintext.upper().replace(" ", "")
    key = key.upper()

    if len(key) < len(plaintext):
        raise ValueError(
            "Key must be at least as long as plaintext for One-Time Pad.")

    cipher_text = ""
    steps = []

    for p, k in zip(plaintext, key):
        if p.isalpha():
            c_val = (ord(p) - 65 + ord(k) - 65) % 26
            c = chr(c_val + 65)
            cipher_text += c
            steps.append(
                f"{p}({ord(p)-65}) + {k}({ord(k)-65}) = {c_val} → {c}")
        else:
            cipher_text += p

    return {"ciphertext": cipher_text, "key": key, "steps": steps}


def string_decryption(ciphertext: str, key: str) -> Dict[str, Any]:
    """Decrypt ciphertext using One-Time Pad (Vernam Cipher)."""
    ciphertext = ciphertext.upper().replace(" ", "")
    key = key.upper()

    if len(key) < len(ciphertext):
        raise ValueError(
            "Key must be at least as long as ciphertext for One-Time Pad.")

    plain_text = ""
    steps = []

    for c, k in zip(ciphertext, key):
        if c.isalpha():
            p_val = (ord(c) - 65 - (ord(k) - 65)) % 26
            p = chr(p_val + 65)
            plain_text += p
            steps.append(
                f"{c}({ord(c)-65}) - {k}({ord(k)-65}) = {p_val} → {p}")
        else:
            plain_text += c

    return {"plaintext": plain_text, "key": key, "steps": steps}


# ----------------------------
# Standalone Test (optional)
# ----------------------------
if __name__ == "__main__":
    message = input("Enter plaintext: ").strip().upper()
    choice = input("Do you want to generate a random key? (y/n): ").lower()

    if choice == "y":
        key = generate_random_key(len(message))
        print(f"Generated Key: {key}")
    else:
        key = input("Enter key (same length as message): ").strip().upper()

    enc = string_encryption(message, key)
    print("\nCiphertext:", enc["ciphertext"])
    print("Steps:")
    for step in enc["steps"]:
        print(" ", step)

    dec = string_decryption(enc["ciphertext"], key)
    print("\nDecrypted Text:", dec["plaintext"])
    print("Decryption Steps:")
    for step in dec["steps"]:
        print(" ", step)
