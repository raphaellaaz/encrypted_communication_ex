import socket
from cryptography.fernet import Fernet

# Función para generar una clave simétrica
def generar_clave():
    return Fernet.generate_key()

# Función para cifrar un archivo
def cifrar_archivo(contenido, clave):
    fernet = Fernet(clave)
    contenido_cifrado = fernet.encrypt(contenido.encode())
    return contenido_cifrado


def envia_clave(clave):
    host = '127.0.0.1'
    puerto = 4444

    try:
        # Crear el socket
        send_key = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_key.connect((host, puerto))

        # Enviar la clave
        send_key.sendall(clave)
        print("Clave enviada.")

        # (Opcional) Esperar confirmación del servidor
        confirmacion = send_key.recv(1024)
        print(f"Confirmación del servidor: {confirmacion.decode()}")

    except Exception as e:
        print(f"Error en envia_clave: {e}")

    finally:
        # Cerrar el socket
        send_key.close()


# Configuración del cliente
def cliente_simetrico():
      # Genera una clave simétrica
    clave = generar_clave()
    print(f"Clave generada: {clave.decode()}")
    envia_clave(clave)

    host = '127.0.0.1'  # Dirección IP del servidor
    puerto = 3333      # Puerto del servidor

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, puerto))
    print("Conectado")

    # Cifra el archivo
    print("Mensaje a cifrar y enviar: ")
    mensaje = input()
    archivo_cifrado = cifrar_archivo(mensaje, clave)

    with open("mensaje_enviar", "wb") as archivo:
        archivo.write(archivo_cifrado)

    # Envía el archivo cifrado
    cliente.sendall(archivo_cifrado)
    print("Archivo cifrado enviado.")

    cliente.close()

if __name__ == "__main__":
    cliente_simetrico()
