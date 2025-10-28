# cipherEngine.py

import os
import importlib
import traceback
from typing import List, Dict, Any
import sys

# --- 1. DYNAMIC CIPHER LOADING ---
CIPHER_MODULES = {}


def load_ciphers(path: str = "ciphers"):
    """
    Dynamically finds and imports all valid .py cipher files from a given directory.
    This makes the application extensible without changing this file.
    """
    global CIPHER_MODULES
    if path not in sys.path:
        sys.path.append(path)
    excluded_files = ["__init__.py"]

    def format_name(filename):
        name = os.path.splitext(filename)[0]
        if name.lower() in ["onetimepad", "playfair", "des", "aes"]:
            return name.upper() if name.lower() in ["des", "aes"] else name.capitalize()
        return ''.join([' ' + char if char.isupper() else char for char in name]).lstrip().title()

    try:
        for filename in os.listdir(path):
            if filename.endswith(".py") and filename not in excluded_files:
                module_name = os.path.splitext(filename)[0]
                try:
                    # Ensure module is reloaded if it already exists (for development)
                    if module_name in sys.modules:
                        importlib.reload(sys.modules[module_name])

                    module = importlib.import_module(module_name)
                    if hasattr(module, 'encrypt') and hasattr(module, 'decrypt'):
                        pretty_name = format_name(filename)
                        CIPHER_MODULES[pretty_name] = module
                        print(f"Successfully loaded cipher: {pretty_name}")
                except ImportError as e:
                    print(f"Error importing {module_name}: {e}")
                    traceback.print_exc()
    except FileNotFoundError:
        print(
            f"Warning: Directory '{path}' not found. No ciphers were loaded.")


def get_available_ciphers() -> List[str]:
    """Returns a sorted list of names of the loaded ciphers."""
    return sorted(CIPHER_MODULES.keys())

# --- 2. ADAPTER LAYER (Handles Inconsistencies) ---


def _call_cipher_op(op_type: str, cipher_name: str, text: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    A centralized adapter function to call the correct encrypt/decrypt method
    for any given cipher, normalizing its parameters and return value.
    """
    module = CIPHER_MODULES.get(cipher_name)
    if not module:
        raise ValueError(f"Cipher '{cipher_name}' not found or loaded.")

    result = {}
    try:
        module_name = module.__name__.lower()  # Use lower for consistent matching

        if module_name in ["caesar", "affine"]:
            func = getattr(module, op_type)
            output_text, steps = func(text, params)
            result = {"text": output_text, "steps": steps}

        elif module_name in ["hill", "vigenere", "playfair", "enigmarotor", "columntransposition", "onetimepad", "des", "aes"]:
            func = getattr(module, op_type)
            raw_output = func(text, params)
            key_to_get = "ciphertext" if op_type == "encrypt" else "plaintext"

            # Special case for enigma
            if module_name == "enigmarotor":
                key_to_get = "ciphertext"  # Enigma module returns 'ciphertext' for both ops

            result = {"text": raw_output.get(key_to_get, ""), "steps": raw_output.get(
                "steps", []), "key": raw_output.get("key")}

        elif module_name == "railfence":
            func = getattr(module, op_type)
            output_text, matrix = func(text, **params)
            viz = "\n".join(" ".join(ch if ch else "." for ch in row)
                            for row in matrix)
            result = {"text": output_text, "steps": [
                f"Rail Fence Matrix:\n{viz}"]}

        else:
            raise NotImplementedError(
                f"Adapter not implemented for cipher '{cipher_name}' ({module_name}).")

    except Exception as e:
        error_message = f"ERROR in {cipher_name}: {e}"
        print(error_message)
        traceback.print_exc()
        return {"text": error_message, "steps": [f"An error occurred: {traceback.format_exc()}"]}

    return result

# --- 3. PUBLIC API FUNCTIONS ---


def process_single_cipher(op_type: str, cipher_name: str, text: str, params: Dict[str, Any]) -> Dict[str, Any]:
    return _call_cipher_op(op_type, cipher_name, text, params)


def encrypt_product(plaintext: str, cipher1: str, params1: Dict, cipher2: str, params2: Dict) -> Dict:
    stage1_result = _call_cipher_op("encrypt", cipher1, plaintext, params1)
    intermediate_text = stage1_result["text"]
    if "ERROR" in intermediate_text:
        return {"ciphertext": intermediate_text, "steps": stage1_result["steps"]}
    stage2_result = _call_cipher_op(
        "encrypt", cipher2, intermediate_text, params2)
    final_ciphertext = stage2_result["text"]
    all_steps = [
        f"--- STAGE 1: {cipher1} Encryption ---",
        *stage1_result.get("steps", ["No steps provided."]),
        f"\nIntermediate Text: {intermediate_text}\n",
        f"--- STAGE 2: {cipher2} Encryption ---",
        *stage2_result.get("steps", ["No steps provided."]),
    ]
    return {"ciphertext": final_ciphertext, "steps": all_steps}


def decrypt_product(ciphertext: str, cipher1: str, params1: Dict, cipher2: str, params2: Dict) -> Dict:
    stage1_result = _call_cipher_op("decrypt", cipher2, ciphertext, params2)
    intermediate_text = stage1_result["text"]
    if "ERROR" in intermediate_text:
        return {"plaintext": intermediate_text, "steps": stage1_result["steps"]}
    stage2_result = _call_cipher_op(
        "decrypt", cipher1, intermediate_text, params1)
    final_plaintext = stage2_result["text"]
    all_steps = [
        f"--- STAGE 1: {cipher2} Decryption (Reverse Order) ---",
        *stage1_result.get("steps", ["No steps provided."]),
        f"\nIntermediate Text: {intermediate_text}\n",
        f"--- STAGE 2: {cipher1} Decryption (Reverse Order) ---",
        *stage2_result.get("steps", ["No steps provided."]),
    ]
    return {"plaintext": final_plaintext, "steps": all_steps}


# --- 4. STANDALONE EXAMPLE USAGE ---
if __name__ == "__main__":
    print("Loading available ciphers from './ciphers/' directory...")
    load_ciphers()

    if not get_available_ciphers():
        print("\nNo ciphers found. Make sure your cipher files are in a 'ciphers' subdirectory.")
    else:
        print("\nAvailable ciphers:", get_available_ciphers())

        print("\n--- Testing Single Cipher: Caesar ---")
        caesar_result = process_single_cipher(
            "encrypt", "Caesar", "HELLO WORLD", {"shift": 3})
        print(f"Result: {caesar_result['text']}")
        print("--- Caesar Steps ---")
        print("\n".join(caesar_result['steps']))

        print("\n--- Testing Single Cipher: AES ---")
        aes_result = process_single_cipher(
            "encrypt", "AES", "This is a test.", {"key": "mysecretkey12345"})
        print(f"Result: {aes_result['text']}")
        aes_dec_result = process_single_cipher(
            "decrypt", "AES", aes_result['text'], {"key": "mysecretkey12345"})
        print(f"Decrypted: {aes_dec_result['text']}")

        print("\n--- Testing Product Cipher: Vigenere -> AES ---")
        original_text = "THIS IS A SECRET MESSAGE"
        c1_name, c1_params = "Vigenere", {"key": "CRYPTO"}
        c2_name, c2_params = "AES", {"key": "2b7e151628aed2a6abf7158809cf4f3c"}

        encryption_result = encrypt_product(
            original_text, c1_name, c1_params, c2_name, c2_params)
        print(f"\nOriginal Text: {original_text}")
        print(f"Final Ciphertext: {encryption_result['ciphertext']}")
        print("\n--- Product Encryption Steps ---")
        print("\n".join(encryption_result['steps']))

        decryption_result = decrypt_product(
            encryption_result['ciphertext'], c1_name, c1_params, c2_name, c2_params)
        print(f"\nDecrypted Text: {decryption_result['plaintext']}")
        print("\n--- Product Decryption Steps ---")
        print("\n".join(decryption_result['steps']))
