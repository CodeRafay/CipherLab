# ciphers/hill.py
import numpy as np
from typing import List, Dict, Any

MOD = 26

# -------------------------
# Utilities
# -------------------------


def text_to_numbers(text: str) -> List[int]:
    """Convert letters to numbers A=0 .. Z=25, ignore non-alpha."""
    return [ord(c.upper()) - 65 for c in text if c.isalpha()]


def numbers_to_text(nums: List[int]) -> str:
    """Convert numbers back to letters (wrap modulo 26)."""
    return ''.join(chr((n % MOD) + 65) for n in nums)


def extended_gcd(a: int, b: int):
    """Extended Euclidean Algorithm: returns (g, x, y) such that a*x + b*y = g = gcd(a,b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def modinv_int(a: int, m: int) -> int:
    """Modular inverse of integer a under modulo m. Raises ValueError if no inverse."""
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"No modular inverse for {a} under mod {m}")
    return x % m


def matrix_minor(mat: np.ndarray, i: int, j: int) -> int:
    """Return determinant of minor matrix (int)."""
    sub = np.delete(np.delete(mat, i, axis=0), j, axis=1)
    det = int(round(np.linalg.det(sub)))
    return det


def matrix_adjugate(mat: np.ndarray) -> np.ndarray:
    """Compute adjugate (classical adjoint) of an integer matrix."""
    n = mat.shape[0]
    cofactors = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            minor_det = matrix_minor(mat, i, j)
            sign = (-1) ** (i + j)
            cofactors[i, j] = sign * minor_det
    adj = cofactors.T
    return adj


def matrix_mod_inv(mat: np.ndarray, mod: int = MOD) -> np.ndarray:
    """
    Compute modular inverse of integer matrix `mat` modulo `mod`.
    """
    if mat.shape[0] != mat.shape[1]:
        raise ValueError("Key matrix must be square.")
    n = mat.shape[0]
    det = int(round(np.linalg.det(mat)))
    det_mod = det % mod

    try:
        det_inv = modinv_int(det_mod, mod)
    except ValueError:
        raise ValueError(
            f"Determinant {det} (mod {mod} = {det_mod}) has no inverse; invalid key matrix for Hill cipher.")

    adj = matrix_adjugate(mat).astype(int)
    inv_mod = (det_inv * adj) % mod
    return inv_mod.astype(int)

# -------------------------
# Key parsing
# -------------------------


def parse_key_matrix_from_params(parameters: Dict[str, Any]) -> np.ndarray:
    """
    Parses the key from parameters, accepting either a text key or a pre-formatted matrix.
    """
    # This branch handles numeric matrix input from the UI
    if "key_matrix" in parameters and parameters["key_matrix"] is not None:
        try:
            mat = np.array(parameters["key_matrix"], dtype=int)
            if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
                raise ValueError(
                    "Provided key_matrix must be a square 2D array.")
            return mat
        except (ValueError, TypeError):
            raise ValueError(
                "Invalid format for key_matrix. It must be a list of lists of integers.")

    # This branch handles the text key input
    elif "key" in parameters and parameters["key"]:
        key = str(parameters["key"]).upper().replace(" ", "")

        if not key:
            raise ValueError("Hill cipher key string cannot be empty.")

        nums = text_to_numbers(key)
        if not nums:
            raise ValueError(
                "Hill cipher key must contain alphabetic characters.")

        size = int(len(nums) ** 0.5)
        if size * size != len(nums):
            raise ValueError(
                "Key string length must be a perfect square (4, 9, 16...).")
        mat = np.array(nums, dtype=int).reshape(size, size)
        return mat
    else:
        raise ValueError(
            "No key provided. Provide 'key' (string) or 'key_matrix' (list of lists) in parameters.")

# -------------------------
# Encryption / Decryption
# -------------------------


def encrypt(plaintext: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hill cipher encryption.
    """
    key_mat = parse_key_matrix_from_params(parameters)
    key_mat = key_mat % MOD
    n = key_mat.shape[0]

    # --- ADDED: Format the key matrix for display in the steps ---
    matrix_str_repr = "\n".join(["  ".join(map(str, row)) for row in key_mat])
    steps = [f"Using Key Matrix:\n{matrix_str_repr}\n" + "-"*15]

    if n == 0:
        return {"ciphertext": plaintext, "key_matrix": [], "steps": ["Error: Key matrix is empty. No encryption performed."]}

    filtered = "".join([c for c in plaintext if c.isalpha()]).upper()
    if len(filtered) == 0:
        return {"ciphertext": "", "key_matrix": key_mat.tolist(), "steps": steps}

    if len(filtered) % n != 0:
        pad_len = n - (len(filtered) % n)
        filtered += "X" * pad_len

    ciphertext = ""
    for i in range(0, len(filtered), n):
        block = filtered[i:i+n]
        vec = np.array(text_to_numbers(block), dtype=int).reshape(n, 1)
        enc_vec = (key_mat.dot(vec) % MOD).flatten().tolist()
        enc_block = numbers_to_text(enc_vec)
        ciphertext += enc_block
        steps.append(
            f"Block '{block}' -> {enc_block}  (vector {vec.flatten().tolist()} * key -> {enc_vec})")

    return {"ciphertext": ciphertext.lower(), "key_matrix": key_mat.tolist(), "steps": steps}


def decrypt(ciphertext: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hill cipher decryption.
    """
    key_mat = parse_key_matrix_from_params(parameters)
    key_mat = key_mat % MOD
    n = key_mat.shape[0]

    if n == 0:
        return {"plaintext": ciphertext, "key_matrix": [], "steps": ["Error: Key matrix is empty. No decryption performed."]}

    inv_key = matrix_mod_inv(key_mat, MOD)

    # --- ADDED: Format the inverse key matrix for display in the steps ---
    matrix_str_repr = "\n".join(["  ".join(map(str, row)) for row in inv_key])
    steps = [f"Using Inverse Key Matrix:\n{matrix_str_repr}\n" + "-"*20]

    filtered = "".join([c for c in ciphertext if c.isalpha()]).upper()
    if len(filtered) == 0:
        return {"plaintext": "", "key_matrix": key_mat.tolist(), "steps": steps}
    if len(filtered) % n != 0:
        raise ValueError(
            f"Ciphertext length must be multiple of key matrix size {n}.")

    plaintext = ""
    for i in range(0, len(filtered), n):
        block = filtered[i:i+n]
        vec = np.array(text_to_numbers(block), dtype=int).reshape(n, 1)
        dec_vec = (inv_key.dot(vec) % MOD).flatten().tolist()
        dec_block = numbers_to_text(dec_vec)
        plaintext += dec_block
        steps.append(
            f"Block '{block}' -> {dec_block}  (vector {vec.flatten().tolist()} * inv_key -> {dec_vec})")

    return {"plaintext": plaintext.lower(), "key_matrix": key_mat.tolist(), "steps": steps}


# -------------------------
# Standalone test (run as script)
# -------------------------
if __name__ == "__main__":
    print("--- Testing with TEXT key ---")
    params_text = {"key": "GYBNQKURP"}
    message = "ACT"
    enc_text = encrypt(message, params_text)
    print("Ciphertext:", enc_text["ciphertext"])
    print("Steps:")
    for s in enc_text["steps"]:
        print(" ", s)

    print("\n" + "="*30 + "\n")

    print("--- Testing with MATRIX key ---")
    # This is the matrix equivalent of "GYBNQKURP"
    params_matrix = {"key_matrix": [[6, 24, 1], [13, 16, 10], [20, 17, 15]]}
    enc_matrix = encrypt(message, params_matrix)
    print("Ciphertext:", enc_matrix["ciphertext"])
    print("Steps:")
    for s in enc_matrix["steps"]:
        print(" ", s)

    print("\n--- Testing Decryption ---")
    dec = decrypt(enc_matrix["ciphertext"], params_matrix)
    print("\nDecrypted back:", dec["plaintext"])
    print("Decryption steps:")
    for s in dec["steps"]:
        print(" ", s)
