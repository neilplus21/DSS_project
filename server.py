import socket
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed

def load_private_key(path):
    try:
        with open(path, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)
    except Exception as e:
        print(f"[Server] Failed to load private key: {e}")
        return None

def load_public_key(path):
    try:
        with open(path, "rb") as f:
            return serialization.load_pem_public_key(f.read())
    except Exception as e:
        print(f"[Server] Failed to load public key: {e}")
        return None

def server():
    host = 'localhost'
    port = 9999

    try:
        server_socket = socket.socket()
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"[Server] Listening on {host}:{port}...")

        conn, addr = server_socket.accept()
        print(f"[Server] Connection from {addr}")

        message = conn.recv(1024)
        signature = conn.recv(1024)

        client_pub = load_public_key("dsa_client_public_key.pem")
        if client_pub is None:
            conn.close()
            return

        hasher = hashes.Hash(hashes.SHA256())
        hasher.update(message)
        digest = hasher.finalize()

        try:
            client_pub.verify(signature, digest, Prehashed(hashes.SHA256()))
            print("[Server] ✅ Client signature verified.")
        except Exception as e:
            print(f"[Server] ❌ Invalid signature: {e}")

        #reply
        reply = b"Message received and verified!"
        server_priv = load_private_key("dsa_server_private_key.pem")
        if server_priv is None:
            conn.close()
            return

        hasher = hashes.Hash(hashes.SHA256())
        hasher.update(reply)
        digest_reply = hasher.finalize()

        server_signature = server_priv.sign(digest_reply, Prehashed(hashes.SHA256()))
        conn.sendall(reply)
        conn.sendall(server_signature)
        print("[Server] Sent reply and signature to client.")

    except Exception as e:
        print(f"[Server] Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    server()
