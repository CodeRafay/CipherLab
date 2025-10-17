# app.py

import streamlit as st
import os
import pandas as pd
from typing import Dict, Any

# --- Import Core Logic ---
# These imports assume product.py and cryptAnalysis.py are in the root directory.
from cipherEngine import (
    load_ciphers,
    get_available_ciphers,
    process_single_cipher,
    encrypt_product,
    decrypt_product
)
from cryptAnalysis import (
    calculate_frequencies,
    get_reference_frequencies,
    calculate_ic
)

# --- App Configuration ---
st.set_page_config(
    page_title="CipherLab",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Helper Function for UI Parameter Inputs ---


def get_ui_params(cipher_name: str, key_prefix: str) -> Dict[str, Any]:
    """
    Dynamically creates Streamlit UI widgets for cipher parameters based on the cipher name.
    """
    params = {}
    st.markdown(f"**Parameters for {cipher_name}**")

    if cipher_name == "Caesar":
        params["shift"] = st.slider(
            "Shift", 1, 25, 3, key=f"{key_prefix}_shift")
    elif cipher_name == "Affine":
        st.info(
            "'a' must be coprime with 26: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25.")
        params["a"] = st.number_input(
            "a", value=5, step=2, key=f"{key_prefix}_a")
        params["b"] = st.number_input("b", value=8, key=f"{key_prefix}_b")
    elif cipher_name in ["Vigenere", "Column Transposition"]:
        params["key"] = st.text_input(
            "Keyword", value="KEY", key=f"{key_prefix}_key").upper()
    elif cipher_name == "Playfair":
        params["keyword"] = st.text_input(
            "Keyword", value="MONARCHY", key=f"{key_prefix}_keyword").lower()

    elif cipher_name == "Hill":
        key_type = st.radio("Key Input Type", ("Text Key", "Matrix Key"),
                            key=f"{key_prefix}_hill_key_type", horizontal=True)
        if key_type == "Text Key":
            params["key"] = st.text_input(
                "Key String (length 4, 9, or 16)", value="GYBNQKURP", key=f"{key_prefix}_hill_key").upper()
        else:
            st.markdown(
                "Enter the key matrix below. Each row on a new line, numbers separated by commas.")
            matrix_input = st.text_area(
                "Key Matrix", value="6, 24, 1\n13, 16, 10\n20, 17, 15", key=f"{key_prefix}_hill_matrix", height=100)
            try:
                matrix = [[int(num.strip()) for num in row.split(',')]
                          for row in matrix_input.strip().split('\n')]
                params["key_matrix"] = matrix
            except ValueError:
                st.error(
                    "Invalid matrix format. Please ensure all values are integers.")
                params["key_matrix"] = None

    elif cipher_name == "Onetimepad":
        key_type = st.radio("Key Type", ("Provide Custom Key", "Generate Random Key"),
                            key=f"{key_prefix}_otp_type", horizontal=True)
        if key_type == "Provide Custom Key":
            st.info(
                "The key must be at least as long as the plaintext (after removing spaces).")
            params["key"] = st.text_input(
                "Enter Custom Key", value="SPARTANS", key=f"{key_prefix}_otp_key").upper()
            params["generate_key"] = False
        else:
            params["generate_key"] = True
            st.success(
                "A secure random key will be generated during encryption.")

    elif cipher_name == "Rail Fence":
        params["rails"] = st.number_input(
            "Rails", min_value=2, value=3, key=f"{key_prefix}_rails")
    elif cipher_name == "Enigma Rotor":
        cols = st.columns(3)
        r1 = cols[0].selectbox("Fast Rotor", list(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"), key=f"{key_prefix}_r1")
        r2 = cols[1].selectbox("Medium Rotor", list(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"), key=f"{key_prefix}_r2")
        r3 = cols[2].selectbox("Slow Rotor", list(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"), key=f"{key_prefix}_r3")
        params["rotor_positions"] = (r1, r2, r3)
    else:
        st.text("This cipher requires no special parameters.")

    return params

# --- Page Rendering Functions ---


def render_toolkit_page():
    """Renders the UI for the Single Cipher Toolkit page."""
    st.title("🛠️ Classical Cipher Toolkit")
    st.markdown("Encrypt or decrypt messages using a single classical cipher.")

    cipher_list = get_available_ciphers()
    selected_cipher = st.selectbox("Choose a Cipher", cipher_list)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Input")
        with st.expander("Parameters", expanded=True):
            params = get_ui_params(selected_cipher, "toolkit")

        input_text = st.text_area(
            "Enter Text Here", "ATTACK AT DAWN", height=150)

        encrypt_button, decrypt_button = st.columns(2)
        if encrypt_button.button("Encrypt", use_container_width=True, type="primary"):
            with st.spinner("Encrypting..."):
                result = process_single_cipher(
                    "encrypt", selected_cipher, input_text, params)
                st.session_state.toolkit_result = result

        if decrypt_button.button("Decrypt", use_container_width=True):
            with st.spinner("Decrypting..."):
                result = process_single_cipher(
                    "decrypt", selected_cipher, input_text, params)
                st.session_state.toolkit_result = result

    with col2:
        st.subheader("Output")
        if 'toolkit_result' in st.session_state:
            result = st.session_state.toolkit_result
            # For OTP, if a key was generated, display it to the user.
            if selected_cipher == "Onetimepad" and result.get("key"):
                st.info(f"Generated/Used Key: {result['key']}")
            st.code(result.get("text", "No output."), language="")

            with st.expander("Show Step-by-Step Breakdown"):
                st.text("\n".join(result.get(
                    "steps", ["No steps available."])))


def render_product_lab_page():
    """Renders the UI for the Product Cipher Lab page."""
    st.title("🔬 Product Cipher Laboratory")
    st.info("A Product Cipher enhances security by applying two ciphers in sequence. Decryption occurs in the reverse order of encryption.")

    cipher_list = get_available_ciphers()

    col1, col2 = st.columns(2)
    with col1:
        st.header("Stage 1 Cipher")
        cipher1_name = st.selectbox(
            "Select first cipher", cipher_list, key="c1")
        with st.expander("Parameters", expanded=True):
            params1 = get_ui_params(cipher1_name, "c1")

    with col2:
        st.header("Stage 2 Cipher")
        cipher2_name = st.selectbox(
            "Select second cipher", cipher_list, key="c2")
        with st.expander("Parameters", expanded=True):
            params2 = get_ui_params(cipher2_name, "c2")

    st.markdown("---")

    input_text = st.text_area(
        "Enter Text Here", "THIS IS A HIGHLY SECRET MESSAGE", height=150)

    encrypt_button, decrypt_button = st.columns(2)
    if encrypt_button.button("Encrypt Product Cipher", use_container_width=True, type="primary"):
        with st.spinner("Applying product encryption..."):
            result = encrypt_product(
                input_text, cipher1_name, params1, cipher2_name, params2)
            st.session_state.product_result = result

    if decrypt_button.button("Decrypt Product Cipher", use_container_width=True):
        with st.spinner("Applying product decryption..."):
            result = decrypt_product(
                input_text, cipher1_name, params1, cipher2_name, params2)
            st.session_state.product_result = result

    if 'product_result' in st.session_state:
        result = st.session_state.product_result
        output_key = "ciphertext" if "ciphertext" in result else "plaintext"

        st.subheader("Final Result")
        st.code(result.get(output_key, ""), language="")

        with st.expander("Show Detailed Steps"):
            st.text("\n".join(result.get("steps", [])))


def render_encyclopedia_page():
    """Renders the UI for the Cipher Encyclopedia page."""
    st.title("📚 Cipher Encyclopedia")
    st.markdown(
        "Learn about the history, mechanics, and security of each cipher.")

    try:
        desc_path = "descriptions"
        description_files = [f for f in os.listdir(
            desc_path) if f.endswith(".md")]

        # Create a more robust function to format filenames into display names
        def format_display_name(filename):
            name_no_ext = os.path.splitext(filename)[0]
            # Handle snake_case first
            name_spaced = name_no_ext.replace('_', ' ')
            # Use logic to insert spaces for camelCase, then title case the result
            final_name = ''.join([' ' + char if char.isupper() and i > 0 and name_spaced[i-1]
                                 != ' ' else char for i, char in enumerate(name_spaced)]).lstrip()
            # Handle special cases from product.py for consistency
            if final_name.lower() in ["onetimepad", "playfair"]:
                return final_name.capitalize()
            return final_name.title()

        cipher_names_map = {format_display_name(
            f): f for f in description_files}

        selected_cipher_name = st.selectbox(
            "Choose a cipher to learn about", sorted(cipher_names_map.keys()))

        if selected_cipher_name:
            file_path = os.path.join(
                desc_path, cipher_names_map[selected_cipher_name])
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            st.markdown(content, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error(
            "The 'descriptions' directory was not found. Please ensure it exists in the root directory.")


def render_cryptanalysis_page():
    """Renders the UI for the Cryptanalysis Tools page."""
    st.title("🔓 Cryptanalysis Tools")
    st.markdown("Analyze ciphertext to uncover its weaknesses and patterns.")

    tool = st.selectbox("Select a Tool", [
                        "Frequency Analysis", "Index of Coincidence (IC) Calculator"])
    input_text = st.text_area(
        "Enter Ciphertext to Analyze", "KHOOR ZRUOG...", height=200)

    if tool == "Frequency Analysis":
        st.subheader("Letter Frequency Analysis")
        if st.button("Analyze Frequencies"):
            if not input_text:
                st.warning("Please enter some text to analyze.")
            else:
                with st.spinner("Calculating frequencies..."):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Ciphertext Frequencies**")
                        freq_data = calculate_frequencies(input_text)
                        df = pd.DataFrame(list(freq_data.items()), columns=[
                                          'Letter', 'Count']).set_index('Letter')
                        st.bar_chart(df)
                    with col2:
                        st.markdown("**Standard English Frequencies (%)**")
                        ref_data = get_reference_frequencies()
                        df_ref = pd.DataFrame(list(ref_data.items()), columns=[
                                              'Letter', 'Percentage']).set_index('Letter')
                        st.bar_chart(df_ref)

    elif tool == "Index of Coincidence (IC) Calculator":
        st.subheader("Index of Coincidence (IC)")
        if st.button("Calculate IC"):
            if not input_text:
                st.warning("Please enter some text to analyze.")
            else:
                with st.spinner("Calculating IC..."):
                    ic_value, interpretation = calculate_ic(input_text)
                    st.metric(label="Index of Coincidence",
                              value=f"{ic_value:.4f}")
                    st.info(interpretation)

# --- Main App Logic ---


def main():
    """Main function to run the Streamlit app."""
    # Load ciphers at the start of the app
    load_ciphers("ciphers")

    st.sidebar.title("Cryptography Suite")
    st.sidebar.markdown(
        "A tool for learning and experimenting with classical ciphers.")

    page_options = {
        "Cipher Toolkit": render_toolkit_page,
        "Product Cipher Lab": render_product_lab_page,
        "Cipher Encyclopedia": render_encyclopedia_page,
        "Cryptanalysis Tools": render_cryptanalysis_page
    }

    page_selection = st.sidebar.radio("Go to", list(page_options.keys()))

    # Render the selected page
    page_options[page_selection]()

    st.sidebar.markdown("---")
    st.sidebar.info("Built for educational purposes.")


if __name__ == "__main__":
    main()
