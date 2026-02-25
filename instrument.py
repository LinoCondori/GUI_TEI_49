# instrument.py
import threading
import random
import time

class Instrument:
    def __init__(self, name, port, instrument_id):
        self.name = name
        self.port = port
        self.instrument_id = instrument_id
        self.enable = False
        self.value = None
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _loop(self):
        while self.running:
            self.value = self.read_value()
            time.sleep(2)

    def read_value(self):
        # Simulación de lectura
        return round(random.uniform(0, 100), 2)

        #self.last_value = round(random.uniform(0, 100), 2)
        #self.last_update = time.strftime("%Y-%m-%d %H:%M:%S")
        #return self.last_value
