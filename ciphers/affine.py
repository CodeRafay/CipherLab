# ciphers/affine.py

def egcd(a, b):
    """Extended Euclidean Algorithm for finding modular inverse."""
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y


def modinv(a, m):
    """Compute modular inverse of a under modulo m."""
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


def encrypt(plaintext: str, parameters: dict):
    """
    Encrypts the given plaintext using the Affine Cipher technique.

    Formula: E(x) = (a * x + b) mod 26

    Parameters:
        plaintext (str): The text to encrypt (only letters and spaces expected).
        parameters (dict): Must contain keys 'a' and 'b' as integers.

    Returns:
        tuple: (ciphertext, steps)
    """
    a = parameters.get("a")
    b = parameters.get("b")
    plaintext = plaintext.lower()
    ciphertext = ""
    steps = []

    # Validate 'a' is coprime with 26
    gcd, _, _ = egcd(a, 26)
    if gcd != 1:
        raise ValueError(
            f"'a' must be coprime with 26. Got a={a} (gcd={gcd}).")

    for index, char in enumerate(plaintext):
        if char.isalpha():
            x = ord(char) - 97
            encrypted_val = (a * x + b) % 26
            encrypted_char = chr(encrypted_val + 97)
            ciphertext += encrypted_char

            steps.append(
                f"{index+1}. '{char}' -> ({a}*{x} + {b}) % 26 = {encrypted_val} -> '{encrypted_char}'"
            )
        else:
            ciphertext += char
            steps.append(f"{index+1}. Space remains unchanged")

    return ciphertext, steps


def decrypt(ciphertext: str, parameters: dict):
    """
    Decrypts the given ciphertext using the Affine Cipher technique.

    Formula: D(y) = a^-1 * (y - b) mod 26

    Parameters:
        ciphertext (str): The encrypted text to decrypt.
        parameters (dict): Must contain keys 'a' and 'b' as integers.

    Returns:
        tuple: (plaintext, steps)
    """
    a = parameters.get("a")
    b = parameters.get("b")
    ciphertext = ciphertext.lower()
    plaintext = ""
    steps = []

    a_inv = modinv(a, 26)
    if a_inv is None:
        raise ValueError(f"No modular inverse exists for a={a} under mod 26.")

    for index, char in enumerate(ciphertext):
        if char.isalpha():
            y = ord(char) - 97
            decrypted_val = (a_inv * (y - b)) % 26
            decrypted_char = chr(decrypted_val + 97)
            plaintext += decrypted_char

            steps.append(
                f"{index+1}. '{char}' -> a^-1= {a_inv}, ({a_inv} * ({y} - {b})) % 26 = {decrypted_val} -> '{decrypted_char}'"
            )
        else:
            plaintext += char
            steps.append(f"{index+1}. Space remains unchanged")

    return plaintext, steps


# Optional standalone test
if __name__ == "__main__":
    sample_text = "affine cipher"
    params = {"a": 17, "b": 20}

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
