# instrument.py
import threading
import random
import time
import os
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


class Instrument:
    def __init__(self, name, port, instrument_id):
        self.name = name
        self.port = port
        self.instrument_id = instrument_id
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
        data1= round(random.uniform(0, 100), 2)
        self.save_data(data1, round(random.uniform(0, 100), 2))
        return data1


    def save_data(self, data1, data2):
        now = datetime.now()

        year = now.strftime("%Y")
        date_str = now.strftime("%Y-%m-%d")
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        base_path = os.path.join("data", self.name, "crudo", year)
        os.makedirs(base_path, exist_ok=True)

        file_path = os.path.join(base_path, f"{date_str}.csv")

        file_exists = os.path.isfile(file_path)

        with open(file_path, "a") as f:
            if not file_exists:
                f.write("FechaHora,dato1,dato2\n")

            f.write(f"{timestamp},{data1},{data2}\n")

    def load_data_from_file(self, file):

        try:
            df = pd.read_csv(file, parse_dates=["FechaHora"])
        except:
            df = pd.DataFrame()
        return df
