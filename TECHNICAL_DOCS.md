# Technical Documentation: Digital Signature System

This document provides a deep dive into the cryptographic implementation details of the CryptoSign project.

## 🧬 Core Cryptography Primitives

1.  **Asymmetric Encryption (RSA-2048)**:
    -   Used for key generation and digital signing.
    -   Key Size: 2048 bits (Standard for modern security).
    -   Public Exponent: 65537 (Optimal balance between security and performance).
    -   Backend Library: `cryptography.hazmat.primitives.asymmetric.rsa`.

2.  **Hashing (SHA-256)**:
    -   Used to generate a 256-bit unique message digest.
    -   Algorithm: Secure Hash Algorithm 2 (SHA-2).
    -   Purpose: Ensures the integrity of the message (any modification changes the hash).

3.  **Signature Scheme (RSA-PSS)**:
    -   The system uses **Probabilistic Signature Scheme** (PSS) rather than PKCS#1 v1.5.
    -   PSS is a standardized signature scheme with a strong security proof.
    -   Padding: `padding.PSS` with `MGF1` (Mask Generation Function) and salt length `MAX_LENGTH`.

## 🔄 Interaction Workflow

### 1. Key Generation
-   Generates a new RSA private key object.
-   Serializes the Public Key using `SubjectPublicKeyInfo`.
-   Serializes the Private Key using `TraditionalOpenSSL` format (NoEncryption for demo purposes).

### 2. Message Signing Logic
The message is formatted as:
`{username}:{original_message}:{unix_timestamp}`
-   This ensures the signature is unique and tied to a specific user and point in time.
-   The Private Key object calls the `.sign()` method:
    -   Input: Encoded message bytes.
    -   Padding: `PSS(MGF1(SHA256), salt_length=MAX_LENGTH)`.
    -   Algorithm: `SHA256`.

### 3. Verification Logic
The system retrieves the **Public Key** for the specified user and performs:
-   `public_key.verify(signature, message, padding, algorithm)`.
-   The system checks:
    -   If the username in the message matches the user specified for verification.
    -   If the signature matches the message (integrity).
    -   If the timestamp in the message is within **60 seconds** of current system time.

## 📁 Data Storage

-   **`keys/`**: Binary PEM files for RSA keys.
-   **`users.json`**: Flat-file JSON database containing a list of registered usernames.
-   **`signature.bin`**: Raw binary output of the last `.sign()` operation.
-   **`message.txt`**: The raw formatted string bytes used for signing.

## 🔒 Security Best Practices
While this is a demo, we follow these best practices:
-   **Strong Padding**: Using RSA-PSS instead of standard RSA PKCS#1 v1.5.
-   **Consistent Hashing**: SHA-256 is used for both the hash display and the internal signature algorithm.
-   **Time-bound Authentication**: Prevents relay attacks by enforcing a 60-second validity window.
