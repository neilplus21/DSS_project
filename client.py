import socket
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed

def load_private_key(path):
    try:
        with open(path, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)
    except Exception as e:
        print(f"[Client] Failed to load private key: {e}")
        return None

def load_public_key(path):
    try:
        with open(path, "rb") as f:
            return serialization.load_pem_public_key(f.read())
    except Exception as e:
        print(f"[Client] Failed to load public key: {e}")
        return None

def client():
    host = 'localhost'
    port = 9999

    try:
        client_socket = socket.socket()
        client_socket.connect((host, port))

        message = b"Hello Server! This is a signed message."
        
        hacker_message = b"hacked!"
        #sign
        private_key = load_private_key("dsa_client_private_key.pem")
        if private_key is None:
            return

        hasher = hashes.Hash(hashes.SHA256())
        hasher.update(message)
        digest = hasher.finalize()

        signature = private_key.sign(digest, Prehashed(hashes.SHA256()))
        client_socket.sendall(message)
        #client_socket.sendall(hacker_message)
        client_socket.sendall(signature)

        client_socket.sendall(signature)
        print("[Client] Sent message and signature to server.")

        reply = client_socket.recv(1024)
        server_signature = client_socket.recv(1024)

        server_pub = load_public_key("dsa_server_public_key.pem")
        if server_pub is None:
            return

        hasher = hashes.Hash(hashes.SHA256())
        hasher.update(reply)
        digest_reply = hasher.finalize()

        server_pub.verify(server_signature, digest_reply, Prehashed(hashes.SHA256()))
        print("[Client] ✅ Server signature verified.")

    except Exception as e:
        print(f"[Client] Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    client()
