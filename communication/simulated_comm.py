import random
import time
from .base_comm import BaseCommunication

class SimulatedCommunication(BaseCommunication):

    def __init__(self, name="Sim", port="SIM",):
        self.name = name
        self.port = port
        self.running = False

    def connect(self):
        self.running = True
        return True

    def read(self):
        time.sleep(1)
        data1 = round(random.uniform(0, 100), 2)
        data2 = round(random.uniform(0, 100), 2)
        dataString = ["adfsadf", "adfyuoi", "yeryuoi", "mbnvvbn"]
        dataString = dataString[random.randint(0, 3)]
        return f"{data1},{data2},{dataString}"



    def close(self):
        self.running = False