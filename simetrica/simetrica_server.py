import socket
from cryptography.fernet import Fernet
from datetime import datetime

def descrifrar_content(contenido, clave):
    fernet = Fernet(clave)
    return fernet.decrypt(contenido)


def recibir_clave():
    host = '127.0.0.1'
    port = 4444

    try:
        # Crear el socket
        recieve_key = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recieve_key.bind((host, port))
        recieve_key.listen(1)
        print("Servidor esperando clave en el puerto 4444...")

        conn, addr = recieve_key.accept()
        print(f"Conexión establecida con {addr}")

        # Recibir la clave
        clave = conn.recv(1024)
        print(f"Clave recibida: {clave.decode()}")

        # (Opcional) Enviar confirmación al cliente
        conn.sendall(b"Clave recibida correctamente.")

    except Exception as e:
        print(f"Error en recibir_clave: {e}")
        clave = None

    finally:
        # Cerrar conexiones
        if 'conn' in locals():
            conn.close()
        recieve_key.close()

    return clave


def server():
	clave = recibir_clave()

	host='127.0.0.1'
	port = 3333
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((host, port))
	server.listen(1)
	print("Server corriendo, esperando conexion")
	
	conn, addr =server.accept()
	print(f"Conexion establecida con {addr}")

	contenido = conn.recv(16384)
	print("Contenido cifrado recibido")
	
	fecha = datetime.now()
	fecha_hora = fecha.strftime("%Y-%m-%d %H:%M:%S")

	contenido_des = descrifrar_content(contenido,clave)
	print(f"Contenido descifrado: {contenido_des.decode('utf-8')}")
	with open(f"{fecha_hora}.txt", "wb") as file:
		file.write(contenido_des)
	print(f"Archivo descrfrado y guardado como {fecha_hora}.txt")
	
	conn.close()
	server.close()

if __name__ == "__main__":
	server()
