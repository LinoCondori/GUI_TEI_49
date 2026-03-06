import socket
import threading

HOST = "192.168.1.50"  # IP del servidor
PORT = 9882  # Puerto

STX = chr(0x02)
SP = chr(0x20)
ST_ID = "ST001"
ETX = chr(0x03)


def calculate_bcc(data_bytes):
    """
    Calculates the Block Check Character (BCC) for a sequence of bytes.

    BCC is commonly calculated as the XOR of all bytes in the data block.
    The exact range of bytes included (e.g., excluding STX/SOH, including ETX)
    depends on the specific protocol definition.
    """
    bcc = 0
    for byte in data_bytes:
        bcc ^= byte
    return chr(bcc)


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

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Conectado a {HOST}:{PORT}")

        # Hilo para recibir datos sin bloquear input
        threading.Thread(target=recibir, args=(s,), daemon=True).start()

        while True:
            entrada =  input("Enviar: ")
            if entrada.lower() == "exit":
                break
            mensaje = (STX + ST_ID + SP + entrada + ETX)
            mensaje = mensaje + calculate_bcc(mensaje.encode())
            print(mensaje)
            s.sendall( (mensaje.encode()))