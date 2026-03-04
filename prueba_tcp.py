import socket
import threading

HOST = "192.168.1.50"  # IP del servidor
PORT = 9881  # Puerto


def recibir(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\nServidor cerró la conexión.")
                break
            print("\nRespuesta:", data.decode())
        except:
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Conectado a {HOST}:{PORT}")

    # Hilo para recibir datos sin bloquear input
    threading.Thread(target=recibir, args=(s,), daemon=True).start()

    while True:
        mensaje = input("Enviar: ")
        if mensaje.lower() == "exit":
            break
        s.sendall((mensaje + "\n").encode())