# CryptoSign: Digital Signature & Identity System

A modern, web-based demonstration of **Asymmetric Cryptography** using RSA-2048 and SHA-256. This project provides a full-flow demo of how digital signatures ensure **Authenticity**, **Integrity**, and **Non-repudiation** in digital communications.

## 🌟 Key Features

- **Modern Web UI**: A premium, responsive dashboard built with Bootstrap 5 and Glassmorphism design aesthetics.
- **Identity Management**: Simple registration system to manage multiple users.
- **RSA Key Generation**: Generates industry-standard 2048-bit Private/Public key pairs.
- **Digital Signing**: Implements RSA-PSS (Probabilistic Signature Scheme) padding with SHA-256 for secure message signing.
- **Verification Engine**: Real-time verification of signatures against public keys and time-based expiration (60-second validity).
- **Interactive System Log**: A live technical feed showing background cryptographic operations.

## 🛠️ Technology Stack

- **Backend**: Python 3.x, Flask (Web Framework)
- **Security**: Pyca/Cryptography (Hardened crypto primitives)
- **Frontend**: HTML5, Vanilla CSS, Bootstrap 5, Bootstrap Icons
- **Typography**: Google Fonts (Outfit)

## 🔄 The 4-Step Process

1.  **Identity Registration**: Users register a unique username to enter the ecosystem.
2.  **RSA Key Generation**: The system creates a 2048-bit RSA key pair.
    -   **Private Key**: Kept secret by the user (stored in `keys/`).
    -   **Public Key**: Shared with others (stored in `keys/`).
3.  **Message Signing**: 
    -   A message is combined with a username and timestamp.
    -   The system hashes this string using **SHA-256**.
    -   The hash is encrypted (signed) using the **Private Key**.
4.  **Signature Verification**:
    -   The verifier uses the user's **Public Key** to decrypt the signature.
    -   The system ensures the message matches the signature and hasn't expired.

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Installation
1. Clone the repository and navigate to the project folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Demo
Start the Flask server:
```bash
python app.py
```
Open your browser and navigate to:
[**http://127.0.0.1:5000**](http://127.0.0.1:5000)

## 📂 Project Structure

```text
├── app.py              # Main Flask application & API logic
├── templates/
│   └── index.html      # Modern dashboard UI
├── keys/               # Storage for generated RSA PEM keys
├── users.json          # Persistent registry of users
├── signature.bin       # Last generated binary signature
├── message.txt         # Last signed message (formatted)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## ⚠️ Security Note
This project is designed for **educational and demonstration purposes**. While it uses strong cryptographic primitives (`RSA-PSS`, `SHA-256`), it stores private keys locally in plain text (PEM) for ease of demonstration. In a production environment, private keys should be stored in secure modules (HSMs) or encrypted with a strong passphrase.
