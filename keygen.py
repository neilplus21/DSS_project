from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization

def generate_keys(role):
    private_key = dsa.generate_private_key(key_size=2048)
    public_key = private_key.public_key()

    with open(f"dsa_{role}_private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()
        ))

    with open(f"dsa_{role}_public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print(f"{role.capitalize()} DSA Keys Generated.")

if __name__ == "__main__":
    generate_keys("client")
    generate_keys("server")
