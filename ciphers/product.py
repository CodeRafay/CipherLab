# product.py

import os
import importlib
import traceback
from typing import List, Dict, Any
import sys

# --- 1. DYNAMIC CIPHER LOADING ---
# This dictionary will hold the imported cipher modules.
CIPHER_MODULES = {}


def load_ciphers(path: str = "ciphers"):
    """
    Dynamically finds and imports all valid .py cipher files from a given directory.
    This makes the application extensible without changing this file.

    Args:
        path (str): The directory path to scan for cipher modules. Defaults to "ciphers".
    """
    global CIPHER_MODULES
    # Add the target path to sys.path to ensure modules are findable
    if path not in sys.path:
        sys.path.append(path)

    # Exclude this file itself and any utility/dunder files.
    excluded_files = ["__init__.py", "product.py", "app.py"]

    # Simple way to get a pretty name from a filename like 'railFence.py' -> 'Rail Fence'
    def format_name(filename):
        name = os.path.splitext(filename)[0]
        # Special handling for names that should be one word
        if name.lower() in ["onetimepad", "playfair"]:
            return name.capitalize()
        # Add spaces before capital letters for names like 'railFence' -> 'Rail Fence'
        return ''.join([' ' + char if char.isupper() else char for char in name]).lstrip().title()

    try:
        for filename in os.listdir(path):
            if filename.endswith(".py") and filename not in excluded_files:
                module_name = os.path.splitext(filename)[0]
                try:
                    module = importlib.import_module(module_name)
                    # Ensure the module has an encrypt or similar function
                    if hasattr(module, 'encrypt') or hasattr(module, 'string_encryption') or hasattr(module, 'encrypt_row_column_transposition'):
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
# This is crucial for making the different cipher files work together.


def _call_cipher_op(op_type: str, cipher_name: str, text: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    A centralized adapter function to call the correct encrypt/decrypt method
    for any given cipher, normalizing its parameters and return value.

    Args:
        op_type (str): Either 'encrypt' or 'decrypt'.
        cipher_name (str): The pretty name of the cipher (e.g., "Caesar", "Hill").
        text (str): The input text for the operation.
        params (Dict[str, Any]): A dictionary of parameters required by the cipher.

    Returns:
        Dict[str, Any]: A standardized dictionary containing 'text' and 'steps'.
    """
    module = CIPHER_MODULES.get(cipher_name)
    if not module:
        raise ValueError(f"Cipher '{cipher_name}' not found or loaded.")

    result = {}
    try:
        # Normalize to the module's actual name for logic branching
        module_name = module.__name__

        if module_name in ["caesar", "affine"]:
            func = getattr(module, op_type)
            output_text, steps = func(text, params)
            result = {"text": output_text, "steps": steps}

        elif module_name in ["hill", "vigenere", "playFair"]:
            func = getattr(module, op_type)
            raw_output = func(text, params)
            key_to_get = "ciphertext" if op_type == "encrypt" else "plaintext"
            result = {"text": raw_output.get(
                key_to_get, ""), "steps": raw_output.get("steps", [])}

        elif module_name == "railFence":
            func = getattr(module, op_type)
            # Pass only the relevant 'rails' parameter
            output_text, matrix = func(text, params.get("rails", 3))
            viz = "\n".join(" ".join(ch if ch else "." for ch in row)
                            for row in matrix)
            result = {"text": output_text, "steps": [
                f"Rail Fence Matrix:\n{viz}"]}

        elif module_name == "columnTransposition":
            # Standardize function names by wrapping them
            encrypt_func = module.encrypt_row_column_transposition
            decrypt_func = module.decrypt_row_column_transposition

            func = encrypt_func if op_type == "encrypt" else decrypt_func
            output_text = func(text, params.get("key", "KEY"))
            result = {"text": output_text, "steps": [
                f"Performed Columnar Transposition with key '{params.get('key')}'."]}

        elif module_name == "OneTimePad":
            # Standardize function names by wrapping them
            encrypt_func = module.string_encryption
            decrypt_func = module.string_decryption

            func = encrypt_func if op_type == "encrypt" else decrypt_func
            raw_output = func(text, params.get("key", ""))
            key_to_get = "ciphertext" if op_type == "encrypt" else "plaintext"
            result = {"text": raw_output.get(
                key_to_get, ""), "steps": raw_output.get("steps", [])}

        elif module_name == "enigmaRotor":
            # Decrypt is the same as encrypt for Enigma, so both point to encrypt
            func = module.encrypt
            rotor_pos = tuple(params.get("rotor_positions", ("A", "A", "A")))
            raw_output = func(text, rotor_pos)
            result = {"text": raw_output.get(
                "ciphertext", ""), "steps": raw_output.get("steps", [])}

        else:
            raise NotImplementedError(
                f"Adapter not implemented for cipher '{cipher_name}'.")

    except Exception as e:
        # Catch errors from individual ciphers (e.g., bad key) and report them gracefully
        return {"text": f"ERROR in {cipher_name}: {e}", "steps": [f"An error occurred: {traceback.format_exc()}"]}

    return result


# --- 3. CORE PRODUCT CIPHER LOGIC ---

def encrypt(plaintext: str, cipher1: str, params1: Dict, cipher2: str, params2: Dict) -> Dict:
    """
    Encrypts plaintext by applying two ciphers in sequence.
    Flow: Plaintext -> Cipher1 -> Intermediate -> Cipher2 -> Final Ciphertext

    Returns:
        A dictionary with the final ciphertext and a combined list of steps.
    """
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


def decrypt(ciphertext: str, cipher1: str, params1: Dict, cipher2: str, params2: Dict) -> Dict:
    """
    Decrypts ciphertext by applying two ciphers in reverse order.
    Flow: Ciphertext -> Cipher2 -> Intermediate -> Cipher1 -> Final Plaintext

    Returns:
        A dictionary with the final plaintext and a combined list of steps.
    """
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
    # This block demonstrates how to use the functions programmatically.
    # You would import and use these functions in your app.py file.

    print("Loading available ciphers from './ciphers/' directory...")
    load_ciphers()  # Will use the default path "ciphers"

    if not get_available_ciphers():
        print("\nNo ciphers found. Make sure your cipher files are in a 'ciphers' subdirectory.")
    else:
        print("\nAvailable ciphers:", get_available_ciphers())

        print("\n--- Example: Vigenere -> Rail Fence ---")

        # 1. Define the inputs
        original_text = "THIS IS A SECRET MESSAGE"

        # Cipher 1: Vigenere
        c1_name = "Vigenere"
        c1_params = {"key": "CRYPTO"}

        # Cipher 2: Rail Fence
        c2_name = "Rail Fence"
        c2_params = {"rails": 4}

        # 2. Encrypt the message
        encryption_result = encrypt(
            original_text, c1_name, c1_params, c2_name, c2_params)

        print(f"\nOriginal Text: {original_text}")
        print(f"Final Ciphertext: {encryption_result['ciphertext']}")
        print("\n--- Encryption Steps ---")
        print("\n".join(encryption_result['steps']))

        # 3. Decrypt the message
        ciphertext = encryption_result['ciphertext']
        decryption_result = decrypt(
            ciphertext, c1_name, c1_params, c2_name, c2_params)

        print("\n--- Decryption Steps ---")
        print("\n".join(decryption_result['steps']))
        print(f"\nDecrypted Text: {decryption_result['plaintext']}")

        # Verification
        if not "ERROR" in decryption_result['plaintext']:
            print(
                f"\nDecryption successful: {decryption_result['plaintext'].lower() == original_text.lower().replace(' ', '')}")
