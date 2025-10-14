# ciphers/columnTransposition.py
# Columnar Transposition Cipher is also know as the Row/Column Transposition Cipher.

import math


def encrypt_row_column_transposition(plaintext, key):
    """
    Encrypts the given plaintext using the Row/Column Transposition Cipher.

    Process:
        1. Write the plaintext row by row under the given key.
        2. Sort the key alphabetically and read the columns in that order.
        3. Join column characters to form ciphertext.

    Parameters:
        plaintext (str): The text to encrypt.
        key (str): The keyword for column order (e.g., "HACK").

    Returns:
        str: The encrypted ciphertext.
    """
    plaintext = plaintext.replace(" ", "")  # remove spaces for simplicity
    num_cols = len(key)
    num_rows = math.ceil(len(plaintext) / num_cols)

    # Fill the grid row-wise, pad with underscores if needed
    fill_null = (num_rows * num_cols) - len(plaintext)
    plaintext += "_" * fill_null

    matrix = [list(plaintext[i:i + num_cols])
              for i in range(0, len(plaintext), num_cols)]

    # Sort the key alphabetically, keeping original index positions
    sorted_key = sorted([(char, idx) for idx, char in enumerate(key)])

    # Read columns based on sorted key order
    ciphertext = ""
    for _, col_index in sorted_key:
        for row in matrix:
            ciphertext += row[col_index]

    return ciphertext


def decrypt_row_column_transposition(ciphertext, key):
    """
    Decrypts a ciphertext encrypted using Row/Column Transposition Cipher.

    Process:
        1. Compute grid size from ciphertext length and key.
        2. Fill columns based on the sorted key order.
        3. Read text row by row to reconstruct plaintext.

    Parameters:
        ciphertext (str): The encrypted text.
        key (str): The same key used for encryption.

    Returns:
        str: The decrypted plaintext.
    """
    num_cols = len(key)
    num_rows = math.ceil(len(ciphertext) / num_cols)

    # Determine column order based on sorted key
    sorted_key = sorted([(char, idx) for idx, char in enumerate(key)])

    # Create an empty grid
    matrix = [['' for _ in range(num_cols)] for _ in range(num_rows)]

    # Fill columns according to sorted key order
    index = 0
    for _, col_index in sorted_key:
        for row in range(num_rows):
            if index < len(ciphertext):
                matrix[row][col_index] = ciphertext[index]
                index += 1

    # Read matrix row by row
    plaintext = ''.join([''.join(row) for row in matrix])
    return plaintext.replace("_", "")


def visualize_row_column(plaintext, key):
    """
    Returns a string visualization of the row-column grid used during encryption.
    """
    plaintext = plaintext.replace(" ", "")
    num_cols = len(key)
    num_rows = math.ceil(len(plaintext) / num_cols)
    fill_null = (num_rows * num_cols) - len(plaintext)
    plaintext += "_" * fill_null

    matrix = [list(plaintext[i:i + num_cols])
              for i in range(0, len(plaintext), num_cols)]
    header = "   ".join(list(key))
    rows = "\n".join(["   ".join(row) for row in matrix])

    return f"Key: {key}\n\n{header}\n{rows}"


# Example Usage
if __name__ == "__main__":
    plaintext = "attackpostponeduntiltwoam"
    key = "EDBCFGH"

    print("=== Row/Column Transposition Cipher ===\n")
    print("Grid Visualization:")
    print(visualize_row_column(plaintext, key))

    encrypted = encrypt_row_column_transposition(plaintext, key)
    print(f"\nEncrypted Text: {encrypted}")

    decrypted = decrypt_row_column_transposition(encrypted, key)
    print(f"Decrypted Text: {decrypted}")
