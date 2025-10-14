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
    # determinant may be float due to numpy; round to nearest int
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
    # adjugate is transpose of cofactor matrix
    adj = cofactors.T
    return adj


def matrix_mod_inv(mat: np.ndarray, mod: int = MOD) -> np.ndarray:
    """
    Compute modular inverse of integer matrix `mat` modulo `mod`.
    Uses det, adjugate method:
        inv_mod = det_inv * adj(mat)  (mod m)
    Raises ValueError if inverse doesn't exist.
    """
    if mat.shape[0] != mat.shape[1]:
        raise ValueError("Key matrix must be square.")
    n = mat.shape[0]
    det = int(round(np.linalg.det(mat)))  # integer determinant
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
    Accepts either:
    - parameters['key_matrix']: a list-of-lists (ints) representing the key matrix, OR
    - parameters['key']: a string whose length is a perfect square (e.g., 4,9,16) and will be converted to numbers
    Returns numpy.ndarray (dtype=int)
    """
    if "key_matrix" in parameters and parameters["key_matrix"] is not None:
        mat = np.array(parameters["key_matrix"], dtype=int)
        if mat.shape[0] != mat.shape[1]:
            raise ValueError("Provided key_matrix must be square.")
        return mat
    elif "key" in parameters and parameters["key"]:
        key = str(parameters["key"]).upper().replace(" ", "")
        nums = text_to_numbers(key)
        size = int(len(nums) ** 0.5)
        if size * size != len(nums):
            raise ValueError(
                "Key string length must be a perfect square (4, 9, 16...).")
        mat = np.array(nums, dtype=int).reshape(size, size)
        return mat
    else:
        raise ValueError(
            "No key provided. Provide 'key_matrix' or 'key' in parameters.")

# -------------------------
# Encryption / Decryption
# -------------------------


def encrypt(plaintext: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hill cipher encryption.
    parameters: expects 'key_matrix' (list of lists) OR 'key' (string of length n*n)
    Returns dict with:
        ciphertext (str),
        key_matrix (list of lists),
        steps (list of step strings)
    """
    key_mat = parse_key_matrix_from_params(parameters)
    key_mat = key_mat % MOD
    n = key_mat.shape[0]

    # Prepare plaintext: uppercase, remove non-alpha, pad with 'X' if necessary
    filtered = "".join([c for c in plaintext if c.isalpha()]).upper()
    if len(filtered) == 0:
        return {"ciphertext": "", "key_matrix": key_mat.tolist(), "steps": []}
    if len(filtered) % n != 0:
        pad_len = n - (len(filtered) % n)
        filtered += "X" * pad_len

    steps = []
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
    parameters: expects 'key_matrix' (list of lists) OR 'key' (string of length n*n)
    Returns dict with:
        plaintext (str),
        key_matrix (list of lists),
        steps (list of step strings)
    """
    key_mat = parse_key_matrix_from_params(parameters)
    key_mat = key_mat % MOD
    n = key_mat.shape[0]

    # compute modular inverse of key matrix
    inv_key = matrix_mod_inv(key_mat, MOD)

    # Prepare ciphertext: uppercase, remove non-alpha
    filtered = "".join([c for c in ciphertext if c.isalpha()]).upper()
    if len(filtered) == 0:
        return {"plaintext": "", "key_matrix": key_mat.tolist(), "steps": []}
    if len(filtered) % n != 0:
        raise ValueError(
            f"Ciphertext length must be multiple of key matrix size {n}.")

    steps = []
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
    # Example using classic 3x3 key "GYBNQKURP" -> matrix [[6,24,1],[13,16,10],[20,17,15]]
    # alternative: {"key_matrix": [[6,24,1],[13,16,10],[20,17,15]]}
    params = {"key": "GYBNQKURP"}
    message = "ACT"

    enc = encrypt(message, params)
    print("Plaintext:", message)
    print("Key matrix:")
    for row in enc["key_matrix"]:
        print(row)
    print("Ciphertext:", enc["ciphertext"])
    print("Steps:")
    for s in enc["steps"]:
        print(" ", s)

    dec = decrypt(enc["ciphertext"], params)
    print("\nDecrypted back:", dec["plaintext"])
    print("Decryption steps:")
    for s in dec["steps"]:
        print(" ", s)
