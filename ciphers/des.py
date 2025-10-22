# ciphers/des.py

from typing import Dict, Any, List, Tuple

# --- DES Constants ---

initialPermutationMatrix = [
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
]
finalPermutationMatrix = [
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
]
expandMatrix = [
    32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
]
eachRoundPermutationMatrix = [
    16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25
]
keyPermutationMatrix1 = [
    57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35,
    27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38,
    30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
]
keyPermutationMatrix2 = [
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
]
SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
SboxesArray = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8], [
        4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10], [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5], [
        0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15], [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8], [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1], [
        13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7], [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15], [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9], [
        10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4], [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9], [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6], [
        4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14], [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8], [
        9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6], [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1], [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6], [
        1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2], [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7], [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2], [
        7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8], [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

# --- Helper Functions ---


def stringToBitArray(text: str) -> List[int]:
    # Using 'latin-1' encoding is crucial as it maps every byte value from 0-255 to a character.
    byte_array = text.encode('latin-1')
    return [int(bit) for byte in byte_array for bit in bin(byte)[2:].zfill(8)]


def bitArrayToString(array: List[int]) -> str:
    # Using 'latin-1' encoding is crucial as it maps every byte value from 0-255 to a character.
    byte_values = [int("".join(map(str, byte)), 2)
                   for byte in nSplit(array, 8)]
    return bytes(byte_values).decode('latin-1')


def binValue(val: Any, bitSize: int) -> str:
    bin_val = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    return bin_val.zfill(bitSize)


def bit_array_to_hex_string(arr: List[int]) -> str:
    return ''.join([f'{int("".join(map(str, nibble)), 2):X}' for nibble in nSplit(arr, 4)])


def nSplit(l: List[Any], n: int) -> List[List[Any]]:
    return [l[i:i + n] for i in range(0, len(l), n)]


def xor(l1: List[int], l2: List[int]) -> List[int]:
    return [a ^ b for a, b in zip(l1, l2)]


def permutation(array: List[int], table: List[int]) -> List[int]:
    return [array[element - 1] for element in table]


def leftShift(l1: List[int], l2: List[int], n: int) -> Tuple[List[int], List[int]]:
    return l1[n:] + l1[:n], l2[n:] + l2[:n]


def addPadding(text: str) -> str:
    padding_char_val = 8 - (len(text.encode('latin-1')) % 8)
    # If the text is a multiple of 8, a full block of padding is added
    if padding_char_val == 0:
        padding_char_val = 8
    return text + chr(padding_char_val) * padding_char_val


def removePadding(data: str) -> str:
    try:
        padding_char = data[-1]
        paddingLength = ord(padding_char)
        # Validate padding to avoid errors on malformed input
        if all(c == padding_char for c in data[-paddingLength:]):
            return data[:-paddingLength]
        return data  # Return as-is if padding seems incorrect
    except IndexError:
        return ""  # Handle empty string case


# --- Core DES Logic Functions ---

def SboxSubstitution(bitArray: List[int]) -> List[int]:
    blocks = nSplit(bitArray, 6)
    result = []
    for i, block in enumerate(blocks):
        row = int(str(block[0]) + str(block[5]), 2)
        column = int(''.join(map(str, block[1:5])), 2)
        sboxValue = SboxesArray[i][row][column]
        result.extend([int(bit) for bit in binValue(sboxValue, 4)])
    return result


def generateKeys(key: str) -> Tuple[List[List[int]], List[str]]:
    keys = []
    steps = ["--- Key Generation ---"]
    key_bits = stringToBitArray(key)

    key_perm = permutation(key_bits, keyPermutationMatrix1)
    steps.append(f"1. Initial 64-bit key permuted (PC-1) to 56 bits.")

    left, right = nSplit(key_perm, 28)

    for i in range(16):
        left, right = leftShift(left, right, SHIFT[i])
        steps.append(f"Round {i+1:>2}: Left shift by {SHIFT[i]}.")

        round_key = permutation(left + right, keyPermutationMatrix2)
        keys.append(round_key)
        steps.append(
            f"  -> Round Key {i+1:>2} (PC-2): {bit_array_to_hex_string(round_key)}")

    return keys, steps


def format_matrix_for_steps(name: str, matrix: list) -> str:
    """Formats a DES matrix into a readable string for the steps output."""
    header = f"----- {name} -----\n"
    body = ""
    # Check for S-Boxes nesting
    if isinstance(matrix[0], list) and isinstance(matrix[0][0], list):
        body += "[\n"
        for i, sbox in enumerate(matrix):
            body += f"  S-Box {i+1}: [\n"
            for row in sbox:
                body += f"    {row},\n"
            body += "  ],\n"
        body += "]"
    else:  # Standard flat list
        body += "[\n"
        for i in range(0, len(matrix), 16):
            line = ", ".join(map(str, matrix[i:i+16]))
            if i + 16 >= len(matrix):
                body += f"    {line}\n"
            else:
                body += f"    {line},\n"
        body += "]"
    return header + body


def _internal_des(text: str, key: str, is_encrypt: bool) -> Tuple[str, List[str]]:
    # Prepend matrices to the steps list for UI display
    steps = [
        "==================== DES CONSTANTS ====================",
        "NOTE: Intermediate values are shown in HEXADECIMAL format.",
        format_matrix_for_steps(
            "Initial Permutation (IP)", initialPermutationMatrix),
        format_matrix_for_steps(
            "Final Permutation (IP-1)", finalPermutationMatrix),
        format_matrix_for_steps("Expansion Matrix (E)", expandMatrix),
        format_matrix_for_steps(
            "Permutation Function (P)", eachRoundPermutationMatrix),
        format_matrix_for_steps(
            "Key Permutation 1 (PC-1)", keyPermutationMatrix1),
        format_matrix_for_steps(
            "Key Permutation 2 (PC-2)", keyPermutationMatrix2),
        format_matrix_for_steps("Key Shift Schedule", SHIFT),
        "=====================================================",
        ""  # Adding a blank line for spacing
    ]

    keys, key_steps = generateKeys(key)
    steps.extend(key_steps)

    # The text is already padded and encoded via 'latin-1' before this function
    text_blocks = nSplit(text, 8)
    result_bits = []

    for i, block_str in enumerate(text_blocks):
        steps.append(f"\n--- Processing Block {i+1} ---")
        block = stringToBitArray(block_str)

        block = permutation(block, initialPermutationMatrix)
        steps.append(
            f"1. Initial Permutation (IP): {bit_array_to_hex_string(block)}")

        left, right = nSplit(block, 32)

        for j in range(16):
            round_num = j + 1
            steps.append(f"\nRound {round_num:>2}:")
            steps.append(
                f"  L_in: {bit_array_to_hex_string(left)}, R_in: {bit_array_to_hex_string(right)}")

            expanded_right = permutation(right, expandMatrix)

            key_for_round = keys[j] if is_encrypt else keys[15 - j]
            steps.append(f"  Key : {bit_array_to_hex_string(key_for_round)}")

            temp = xor(key_for_round, expanded_right)
            temp = SboxSubstitution(temp)
            temp = permutation(temp, eachRoundPermutationMatrix)

            temp = xor(left, temp)
            left = right
            right = temp
            steps.append(
                f"  L_out:{bit_array_to_hex_string(left)}, R_out:{bit_array_to_hex_string(right)}")

        # Final swap of left and right is undone by concatenating right + left
        final_block = permutation(right + left, finalPermutationMatrix)
        steps.append(
            f"\nFinal Permutation (IP-1): {bit_array_to_hex_string(final_block)}")
        result_bits.extend(final_block)

    return bitArrayToString(result_bits), steps

# --- Standardized Functions for CipherLab ---


def encrypt(plaintext: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Encrypts plaintext using DES and returns ciphertext as a hex string."""
    key = parameters.get("key", "")
    if len(key) != 8:
        raise ValueError(
            "DES key must be exactly 8 characters (64 bits) long.")

    padded_text = addPadding(plaintext)
    # The result of _internal_des is a string that represents raw bytes.
    # This must be encoded back to bytes and then converted to hex for safe display.
    raw_ciphertext, steps = _internal_des(padded_text, key, is_encrypt=True)
    hex_ciphertext = raw_ciphertext.encode('latin-1').hex()

    return {"ciphertext": hex_ciphertext, "steps": steps}


def decrypt(ciphertext: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Decrypts a hex string ciphertext using DES."""
    key = parameters.get("key", "")
    if len(key) != 8:
        raise ValueError(
            "DES key must be exactly 8 characters (64 bits) long.")

    # **FIX**: Convert the incoming hex string back to a raw byte string ('latin-1')
    # that the internal DES function can process.
    try:
        # 1. Take hex string and convert to bytes object
        # 2. Decode bytes object into a 'latin-1' string
        raw_ciphertext = bytes.fromhex(ciphertext).decode('latin-1')
    except (ValueError, TypeError):
        raise ValueError(
            "Invalid ciphertext. It must be a valid hexadecimal string.")

    decrypted_padded, steps = _internal_des(
        raw_ciphertext, key, is_encrypt=False)
    plaintext = removePadding(decrypted_padded)

    return {"plaintext": plaintext, "steps": steps}


# --- Standalone Execution for Testing ---
if __name__ == "__main__":
    # Helper function to pretty-print matrices for the console
    def display_matrix(name: str, matrix: list):
        print(f"----- {name} -----")
        # Check if it's a deeply nested list like S-Boxes
        if isinstance(matrix[0], list) and isinstance(matrix[0][0], list):
            print("[")
            for i, sbox in enumerate(matrix):
                print(f"  S-Box {i+1}: [")
                for row in sbox:
                    print(f"    {row},")
                print("  ],")
            print("]")
        else:  # Standard flat list permutation tables
            print("[")
            # Format into rows of 16 elements for readability
            for i in range(0, len(matrix), 16):
                line = ", ".join(map(str, matrix[i:i+16]))
                # Remove trailing comma on the last line
                if i + 16 >= len(matrix):
                    print(f"    {line}")
                else:
                    print(f"    {line},")
            print("]")
        print()  # Add a newline for spacing

    # 1. Display important matrices
    print("="*60)
    print("                DES ALGORITHM CONSTANTS")
    print("="*60)
    display_matrix("Initial Permutation (IP)", initialPermutationMatrix)
    display_matrix("Final Permutation (IP-1)", finalPermutationMatrix)
    display_matrix("Expansion Matrix (E)", expandMatrix)
    display_matrix("Permutation Function (P)", eachRoundPermutationMatrix)
    display_matrix("Key Permutation 1 (PC-1)", keyPermutationMatrix1)
    display_matrix("Key Permutation 2 (PC-2)", keyPermutationMatrix2)
    display_matrix("Key Shift Schedule", SHIFT)
    display_matrix("Substitution Boxes (S-Boxes)", SboxesArray)

    # 2. Add an info box
    print("="*60)
    print("NOTE: Intermediate values (like keys and block states) in the")
    print("      process below are shown in HEXADECIMAL format.")
    print("="*60 + "\n")

    # 3. Define sample data
    sample_plaintext = "This is a secret message for DES."
    des_key = "s3cr3tk3y"  # Must be 8 characters
    params = {"key": des_key}

    print(f"Original Plaintext: '{sample_plaintext}'")
    print(f"Key: '{des_key}'\n")

    # 4. Encrypt the data
    print("--- ENCRYPTING ---")
    encryption_result = encrypt(sample_plaintext, params)
    hex_ciphertext = encryption_result["ciphertext"]
    enc_steps = encryption_result["steps"]

    print(f"Ciphertext (Hex): {hex_ciphertext}")
    # Uncomment the following lines to see the detailed steps
    print("\nEncryption Steps:")
    for step in enc_steps:
        print(step)

    print("\n" + "="*40 + "\n")

    # 5. Decrypt the data
    print("--- DECRYPTING ---")
    decryption_result = decrypt(hex_ciphertext, params)
    decrypted_plaintext = decryption_result["plaintext"]
    dec_steps = decryption_result["steps"]

    print(f"Decrypted Plaintext: '{decrypted_plaintext}'")
    # Uncomment the following lines to see the detailed steps
    print("\nDecryption Steps:")
    for step in dec_steps:
        print(step)

    # 6. Verify the result
    print("\n--- VERIFICATION ---")
    if sample_plaintext == decrypted_plaintext:
        print("SUCCESS: Decrypted text matches the original plaintext.")
    else:
        print("ERROR: Decrypted text does NOT match the original plaintext.")
