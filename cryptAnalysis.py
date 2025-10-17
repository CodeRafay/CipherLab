# cryptanalysis_logic.py

import string
from collections import Counter
from typing import Dict, Tuple


def calculate_frequencies(text: str) -> Dict[str, int]:
    """
    Calculates the frequency of each letter (A-Z) in a given text.

    The function is case-insensitive and ignores all non-alphabetic characters,
    including spaces, numbers, and punctuation.

    Args:
        text (str): The input string to analyze.

    Returns:
        Dict[str, int]: A dictionary mapping each uppercase letter to its frequency count.
                        Letters that do not appear in the text are included with a count of 0.
    """
    # Initialize a counter with all letters of the alphabet set to 0
    frequencies = {letter: 0 for letter in string.ascii_uppercase}

    # Filter the text to only include alphabetic characters and convert to uppercase
    filtered_text = filter(str.isalpha, text.upper())

    # Count the occurrences of each character
    letter_counts = Counter(filtered_text)

    # Update the initial dictionary with the actual counts
    frequencies.update(letter_counts)

    return frequencies


def get_reference_frequencies() -> Dict[str, float]:
    """
    Returns a dictionary of the standard, average frequencies of letters in the English language.

    These values are useful for comparing the frequency distribution of a ciphertext
    against a known linguistic standard to identify potential letter substitutions.


    Returns:
        Dict[str, float]: A dictionary mapping each uppercase letter to its
                          standard frequency as a percentage (e.g., 'E' -> 12.702).
    """
    return {
        'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702, 'F': 2.228,
        'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153, 'K': 0.772, 'L': 4.025,
        'M': 2.406, 'N': 6.749, 'O': 7.507, 'P': 1.929, 'Q': 0.095, 'R': 5.987,
        'S': 6.327, 'T': 9.056, 'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150,
        'Y': 1.974, 'Z': 0.074
    }


def calculate_ic(text: str) -> Tuple[float, str]:
    """
    Calculates the Index of Coincidence (IC) for a given text.

    The IC is a statistical measure of how similar a frequency distribution is to the
    uniform distribution. It is a powerful tool for differentiating between cipher types.

    Args:
        text (str): The input string to analyze.

    Returns:
        Tuple[float, str]: A tuple containing:
            - The calculated Index of Coincidence value.
            - A string with a brief interpretation of the result.
    """
    # Get the frequency counts of each letter in the text.
    frequencies = calculate_frequencies(text)

    # Filter out non-alphabetic characters and get the total length.
    filtered_text = ''.join(filter(str.isalpha, text))
    N = len(filtered_text)

    # If there are fewer than 2 letters, IC is not meaningful.
    if N < 2:
        return 0.0, "Not enough text to calculate the Index of Coincidence."

    # The formula for IC is: Σ [ n_i * (n_i - 1) ] / [ N * (N - 1) ]
    # where n_i is the count of the i-th letter and N is the total number of letters.
    numerator = sum(n * (n - 1) for n in frequencies.values())
    denominator = N * (N - 1)

    ic = numerator / denominator

    # Provide a helpful interpretation of the IC value.
    interpretation = ""
    if ic > 0.060:
        interpretation = (f"The IC value of {ic:.4f} is high, closely matching the IC of standard English (~0.067). "
                          "This strongly suggests the text is either plaintext or has been encrypted "
                          "with a **monoalphabetic substitution cipher** (like Caesar, Affine, or simple substitution).")
    elif ic < 0.045:
        interpretation = (f"The IC value of {ic:.4f} is low, approaching the value for random text (~0.038). "
                          "This strongly suggests the text has been encrypted with a **polyalphabetic cipher** "
                          "(like Vigenere or Enigma) or a transposition cipher, which flattens the frequency distribution.")
    else:
        interpretation = (f"The IC value of {ic:.4f} is intermediate. This could indicate a short polyalphabetic "
                          "key, a cipher that only partially obscures frequencies, or simply a short text sample.")

    return ic, interpretation


# --- Standalone Example Usage ---
if __name__ == "__main__":
    # Example 1: A simple Caesar-shifted ciphertext
    monoalphabetic_ciphertext = "KHOOR ZRUOG, WKLV LV D WHVW RI WKH CAHVDU FLSHU."
    print("--- Analyzing Monoalphabetic Ciphertext ---")
    print(f"Ciphertext: '{monoalphabetic_ciphertext}'")

    # Test frequency calculation
    freqs = calculate_frequencies(monoalphabetic_ciphertext)
    print("\nLetter Frequencies:")
    print(freqs)

    # Test Index of Coincidence calculation
    ic_value, ic_interp = calculate_ic(monoalphabetic_ciphertext)
    print(f"\nCalculated Index of Coincidence: {ic_value:.4f}")
    print("Interpretation:", ic_interp)

    print("\n" + "="*60 + "\n")

    # Example 2: A Vigenère-encrypted ciphertext (polyalphabetic)
    polyalphabetic_ciphertext = "LXFOPVEFRNHR"  # "ATTACKATDAWN" with key "LEMON"
    print("--- Analyzing Polyalphabetic Ciphertext ---")
    print(f"Ciphertext: '{polyalphabetic_ciphertext}'")

    # Test frequency calculation
    freqs_poly = calculate_frequencies(polyalphabetic_ciphertext)
    print("\nLetter Frequencies:")
    print(freqs_poly)

    # Test Index of Coincidence calculation
    ic_value_poly, ic_interp_poly = calculate_ic(polyalphabetic_ciphertext)
    print(f"\nCalculated Index of Coincidence: {ic_value_poly:.4f}")
    print("Interpretation:", ic_interp_poly)
