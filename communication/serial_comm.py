import serial
from .base_comm import BaseCommunication


class SerialCommunication(BaseCommunication):

    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.conn = None

    def connect(self):
        self.conn = serial.Serial(self.port, self.baudrate)

    def read(self):
        return self.conn.readline().decode().strip()

    def close(self):
        if self.conn:
            self.conn.close()