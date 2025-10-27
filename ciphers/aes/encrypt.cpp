// encrypt.cpp
// Performs encryption using AES 128-bit


#include <iostream>
#include <cstring>
#include <fstream>
#include <sstream>
#include <iomanip> // For formatting
#include "structures.h"

using namespace std;

/* Serves as the initial round during encryption
 * AddRoundKey is simply an XOR of a 128-bit block with the 128-bit key.
 */
void AddRoundKey(unsigned char * state, unsigned char * roundKey) {
	for (int i = 0; i < 16; i++) {
		state[i] ^= roundKey[i];
	}
}

/* Perform substitution to each of the 16 bytes
 * Uses S-box as lookup table 
 */
void SubBytes(unsigned char * state) {
	for (int i = 0; i < 16; i++) {
		state[i] = s[state[i]];
	}
}

// Shift left, adds diffusion
void ShiftRows(unsigned char * state) {
	unsigned char tmp[16];

	/* Column 1 */
	tmp[0] = state[0];
	tmp[1] = state[5];
	tmp[2] = state[10];
	tmp[3] = state[15];
	
	/* Column 2 */
	tmp[4] = state[4];
	tmp[5] = state[9];
	tmp[6] = state[14];
	tmp[7] = state[3];

	/* Column 3 */
	tmp[8] = state[8];
	tmp[9] = state[13];
	tmp[10] = state[2];
	tmp[11] = state[7];
	
	/* Column 4 */
	tmp[12] = state[12];
	tmp[13] = state[1];
	tmp[14] = state[6];
	tmp[15] = state[11];

	for (int i = 0; i < 16; i++) {
		state[i] = tmp[i];
	}
}

 /* MixColumns uses mul2, mul3 look-up tables
  * Source of diffusion
  */
void MixColumns(unsigned char * state) {
	unsigned char tmp[16];

	tmp[0] = (unsigned char) mul2[state[0]] ^ mul3[state[1]] ^ state[2] ^ state[3];
	tmp[1] = (unsigned char) state[0] ^ mul2[state[1]] ^ mul3[state[2]] ^ state[3];
	tmp[2] = (unsigned char) state[0] ^ state[1] ^ mul2[state[2]] ^ mul3[state[3]];
	tmp[3] = (unsigned char) mul3[state[0]] ^ state[1] ^ state[2] ^ mul2[state[3]];

	tmp[4] = (unsigned char)mul2[state[4]] ^ mul3[state[5]] ^ state[6] ^ state[7];
	tmp[5] = (unsigned char)state[4] ^ mul2[state[5]] ^ mul3[state[6]] ^ state[7];
	tmp[6] = (unsigned char)state[4] ^ state[5] ^ mul2[state[6]] ^ mul3[state[7]];
	tmp[7] = (unsigned char)mul3[state[4]] ^ state[5] ^ state[6] ^ mul2[state[7]];

	tmp[8] = (unsigned char)mul2[state[8]] ^ mul3[state[9]] ^ state[10] ^ state[11];
	tmp[9] = (unsigned char)state[8] ^ mul2[state[9]] ^ mul3[state[10]] ^ state[11];
	tmp[10] = (unsigned char)state[8] ^ state[9] ^ mul2[state[10]] ^ mul3[state[11]];
	tmp[11] = (unsigned char)mul3[state[8]] ^ state[9] ^ state[10] ^ mul2[state[11]];

	tmp[12] = (unsigned char)mul2[state[12]] ^ mul3[state[13]] ^ state[14] ^ state[15];
	tmp[13] = (unsigned char)state[12] ^ mul2[state[13]] ^ mul3[state[14]] ^ state[15];
	tmp[14] = (unsigned char)state[12] ^ state[13] ^ mul2[state[14]] ^ mul3[state[15]];
	tmp[15] = (unsigned char)mul3[state[12]] ^ state[13] ^ state[14] ^ mul2[state[15]];

	for (int i = 0; i < 16; i++) {
		state[i] = tmp[i];
	}
}

/* Each round operates on 128 bits at a time
 * The number of rounds is defined in AESEncrypt()
 */
void Round(unsigned char * state, unsigned char * key) {
	SubBytes(state);
	ShiftRows(state);
	MixColumns(state);
	AddRoundKey(state, key);
}

 // Same as Round() except it doesn't mix columns
void FinalRound(unsigned char * state, unsigned char * key) {
	SubBytes(state);
	ShiftRows(state);
	AddRoundKey(state, key);
}

/* The AES encryption function
 * Organizes the confusion and diffusion steps into one function
 */
void AESEncrypt(unsigned char * message, unsigned char * expandedKey, unsigned char * encryptedMessage) {
	unsigned char state[16]; // Stores the first 16 bytes of original message

	for (int i = 0; i < 16; i++) {
		state[i] = message[i];
	}

    cout << "--- Encryption Process Started ---" << endl;
	cout << "Initial Plaintext Block:" << endl;
	printState(state);

	int numberOfRounds = 9;

	cout << "--- Initial Round (Round 0) ---" << endl;
    cout << "Round Key 0:" << endl;
    printRoundKey(expandedKey);
	AddRoundKey(state, expandedKey); // Initial round
	cout << "After AddRoundKey:" << endl;
	printState(state);
    cout << "---------------------------------" << endl;


	for (int i = 0; i < numberOfRounds; i++) {
        cout << "--- Round " << (i + 1) << " ---" << endl;
        
		SubBytes(state);
        cout << "After SubBytes:" << endl;
        printState(state);

		ShiftRows(state);
        cout << "After ShiftRows:" << endl;
        printState(state);

		MixColumns(state);
        cout << "After MixColumns:" << endl;
        printState(state);
        
        cout << "Round Key " << (i + 1) << ":" << endl;
        printRoundKey(expandedKey + (16 * (i+1)));
		AddRoundKey(state, expandedKey + (16 * (i+1)));
        cout << "After AddRoundKey:" << endl;
        printState(state);
        cout << "---------------------------------" << endl;
	}

	cout << "--- Final Round (Round 10) ---" << endl;
	SubBytes(state);
    cout << "After SubBytes:" << endl;
    printState(state);

	ShiftRows(state);
    cout << "After ShiftRows:" << endl;
    printState(state);
    
    cout << "Round Key 10:" << endl;
    printRoundKey(expandedKey + 160);
	AddRoundKey(state, expandedKey + 160);
    cout << "After AddRoundKey (Final Ciphertext):" << endl;
	printState(state);
    cout << "---------------------------------" << endl;
    cout << "--- Encryption Process Finished ---" << endl << endl;

	// Copy encrypted state to buffer
	for (int i = 0; i < 16; i++) {
		encryptedMessage[i] = state[i];
	}
}

int main() {

	cout << "=============================" << endl;
	cout << " 128-bit AES Encryption Tool   " << endl;
	cout << "=============================" << endl;

	char message[1024];

	cout << "Enter the message to encrypt (max 1023 chars): ";
	cin.getline(message, sizeof(message));

	// Pad message to 16 bytes
	int originalLen = strlen((const char *)message);

	int paddedMessageLen = originalLen;

	if ((paddedMessageLen % 16) != 0) {
		paddedMessageLen = (paddedMessageLen / 16 + 1) * 16;
	}

	unsigned char * paddedMessage = new unsigned char[paddedMessageLen];
	for (int i = 0; i < paddedMessageLen; i++) {
		if (i >= originalLen) {
			paddedMessage[i] = 0; // Pad with null bytes
		}
		else {
			paddedMessage[i] = message[i];
		}
	}

    // *** MODIFIED ***
    cout << "\nOriginal message: " << message << endl;
    cout << "Padded message length: " << paddedMessageLen << " bytes" << endl;
    cout << "Padded message in hex:" << endl;
    std::cout << std::hex << std::setfill('0');
    for (int i = 0; i < paddedMessageLen; i++) {
        std::cout << "0x" << std::setw(2) << (int)paddedMessage[i] << " ";
        if ((i + 1) % 16 == 0) std::cout << endl; // Newline for each block
    }
    std::cout << std::dec << std::setfill(' ') << std::endl << std::endl;


	unsigned char * encryptedMessage = new unsigned char[paddedMessageLen];

	string str;
	cout << "Enter the 16-byte key as space-separated hex values (e.g., 01 04 02...): ";
	getline(cin, str); // Read the key string from the user

	istringstream hex_chars_stream(str);
	unsigned char key[16];
	int i = 0;
	unsigned int c;
	while (hex_chars_stream >> hex >> c)
	{
        if (i < 16) {
		    key[i] = c;
		    i++;
        }
	}
    if (i != 16) {
        cout << "Error: Key must be 16 bytes. You entered " << i << " bytes. Exiting." << endl;
        delete[] paddedMessage;
        delete[] encryptedMessage;
        return 1;
    }

	unsigned char expandedKey[176];

	KeyExpansion(key, expandedKey);

	for (int i = 0; i < paddedMessageLen; i += 16) {
        cout << "========================================" << endl;
        cout << " Encrypting Block " << (i / 16) << endl;
        cout << "========================================" << endl;
		AESEncrypt(paddedMessage+i, expandedKey, encryptedMessage+i);
	}

	cout << "\n========================================" << endl;
	cout << "Final Encrypted message in hex:" << endl;
    std::cout << std::hex << std::setfill('0');
	for (int i = 0; i < paddedMessageLen; i++) {
		cout << "0x" << std::setw(2) << (int) encryptedMessage[i] << " ";
	}
    std::cout << std::dec << std::setfill(' ') << std::endl;
	cout << "========================================" << endl;


	// Write the encrypted string out to file "message.aes"
	ofstream outfile;
	outfile.open("message.aes", ios::out | ios::binary);
	if (outfile.is_open())
	{
        // Write raw bytes, not a hex string
		outfile.write((char*)encryptedMessage, paddedMessageLen);
		outfile.close();
		cout << "Wrote encrypted message to file message.aes" << endl;
	}
	else cout << "Unable to open file";

	// Free memory
	delete[] paddedMessage;
	delete[] encryptedMessage;

	return 0;
}