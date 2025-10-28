# CipherLab: An Interactive Cryptography Learning Suite 🔐

Welcome to **CipherLab**! This project is a comprehensive, multi-page web application built with **Streamlit**, designed as an interactive and educational tool for anyone interested in the fascinating world of classical cryptography.

Whether you're a student, history enthusiast, or developer curious about encryption, CipherLab provides a hands-on platform to explore, experiment with, and understand the building blocks of secret communication.

---

## 🚀 Live Demo

Access the live, deployed version of the application here:
[CipherLabs](https://cipherlabs.streamlit.app)

---

## ✨ Key Features

CipherLab is organized into **four distinct modules**, each designed for a specific learning objective:

### 1. 🛠️ Cipher Toolkit

- Interactive sandbox to experiment with individual classical ciphers.
- Encrypt and decrypt messages with a wide range of ciphers (Caesar, Playfair, Hill, and more).
- Detailed, step-by-step breakdown of the cryptographic process.
- Dynamically adjust keys and parameters to see effects in real-time.

### 2. 🔬 Product Cipher Lab

- Explore the power of combining ciphers to enhance security.
- Create a "product cipher" by chaining any two ciphers in sequence.
- Understand encryption (Plaintext → Cipher1 → Cipher2 → Ciphertext) and decryption (Ciphertext → Cipher2 → Cipher1 → Plaintext) in reverse order.
- Analyze the full process trace for both encryption and decryption stages.

### 3. 📚 Cipher Encyclopedia

- A rich educational resource covering each cipher's history, methodology, and vulnerabilities.
- Examples and mathematical principles behind algorithms.
- Understand the historical context in which these ciphers were used and broken.

### 4. 🔓 Cryptanalysis Tools

- Think like a codebreaker and learn to exploit classical cipher weaknesses.
- **Frequency Analysis:** Visualize letter frequency in any ciphertext and compare to standard English distribution.
- **Index of Coincidence (IC) Calculator:** Statistical tool to help determine cipher types (monoalphabetic vs. polyalphabetic).

---

## 💻 Tech Stack

- **Frontend:** Streamlit
- **Backend & Logic:** Python
- **Data Manipulation & Visualization:** Pandas, NumPy (for Hill Cipher)

---

## 📂 Project Structure

```
CipherLab/
├── app.py                     # Main Streamlit app (UI logic)
├── cipher_engine.py           # Backend orchestrator for all ciphers
├── cryptanalysis_logic.py     # Backend logic for analytical tools
├── requirements.txt           # Python dependencies
│
├── ciphers/                   # Individual cipher algorithms
│   ├── __init__.py
│   └── *.py
│
└── descriptions/              # Educational content in Markdown
    └── *.md
```

---

## 🚀 Getting Started Locally

Follow these steps to run CipherLab on your local machine:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/CodeRafay/CipherLab.git
   cd CipherLab
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

Your browser should automatically open with the application running!

---

## 🤝 How to Contribute

Contributions are welcome and greatly appreciated! Whether it's adding a new cipher, improving the UI, or fixing a bug, your help makes this project better.

To contribute:

1. Fork the repository using the 'Fork' button in the top right.
2. Create a new branch for your feature or fix:

   ```bash
   git checkout -b feature/YourAmazingFeature
   ```

3. Make your changes and commit with a clear message.
4. Push your changes to your forked repository.
5. Open a Pull Request to the main `CodeRafay/CipherLab` repository.

Don't forget to leave a star ⭐ if you find this project useful or interesting!

---

## 📄 License

This project is licensed under the **Apache 2.0 License**. See the LICENSE file for more details.
