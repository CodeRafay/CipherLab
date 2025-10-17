# ciphers/enigmaRotor.py
"""
Simplified Enigma rotor machine (educational)

Features:
- 3-rotor configuration (using historical Enigma I rotor wirings)
- Simple stepping: fast rotor steps every keypress; middle steps when fast completes a full revolution; slow steps when middle completes
- Reflector B for symmetric mapping (encryption == decryption)
- Detailed per-letter steps for pedagogical visualization

Limitations (intentionally simplified):
- No ring setting, no notch-based double-stepping, no plugboard
- Stepping uses full-turn carry (pos wraps to 0) rather than rotor notch mechanics
"""

import string
from typing import Tuple, Dict, Any, List

ALPHABET = string.ascii_uppercase

# Historical rotor wirings (Enigma I)
ROTOR_I = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_II = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_III = "BDFHJLCPRTXVZNYEIWGAKMUSQO"

# Reflector B (historical)
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"


# -------------------------
# Helper utilities
# -------------------------
def _char_to_index(c: str) -> int:
    return ALPHABET.index(c)


def _index_to_char(i: int) -> str:
    return ALPHABET[i % 26]


def rotor_forward(idx: int, wiring: str, pos: int) -> int:
    """
    Pass signal forward through rotor with a given rotational offset.
    """
    i = (idx + pos) % 26
    mapped_char = wiring[i]
    mapped_index = ALPHABET.index(mapped_char)
    return (mapped_index - pos) % 26


def rotor_backward(idx: int, wiring: str, pos: int) -> int:
    """
    Pass signal backward (inverse) through rotor with given offset.
    """
    i = (idx + pos) % 26
    j = wiring.index(ALPHABET[i])
    return (j - pos) % 26


def reflect(idx: int, reflector: str) -> int:
    """Reflector mapping (no offset)."""
    return ALPHABET.index(reflector[idx])


# -------------------------
# Core Enigma functions
# -------------------------
def encrypt(plaintext: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Encrypt plaintext using simplified 3-rotor Enigma.
    Accepts a parameters dictionary with 'rotor_positions'.
    """
    # Extract rotor positions from the parameters dictionary for compatibility
    rotor_positions = parameters.get("rotor_positions", ("A", "A", "A"))

    rotor1, rotor2, rotor3 = ROTOR_I, ROTOR_II, ROTOR_III
    reflector = REFLECTOR_B

    # convert positions to integer offsets
    pos1 = _char_to_index(rotor_positions[0])
    pos2 = _char_to_index(rotor_positions[1])
    pos3 = _char_to_index(rotor_positions[2])

    steps: List[str] = []
    ciphertext = ""

    steps.append(
        f"Initial rotor positions (fast, med, slow): {rotor_positions}, offsets = ({pos1},{pos2},{pos3})")
    steps.append(
        f"Rotor wirings:\n fast:  {rotor1}\n med:   {rotor2}\n slow:  {rotor3}")

    for char in plaintext:
        if char.upper() not in ALPHABET:
            ciphertext += char
            steps.append(f"Non-letter preserved: '{char}'")
            continue

        # STEP ROTORS: fast rotor steps before enciphering
        pos1 = (pos1 + 1) % 26
        if pos1 == 0:
            pos2 = (pos2 + 1) % 26
            if pos2 == 0:
                pos3 = (pos3 + 1) % 26

        steps.append(
            f"Positions after stepping: offsets=(fast:{pos1},med:{pos2},slow:{pos3})")

        c_idx = _char_to_index(char.upper())
        path = [f"Input '{char.upper()}' ({c_idx})"]

        # Signal path forward
        out1 = rotor_forward(c_idx, rotor1, pos1)
        path.append(f"-> rotor1 out '{_index_to_char(out1)}'")
        out2 = rotor_forward(out1, rotor2, pos2)
        path.append(f"-> rotor2 out '{_index_to_char(out2)}'")
        out3 = rotor_forward(out2, rotor3, pos3)
        path.append(f"-> rotor3 out '{_index_to_char(out3)}'")

        # Reflector
        refl = reflect(out3, reflector)
        path.append(f"-> reflector '{_index_to_char(refl)}'")

        # Signal path backward
        back3 = rotor_backward(refl, rotor3, pos3)
        path.append(f"-> back rotor3 '{_index_to_char(back3)}'")
        back2 = rotor_backward(back3, rotor2, pos2)
        path.append(f"-> back rotor2 '{_index_to_char(back2)}'")
        back1 = rotor_backward(back2, rotor1, pos1)
        path.append(f"-> back rotor1 '{_index_to_char(back1)}'")

        out_char = _index_to_char(back1)
        ciphertext += out_char

        steps.append("  ".join(path) + f"  => Output '{out_char}'")
        steps.append("-" * 60)

    return {
        "ciphertext": ciphertext,
        "steps": steps,
        "rotors": [rotor1, rotor2, rotor3],
        "initial_positions": rotor_positions
    }


def decrypt(ciphertext: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decrypt ciphertext using the simplified Enigma. Encryption and decryption are symmetric.
    """
    return encrypt(ciphertext, parameters)


# -------------------------
# Standalone test/demo
# -------------------------
if __name__ == "__main__":
    msg = "Django"
    # Updated to use the dictionary format required by the new function signature
    params = {"rotor_positions": ("A", "A", "A")}
    res = encrypt(msg, params)

    print("Initial positions:", res["initial_positions"])
    print("Rotor wirings (fast, med, slow):")
    for r in res["rotors"]:
        print(" ", r)
    print("\nCiphertext:", res["ciphertext"])
    print("\nDetailed steps:")
    for s in res["steps"]:
        print(s)

    # Decrypt with the same parameters dictionary
    res_dec = decrypt(res["ciphertext"], params)
    print("\nDecrypted text:", res_dec["ciphertext"])
