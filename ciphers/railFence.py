# ciphers/railFence.py
"""
Rail Fence Cipher - encryption, decryption, and visualization utilities.

Functions:
- build_rail_matrix(text, rails, preserve_spaces=False)
    returns a 2D list (rails x columns) with characters placed in zig-zag order.
    if preserve_spaces=False, spaces are removed before placement (common variant).
- visualize_rail_pattern(text, rails, preserve_spaces=False)
    returns a multiline string representation of the matrix for printing / Streamlit.
- encrypt(text, rails, preserve_spaces=False)
    returns ciphertext (string) and the rail matrix (for UI).
- decrypt(ciphertext, rails, preserve_spaces=False)
    returns plaintext (string) and a rail matrix used during decryption (for UI).

Notes:
- preserve_spaces=False is the common behaviour: plaintext has spaces removed prior to placement.
- preserve_spaces=True preserves spaces as positions in the zig-zag (useful for teaching).
"""

from typing import List, Tuple


def build_rail_matrix(text: str, rails: int, preserve_spaces: bool = False) -> List[List[str]]:
    """
    Build the zig-zag rail matrix.

    Parameters:
        text: input text (plaintext or ciphertext)
        rails: number of rails (rows)
        preserve_spaces: if False, spaces are removed before placement; if True, spaces are treated as characters

    Returns:
        matrix: List of lists shape (rails x columns). Empty cells are filled with ''.
    """
    if rails < 2:
        raise ValueError("rails must be >= 2")

    if preserve_spaces:
        seq = list(text)  # include spaces and punctuation in positions
    else:
        # remove spaces only; keep punctuation if you want (you can adjust)
        seq = [c for c in text if c != ' ']

    cols = len(seq)
    # initialize matrix with empty strings
    matrix = [['' for _ in range(cols)] for _ in range(rails)]

    row = 0
    dir_down = False  # direction flag
    for col, ch in enumerate(seq):
        matrix[row][col] = ch
        # flip direction when you hit top or bottom row
        if row == 0 or row == rails - 1:
            dir_down = not dir_down
        row = row + 1 if dir_down else row - 1

    return matrix


def visualize_rail_pattern(text: str, rails: int, preserve_spaces: bool = False) -> str:
    """
    Return a multiline textual visualization of the rail matrix.
    This is good to show in console or Streamlit `st.text()`.

    Empty cells are shown as spaces for readability.
    """
    matrix = build_rail_matrix(text, rails, preserve_spaces)
    # format rows with single spaces between columns so alignment is stable
    formatted_rows = []
    for r in matrix:
        # replace empty strings with space to keep columns aligned
        formatted_rows.append(" ".join(ch if ch != "" else " " for ch in r))
    return "\n".join(formatted_rows)


def encrypt(plaintext: str, rails: int, preserve_spaces: bool = False) -> Tuple[str, List[List[str]]]:
    """
    Encrypt using Rail Fence Cipher.
    Returns tuple: (ciphertext (string), rail_matrix (list of lists) used to produce ciphertext)
    """
    matrix = build_rail_matrix(plaintext, rails, preserve_spaces)

    # read row-wise to produce ciphertext
    cipher_chars = []
    for r in range(rails):
        for c in range(len(matrix[0])):
            ch = matrix[r][c]
            if ch != '':
                cipher_chars.append(ch)

    ciphertext = "".join(cipher_chars)
    return ciphertext, matrix


def decrypt(ciphertext: str, rails: int, preserve_spaces: bool = False) -> Tuple[str, List[List[str]]]:
    """
    Decrypt a Rail Fence ciphertext.
    Returns tuple: (plaintext (string), rail_matrix (list of lists) used during decryption)
    """
    if rails < 2:
        raise ValueError("rails must be >= 2")

    # we need the same sequence length as used during encryption
    if preserve_spaces:
        # encryption used full length (including spaces), so ciphertext length must match that length
        # but ciphertext contains only the characters placed row-wise, so to reconstruct positions
        # we must attempt to build a placeholder sequence of the original length.
        # For decryption with preserve_spaces=True we need the original plaintext length.
        raise ValueError("When preserve_spaces=True, decrypt requires the original text length; "
                         "use decrypt_with_length(ciphertext, rails, original_length).")
    else:
        # when spaces removed, seq_len = length used during placement
        seq_len = len(ciphertext)

    # Phase 1: build an empty matrix and mark the zig-zag pattern with placeholders
    matrix = [['' for _ in range(seq_len)] for _ in range(rails)]
    row = 0
    dir_down = False
    for col in range(seq_len):
        matrix[row][col] = '*'  # marker
        if row == 0 or row == rails - 1:
            dir_down = not dir_down
        row = row + 1 if dir_down else row - 1

    # Phase 2: fill the markers with ciphertext letters row-wise
    idx = 0
    for r in range(rails):
        for c in range(seq_len):
            if matrix[r][c] == '*' and idx < len(ciphertext):
                matrix[r][c] = ciphertext[idx]
                idx += 1

    # Phase 3: read the matrix in zig-zag (col order) to reconstruct plaintext (without spaces)
    result_chars = []
    row = 0
    dir_down = False
    for col in range(seq_len):
        ch = matrix[row][col]
        result_chars.append(ch)
        if row == 0 or row == rails - 1:
            dir_down = not dir_down
        row = row + 1 if dir_down else row - 1

    plaintext = "".join(result_chars)
    return plaintext, matrix


# Optional helper for Streamlit or console when preserve_spaces=True decryption is required:
def decrypt_with_length(ciphertext: str, rails: int, original_length: int) -> Tuple[str, List[List[str]]]:
    """
    Decrypts when preserve_spaces=True was used during encryption.
    You must supply the original plaintext length (including spaces).
    This reconstructs positions and returns plaintext including preserved spaces.
    """
    if original_length < 0:
        raise ValueError("original_length must be positive")

    # build placeholders for sequence of original_length
    seq_len = original_length
    matrix = [['' for _ in range(seq_len)] for _ in range(rails)]

    # mark zig-zag pattern
    row = 0
    dir_down = False
    for col in range(seq_len):
        matrix[row][col] = '*'
        if row == 0 or row == rails - 1:
            dir_down = not dir_down
        row = row + 1 if dir_down else row - 1

    # fill markers with ciphertext characters row-wise
    idx = 0
    for r in range(rails):
        for c in range(seq_len):
            if matrix[r][c] == '*' and idx < len(ciphertext):
                matrix[r][c] = ciphertext[idx]
                idx += 1

    # read zig-zag to reconstruct the original sequence positions (including spaces placeholders)
    result_chars = []
    row = 0
    dir_down = False
    for col in range(seq_len):
        ch = matrix[row][col]
        if ch == '':
            # this position was not filled (shouldn't happen), put space
            result_chars.append(' ')
        else:
            result_chars.append(ch)
        if row == 0 or row == rails - 1:
            dir_down = not dir_down
        row = row + 1 if dir_down else row - 1

    plaintext = "".join(result_chars)
    return plaintext, matrix


# -------------------------
# Standalone test / demonstration
# -------------------------
if __name__ == "__main__":
    sample = "Meet me after the party"
    rails = 3

    print("=== SAMPLE:", sample, "| rails =", rails, "===\n")

    # Mode 1: preserve_spaces=True (treat spaces as characters)
    print("Mode: preserve_spaces = True (spaces kept as positions)\n")
    viz_pres = visualize_rail_pattern(sample, rails, preserve_spaces=True)
    print("Rail Pattern (plaintext):")
    print(viz_pres)
    enc_pres, mat_pres = encrypt(sample, rails, preserve_spaces=True)
    print("\nEncrypted (preserve spaces):", enc_pres)
    # decrypt_with_length required to recover when spaces were preserved
    dec_pres, _ = decrypt_with_length(
        enc_pres, rails, original_length=len(sample))
    print("Decrypted (preserve spaces):", dec_pres)

    print("\n" + "="*60 + "\n")

    # Mode 2: preserve_spaces=False (remove spaces before placement) - common variant
    print("Mode: preserve_spaces = False (spaces removed before placement)\n")
    viz_nosp = visualize_rail_pattern(sample, rails, preserve_spaces=False)
    print("Rail Pattern (plaintext-without-spaces):")
    print(viz_nosp)
    enc_nosp, mat_nosp = encrypt(sample, rails, preserve_spaces=False)
    print("\nEncrypted (no spaces):", enc_nosp)
    dec_nosp, _ = decrypt(enc_nosp, rails, preserve_spaces=False)
    # decrypted text will be without spaces
    print("Decrypted (no spaces):", dec_nosp)
