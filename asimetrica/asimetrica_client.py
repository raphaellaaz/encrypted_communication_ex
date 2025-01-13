# Client (Sender)
def client():
    import socket
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import serialization, hashes

    HOST = '127.0.0.1'
    PORT = 6543
    FILE_TO_SEND = 'archivo_encriptado.txt'

    def encrypt_data(data, public_key):
        return public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("Connectado al servidor.")

        # Receive public key from server
        serialized_public_key = client_socket.recv(4096)
        public_key = serialization.load_pem_public_key(serialized_public_key)
        print(f"Llave publica recivida del servidor. {public_key}")

        # Read the file to send
        #with open(FILE_TO_SEND, 'rb') as f:
        #    file_data = f.read()

        print("Ingrese mensaje a encriptar y enviar: ")
        menssaje = input()

        # Encrypt the file data
        encrypted_data = encrypt_data(menssaje.encode(), public_key)
        print(f"Message encriptado. {encrypted_data}")

        # Send encrypted data
        client_socket.sendall(encrypted_data)
        print("Message encriptado enviado")

if __name__ == "__main__":
    client()
