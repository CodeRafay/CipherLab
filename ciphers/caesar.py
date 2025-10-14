# ciphers/caesar.py

def encrypt(plaintext: str, parameters: dict):
    """
    Encrypts the given plaintext using the Caesar Cipher technique.

    Parameters:
        plaintext (str): The input text to encrypt (only letters and spaces expected).
        parameters (dict): Must contain key 'shift' -> int (number of positions to shift).

    Returns:
        tuple: (ciphertext, steps)
            ciphertext (str): The encrypted text.
            steps (list): Step-by-step explanation of encryption process.
    """
    shift = parameters.get("shift", 0)
    plaintext = plaintext.lower()
    ciphertext = ""
    steps = []

    for index, char in enumerate(plaintext):
        if char.isalpha():
            original_ord = ord(char) - 97
            shifted = (original_ord + shift) % 26
            encrypted_char = chr(shifted + 97)
            ciphertext += encrypted_char

            # Record step
            steps.append(
                f"{index+1}. '{char}' -> ({original_ord} + {shift}) % 26 = {shifted} -> '{encrypted_char}'"
            )
        else:
            # Keep spaces unchanged
            ciphertext += char
            steps.append(f"{index+1}. Space remains unchanged")

    return ciphertext, steps


def decrypt(ciphertext: str, parameters: dict):
    """
    Decrypts the given ciphertext using the Caesar Cipher technique.

    Parameters:
        ciphertext (str): The encrypted text to decrypt.
        parameters (dict): Must contain key 'shift' -> int (number of positions to shift back).

    Returns:
        tuple: (plaintext, steps)
            plaintext (str): The decrypted text.
            steps (list): Step-by-step explanation of decryption process.
    """
    shift = parameters.get("shift", 0)
    ciphertext = ciphertext.lower()
    plaintext = ""
    steps = []

    for index, char in enumerate(ciphertext):
        if char.isalpha():
            encrypted_ord = ord(char) - 97
            shifted = (encrypted_ord - shift) % 26
            decrypted_char = chr(shifted + 97)
            plaintext += decrypted_char

            steps.append(
                f"{index+1}. '{char}' -> ({encrypted_ord} - {shift}) % 26 = {shifted} -> '{decrypted_char}'"
            )
        else:
            plaintext += char
            steps.append(f"{index+1}. Space remains unchanged")

    return plaintext, steps


# Optional: quick test independent
if __name__ == "__main__":
    sample_text = "attack at once"
    params = {"shift": 4}

    cipher, enc_steps = encrypt(sample_text, params)
    print("Plaintext:", sample_text)
    print("Ciphertext:", cipher)
    print("\nEncryption Steps:")
    for s in enc_steps:
        print(s)

    plain, dec_steps = decrypt(cipher, params)
    print("\nDecrypted Back:", plain)
    print("\nDecryption Steps:")
    for s in dec_steps:
        print(s)
