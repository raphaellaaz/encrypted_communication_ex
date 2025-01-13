def server():
    import socket
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import serialization, hashes

    HOST = '127.0.0.1'
    PORT = 6543
    RECEIVED_FILE = 'received_file.txt'

    def generate_keys():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def serialize_public_key(public_key):
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def decrypt_data(encrypted_data, private_key):
        return private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    private_key, public_key = generate_keys()
    serialized_public_key = serialize_public_key(public_key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Server is listening...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connection established with {addr}")

            # Send public key to client
            conn.sendall(serialized_public_key)

            # Receive encrypted data
            encrypted_data = conn.recv(4096)
            print("Encrypted data received.")

            # Decrypt the data
            decrypted_data = decrypt_data(encrypted_data, private_key)

            # Write to a file
            with open(RECEIVED_FILE, 'wb') as f:
                f.write(decrypted_data)
            print(f"File received and saved as {RECEIVED_FILE}")

            print(decrypted_data.decode())

if __name__ == "__main__":
    server()
