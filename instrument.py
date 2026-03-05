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

header_ps = "time date Concentration_(ppb_or_ug/m3)"


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

        while self.running:

            if not self.communication.connected:
                if not self.communication.connect():
                    time.sleep(5)
                    continue

            data = self.communication.read()


            if data:
                if self.instrument_id == "PS":
                    if self.communication.header == data:
                        print("se detecto encabezado")  # self.read_value()
                        continue
                if self.communication.header == data:
                    print("se detecto encabezado")# self.read_value()
                    continue
                self.value = data
                self.save_data(self.value)
            else:
                print("Reconectando...")
                self.communication.close()
                time.sleep(5)


    def read_value(self):
        # Ya no se usa
        pass


    def save_data(self, data1, data2="", dataString=" "):
        #Generar PATH
        now = datetime.now()
        year = now.strftime("%Y")
        date_str = now.strftime("%Y-%m-%d")
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        base_path = os.path.join("data", self.name, "crudo", year)
        os.makedirs(base_path, exist_ok=True)

        file_path = os.path.join(base_path, f"{date_str}.csv")
        file_exists = os.path.isfile(file_path)
        #print(self.communication.port)
        ### GUARDAR

        if self.communication.port.startswith("COM"):
            with open(file_path, "a") as f:
                if not file_exists:
                    f.write("FechaHora, trama de datos \n")

                f.write(f"{timestamp},{data1}\n")

        elif hasattr(self.communication, 'host'): #"." in self.communication.host:  # IP if hasattr(self.communication, 'host'):
            if self.instrument_id == "PS":

                with open(file_path, "a") as f:
                    if not file_exists:
                        f.write(f"FechaHora,{header_ps.replace(" ", ",")}")
                    f.write(f"{timestamp},{data1.replace("\r", "").replace(" ", ",")}")

            with open(file_path, "a") as f:
                if not file_exists:
                    f.write(f"FechaHora,{self.communication.header.replace(" ", ",")}")
                f.write(f"{timestamp},{data1.replace("\r", "").replace(" ", ",")}")
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





