# ciphers/columnTransposition.py
# Columnar Transposition Cipher is also known as the Row/Column Transposition Cipher.

import math
from typing import Dict, Any, List

# --- Core Logic Functions ---


def _internal_encrypt(plaintext: str, key: str) -> tuple[str, list[list[str]]]:
    """Internal encryption logic that also returns the grid for visualization."""
    plaintext = plaintext.replace(" ", "")
    num_cols = len(key)
    num_rows = math.ceil(len(plaintext) / num_cols)

    padded_plaintext = plaintext.ljust(num_rows * num_cols, '_')
    grid = [list(padded_plaintext[i:i + num_cols])
            for i in range(0, len(padded_plaintext), num_cols)]

    sorted_key_indices = sorted(range(len(key)), key=lambda k: key[k])

    ciphertext = ""
    for col_index in sorted_key_indices:
        for row in range(num_rows):
            ciphertext += grid[row][col_index]

    return ciphertext, grid


def _internal_decrypt(ciphertext: str, key: str) -> tuple[str, list[list[str]]]:
    """Internal decryption logic that also returns the reconstructed grid."""
    num_cols = len(key)
    num_rows = math.ceil(len(ciphertext) / num_cols)

    grid: List[List[str]] = [
        ['' for _ in range(num_cols)] for _ in range(num_rows)]

    sorted_key_indices = sorted(range(len(key)), key=lambda k: key[k])

    # Calculate how many columns are "full" vs "short"
    num_short_cols = (num_rows * num_cols) - len(ciphertext)

    cipher_idx = 0
    for col_index in sorted_key_indices:
        # Determine the number of rows for this specific column
        rows_in_this_col = num_rows
        # The columns that come *last* alphabetically get one fewer cell
        if col_index >= num_cols - num_short_cols:
            rows_in_this_col = num_rows - 1

        for row in range(rows_in_this_col):
            if cipher_idx < len(ciphertext):
                grid[row][col_index] = ciphertext[cipher_idx]
                cipher_idx += 1

    plaintext = "".join("".join(row) for row in grid).replace("_", "")
    return plaintext, grid


# --- Standardized Functions for Streamlit App ---
# These new functions wrap the core logic and produce the dictionary output needed by product.py.

def encrypt(plaintext: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Encrypts using Columnar Transposition and returns a detailed dictionary for the UI.
    """
    key = parameters.get("key", "KEY")
    if not key:
        raise ValueError("A key is required for Columnar Transposition.")

    ciphertext, grid = _internal_encrypt(plaintext, key)

    # Use the grid to create a detailed step-by-step visualization
    header = "  ".join(list(key))
    rows_viz = "\n".join(["  ".join(cell) for cell in grid])

    steps = [
        "1. The plaintext (with padding '_') is written into a grid under the key:",
        f"Key: {key}\n{header}\n{'-' * len(header)}\n{rows_viz}",
        "\n2. The columns are read out based on the alphabetical order of the key's letters."
    ]

    return {"ciphertext": ciphertext, "steps": steps}


def decrypt(ciphertext: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decrypts using Columnar Transposition and returns a detailed dictionary for the UI.
    """
    key = parameters.get("key", "KEY")
    if not key:
        raise ValueError("A key is required for Columnar Transposition.")

    plaintext, grid = _internal_decrypt(ciphertext, key)

    # Use the reconstructed grid for a detailed step-by-step visualization
    header = "  ".join(list(key))
    # Replace empty strings with a placeholder for better alignment in the UI
    rows_viz = "\n".join(
        ["  ".join(cell if cell else ' ' for cell in row) for row in grid])

    steps = [
        "1. A grid is created and filled column-by-column using the ciphertext, following the key's alphabetical order:",
        f"Key: {key}\n{header}\n{'-' * len(header)}\n{rows_viz}",
        "\n2. The plaintext is revealed by reading the grid row-by-row."
    ]

    return {"plaintext": plaintext, "steps": steps}


# --- Standalone Example Usage ---
# This block remains to allow for independent testing of the file.

if __name__ == "__main__":
    sample_plaintext = "attack postponed until two am"
    params = {"key": "SECURITY"}

    print("=== Columnar Transposition Cipher Test ===\n")

    # --- Test Encryption ---
    encryption_result = encrypt(sample_plaintext, params)
    print(f"Plaintext: '{sample_plaintext}'")
    print(f"Key: '{params['key']}'")
    print("\n--- Encryption Steps ---")
    print("\n".join(encryption_result["steps"]))
    print(f"\nFinal Ciphertext: {encryption_result['ciphertext']}")

    print("\n" + "="*50 + "\n")

    # --- Test Decryption ---
    sample_ciphertext = encryption_result['ciphertext']
    decryption_result = decrypt(sample_ciphertext, params)
    print(f"Ciphertext: '{sample_ciphertext}'")
    print(f"Key: '{params['key']}'")
    print("\n--- Decryption Steps ---")
    print("\n".join(decryption_result["steps"]))
    print(f"\nReconstructed Plaintext: {decryption_result['plaintext']}")
