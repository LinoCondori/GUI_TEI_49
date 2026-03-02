import socket
from .base_comm import BaseCommunication

class TCPCommunication(BaseCommunication):

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def read(self):
        comando = 'o3'
        self.sock.send(comando.encode('utf-8'))
        data = self.sock.recv(1024)
        print(data)
        return data.decode().strip()

    def close(self):
        if self.sock:
            self.sock.close()
