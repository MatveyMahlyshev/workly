import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


def main():
    certs_dir = "certs"
    os.makedirs(certs_dir, exist_ok=True)

    private_key_path = os.path.join(certs_dir, "jwt-private.pem")
    public_key_path = os.path.join(certs_dir, "jwt-public.pem")

    if os.path.exists(private_key_path) and os.path.exists(public_key_path):
        return

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )

    with open(private_key_path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    public_key = private_key.public_key()
    with open(public_key_path, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


if __name__ == "__main__":
    main()
