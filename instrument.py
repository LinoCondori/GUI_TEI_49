# instrument.py
import threading
import random
import time
import os
import pandas as pd
from datetime import datetime, timedelta

import serial

def minute_mode(x):
    m = x.mode()
    if len(m) == 0:
        return None
    return m.iloc[0]




class Instrument:
    def __init__(self, name, port=None, instrument_id=None, communication=None):
        self.name = name
        self.communication = communication
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
        self.communication.connect()
        while self.running:
            if not self.communication.connect():
                print("Reintentando en 5 segundos...")
                time.sleep(5)
                continue
            data = self.communication.read()
            self.value= data # self.read_value()
            self.save_data(self.value)
        self.communication.close()


    def read_value(self):
        # Ya no se usa
        data1= round(random.uniform(0, 100), 2)
        dataString = ["adfsadf", "adfyuoi", "yeryuoi", "mbnvvbn"]
        self.save_data(data1, round(random.uniform(0, 100), 2), dataString[random.randint(0, 3)])
        return data1


    def save_data(self, data1, data2="", dataString=" "):
        now = datetime.now()

        year = now.strftime("%Y")
        date_str = now.strftime("%Y-%m-%d")
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        base_path = os.path.join("data", self.name, "crudo", year)
        os.makedirs(base_path, exist_ok=True)

        file_path = os.path.join(base_path, f"{date_str}.csv")
        file_exists = os.path.isfile(file_path)

        if self.communication.port.startswith("COM"):
            with open(file_path, "a") as f:
                if not file_exists:
                    f.write("FechaHora,dato1,dato2,dataString\n")

                f.write(f"{timestamp},{data1},{data2},{dataString}\n")

        elif "." in self.communication.port:  # IP
            with open(file_path, "a") as f:
                if not file_exists:
                    f.write("FechaHora,dato1,dato2,dataString\n")

                f.write(f"{timestamp},{data1},{data2},{dataString}\n")
        else:
            with open(file_path, "a") as f:
                if not file_exists:
                    f.write("FechaHora,dato1,dato2,dataString\n")

                f.write(f"{timestamp},{data1}\n")




    def load_data_from_file(self, file):

        try:
            df = pd.read_csv(file, parse_dates=["FechaHora"])
        except:
            df = pd.DataFrame()
        return df

    def minute_average(self, file):

        df = self.load_data_from_file(file)
        if df.empty:
            return pd.DataFrame(columns=["FechaHora", "dato1"])
        df.set_index(df["FechaHora"], inplace=True)
        #df["FechaHora"] = df.index
        df_num = df.select_dtypes(include='number')
        df_Tmin = df_num.resample('min', label='left').mean()
        df_No_num = df.select_dtypes(exclude='number')
        df_NO_min = df_No_num.resample('min').agg(minute_mode)

        return pd.concat([df_Tmin.round(3),df_NO_min], axis=1)





