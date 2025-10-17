# ciphers/playFair.py
from typing import Dict, Any


def generate_key_table(keyword: str):
    """
    Generates a 5x5 Playfair cipher key table from the given keyword.
    The letter 'j' is merged with 'i'.
    """
    keyword = keyword.lower().replace(" ", "").replace("j", "i")
    key_square = []
    seen = set()

    for ch in keyword:
        if ch not in seen and ch.isalpha():
            seen.add(ch)
            key_square.append(ch)

    alphabet = "abcdefghiklmnopqrstuvwxyz"  # 'j' is omitted
    for ch in alphabet:
        if ch not in seen:
            seen.add(ch)
            key_square.append(ch)

    matrix = [key_square[i:i + 5] for i in range(0, 25, 5)]
    return matrix


def format_plaintext(plaintext: str):
    """
    Prepares the plaintext for Playfair encryption:
    - Converts to lowercase, removes spaces.
    - Replaces 'j' with 'i'.
    - Splits into digraphs, inserting 'x' for duplicate pairs or padding.
    """
    plaintext = plaintext.lower().replace(" ", "").replace("j", "i")
    if not plaintext:
        return []

    formatted = []
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        b = ''
        if i + 1 < len(plaintext):
            if plaintext[i] == plaintext[i+1]:
                b = 'x'
                i -= 1  # Stay on the current character for the next pair
        else:
            b = 'x'

        if b == '':
            b = plaintext[i+1]

        formatted.append(a + b)
        i += 2

    return formatted


def find_position(matrix, char):
    """Find the (row, col) position of a character in the key table."""
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return None, None  # Return a tuple to avoid errors


def encrypt(plaintext: str, parameters: dict):
    """
    Encrypts plaintext using Playfair Cipher.
    """
    keyword = parameters.get("keyword", "")
    key_table = generate_key_table(keyword)
    digraphs = format_plaintext(plaintext)
    ciphertext = ""

    # --- ADDED: Format the key matrix for display ---
    matrix_str = "\n".join(["  ".join(row) for row in key_table])
    steps = [f"Generated 5x5 Key Matrix:\n{matrix_str}\n" + "-"*25]

    for idx, pair in enumerate(digraphs):
        a, b = pair[0], pair[1]
        row_a, col_a = find_position(key_table, a)
        row_b, col_b = find_position(key_table, b)

        # Handle case where a character is not in the matrix (e.g. 'j')
        if row_a is None or row_b is None:
            steps.append(f"Skipping invalid pair: '{pair}'")
            continue

        if row_a == row_b:
            enc_a = key_table[row_a][(col_a + 1) % 5]
            enc_b = key_table[row_b][(col_b + 1) % 5]
            rule = "Same row -> shift right"
        elif col_a == col_b:
            enc_a = key_table[(row_a + 1) % 5][col_a]
            enc_b = key_table[(row_b + 1) % 5][col_b]
            rule = "Same column -> shift down"
        else:
            enc_a = key_table[row_a][col_b]
            enc_b = key_table[row_b][col_a]
            rule = "Rectangle -> swap columns"

        ciphertext += enc_a + enc_b
        steps.append(f"{idx+1}. '{a}{b}' -> '{enc_a}{enc_b}' ({rule})")

    return {
        "ciphertext": ciphertext.upper(),
        "steps": steps,
        "key_matrix": key_table
    }


def decrypt(ciphertext: str, parameters: dict):
    """
    Decrypts ciphertext using Playfair Cipher.
    """
    keyword = parameters.get("keyword", "")
    key_table = generate_key_table(keyword)
    ciphertext = ciphertext.lower().replace(" ", "").replace("j", "i")
    digraphs = [ciphertext[i:i + 2] for i in range(0, len(ciphertext), 2)]
    plaintext = ""

    # --- ADDED: Format the key matrix for display ---
    matrix_str = "\n".join(["  ".join(row) for row in key_table])
    steps = [f"Using 5x5 Key Matrix:\n{matrix_str}\n" + "-"*25]

    for idx, pair in enumerate(digraphs):
        if len(pair) != 2:
            continue  # Skip incomplete pairs
        a, b = pair[0], pair[1]
        row_a, col_a = find_position(key_table, a)
        row_b, col_b = find_position(key_table, b)

        if row_a is None or row_b is None:
            steps.append(f"Skipping invalid pair: '{pair}'")
            continue

        if row_a == row_b:
            dec_a = key_table[row_a][(col_a - 1) % 5]
            dec_b = key_table[row_b][(col_b - 1) % 5]
            rule = "Same row -> shift left"
        elif col_a == col_b:
            dec_a = key_table[(row_a - 1) % 5][col_a]
            dec_b = key_table[(row_b - 1) % 5][col_b]
            rule = "Same column -> shift up"
        else:
            dec_a = key_table[row_a][col_b]
            dec_b = key_table[row_b][col_a]
            rule = "Rectangle -> swap columns"

        plaintext += dec_a + dec_b
        steps.append(f"{idx+1}. '{a}{b}' -> '{dec_a}{dec_b}' ({rule})")

    return {
        "plaintext": plaintext,
        "steps": steps,
        "key_matrix": key_table
    }


# Optional: standalone test
if __name__ == "__main__":
    sample_text = "instruments"
    params = {"keyword": "monarchy"}

    result = encrypt(sample_text, params)
    print("Plaintext:", sample_text)
    print("Ciphertext:", result["ciphertext"])

    print("\nEncryption Steps:")
    for s in result["steps"]:
        print(s)

    dec_result = decrypt(result["ciphertext"], params)
    print("\nDecrypted Back:", dec_result["plaintext"])
    print("\nDecryption Steps:")
    for s in dec_result["steps"]:
        print(s)
