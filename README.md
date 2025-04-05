# 🔐 DSS - Digital Signature Standard Project (TrustSign)

TrustSign is a secure messaging application that uses the **Digital Signature Standard (DSS)** for authenticating messages between a client and a server. It ensures message integrity and authenticity through public-key cryptography.

## ✨ Features

- Digital Signature creation using DSA private key
- Message verification using DSA public key
- Tamper detection and integrity check
- Secure communication via sockets (TCP)
- Detailed error handling and verification feedback

---

## 🧠 How It Works

### 🖊️ Signing Process (Client)
1. Hash the message using **SHA-256**
2. Generate a **DSA signature** using the private key
3. Send the **message** and **signature** to the server

### ✅ Verification Process (Server)
1. Receive the message and signature
2. Hash the received message using **SHA-256**
3. Verify the signature using the client’s **public key**
4. Respond with a signed acknowledgment

---

## 📁 Project Structure

```
TrustSign/
│
├── dsa_client_private_key.pem
├── dsa_client_public_key.pem
├── dsa_server_private_key.pem
├── dsa_server_public_key.pem
├── client.py
├── server.py
├── generate_keys.py
└── README.md
```

---

## 🛠️ Setup Instructions (GitHub Codespaces)

### 1. Open in Codespaces
- Fork or clone this repo
- Click `Code` → `Codespaces` → `Create codespace on main`

### 2. Install Dependencies
Inside the Codespace terminal:

```bash
pip install cryptography
```

### 3. Generate DSA Key Pairs
Run the key generation script (one-time setup):

```bash
python keygen.py
```

This creates 4 keys:

### 4. Run the Server (In Terminal 1)

```bash
python server.py
```

### 5. Run the Client (In Terminal 2)

```bash
python client.py
```

✅ You should see message verification and signed responses.

---

## 🧪 Simulating Tampering

To test tampering detection:

1. In `client.py`, modify the message after signing:
   ```python
   message = b"Original Message"
   signature = client_private_key.sign(message, hashes.SHA256())

   # Tamper with the message
   message = b"Tampered Message"
   ```

2. Run the server and client again. You should see:
   ```
   [Server] ❌ Invalid signature
   ```

---

## 📜 Tech Stack
- Python 3
- `cryptography` library
- Digital Signature Standard (DSS)
- SHA-256 Hashing
- Sockets (TCP)

---

## 📄 License
This project is for educational and research purposes. Use responsibly.

---

## 🙌 Author
Developed with 💡 by Neil Mammen Prakash

