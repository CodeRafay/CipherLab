# ciphers/OneTimePad.py
import random
import string
from typing import Dict, Any


def _generate_random_key(length: int) -> str:
    """Internal function to generate a random key of a given length."""
    if length <= 0:
        return ""
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))


def encrypt(plaintext: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Encrypts plaintext using One-Time Pad, supporting custom or generated keys.
    """
    plaintext_processed = "".join(filter(str.isalpha, plaintext.upper()))
    key = ""
    steps = []

    # Option 1: Generate a random key if requested by the UI
    if parameters.get("generate_key"):
        key = _generate_random_key(len(plaintext_processed))
        steps.append(
            f"Generated a random key of length {len(plaintext_processed)}.")
    # Option 2: Use a custom key provided by the user
    else:
        key = parameters.get("key", "").upper()
        if len(key) < len(plaintext_processed):
            raise ValueError(
                f"Custom key length ({len(key)}) must be at least as long as the plaintext length ({len(plaintext_processed)})."
            )

    cipher_text = ""
    for p, k in zip(plaintext_processed, key):
        c_val = (ord(p) - 65 + ord(k) - 65) % 26
        c = chr(c_val + 65)
        cipher_text += c
        steps.append(f"{p}({ord(p)-65}) + {k}({ord(k)-65}) = {c_val} → {c}")

    return {"ciphertext": cipher_text, "key": key, "steps": steps}


def decrypt(ciphertext: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decrypts ciphertext using One-Time Pad. A key is always required for decryption.
    """
    ciphertext_processed = "".join(filter(str.isalpha, ciphertext.upper()))
    key = parameters.get("key", "").upper()
    steps = []

    if not key:
        raise ValueError("A key is required for One-Time Pad decryption.")
    if len(key) < len(ciphertext_processed):
        raise ValueError(
            f"Key length ({len(key)}) must be at least as long as the ciphertext length ({len(ciphertext_processed)})."
        )

    plain_text = ""
    for c, k in zip(ciphertext_processed, key):
        p_val = (ord(c) - 65 - (ord(k) - 65)) % 26
        p = chr(p_val + 65)
        plain_text += p
        steps.append(f"{c}({ord(c)-65}) - {k}({ord(k)-65}) = {p_val} → {p}")

    return {"plaintext": plain_text, "key": key, "steps": steps}


# --- Standalone Test ---
if __name__ == "__main__":
    message = "THISISATEST"

    print("--- Test 1: Random Key Generation ---")
    enc_rand = encrypt(message, {"generate_key": True})
    print(f"Plaintext: {message}")
    print(f"Generated Key: {enc_rand['key']}")
    print(f"Ciphertext: {enc_rand['ciphertext']}")

    dec_rand = decrypt(enc_rand['ciphertext'], {"key": enc_rand['key']})
    print(f"Decrypted: {dec_rand['plaintext']}")
    assert dec_rand['plaintext'] == message
    print("Random Key Test Successful!")

    print("\n" + "="*30 + "\n")

    print("--- Test 2: Custom Key ---")
    custom_key = "XMCKL" * 3  # Make a long enough key
    enc_custom = encrypt(message, {"key": custom_key})
    print(f"Plaintext: {message}")
    print(f"Custom Key: {custom_key}")
    print(f"Ciphertext: {enc_custom['ciphertext']}")

    dec_custom = decrypt(enc_custom['ciphertext'], {"key": custom_key})
    print(f"Decrypted: {dec_custom['plaintext']}")
    assert dec_custom['plaintext'] == message
    print("Custom Key Test Successful!")
