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
        self.auto_recover = True

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

        recover = self.detect_recover()
        if recover:
            #cruzar datos en el archivo principal.
            self.read_recover_to_minute(recover)


    def stop(self):
        self.running = False

    def _loop(self):

        while self.running:

            if not self.communication.connected:
                if not self.communication.connect():
                    time.sleep(5)
                    continue

            data = self.communication.read()

            if self.communication.type == 'tcp':
                if data:
                    if self.communication.header == data:
                        print("se detecto encabezado")# self.read_value()
                        continue
                    self.value = data
                    self.save_data(self.value)
                else:
                    print("Reconectando...")
                    self.communication.close()
                    time.sleep(5)

            if self.communication.type == 'serial':
                if data:
                    self.value = data
                    self.save_data(self.value)
                else:
                    print("Sin Datos...")
                    #self.communication.close()
                    #time.sleep(5)


    def read_value(self):
        # Ya no se usa
        pass


    def save_data(self, data1, data2="", dataString=" "):
        #Generar PATH
        #now = datetime.now()
        #year = now.strftime("%Y")
        #date_str = now.strftime("%Y-%m-%d")
        #timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        #base_path = os.path.join("data", self.name, "crudo", year)
        #os.makedirs(base_path, exist_ok=True)

        file_path, timestamp = self.generate_path(datetime.now(), "crudo")
        file_exists = os.path.isfile(file_path)
        #print(self.communication.port)
        ### GUARDAR

        if self.communication.type == "serial":
            with open(file_path, "a") as f:
                if not file_exists:
                    f.write("FechaHora, trama de datos \n")

                f.write(f"{timestamp},{data1}\n")

        if self.communication.type == "tcp": #"." in self.communication.host:  # IP if hasattr(self.communication, 'host'):
            with open(file_path, "a") as f:
                if not file_exists:
                    f.write(f"FechaHora,{self.communication.header.replace(" ", ",")}")
                f.write(f"{timestamp},{data1.replace("\r", "").replace(" ", ",")}")
        if self.communication.type == "simulated":
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
        df = df.drop(columns=["FechaHora"])
        #df["FechaHora"] = df.index
        df_num = df.select_dtypes(include='number')
        df_Tmin = df_num.resample('min', label='left').mean()
        df_No_num = df.select_dtypes(exclude='number')
        df_NO_min = df_No_num.resample('min').agg(minute_mode)
        #df_Tmin.index.name = "FechaHora"
        return pd.concat([df_Tmin.round(3),df_NO_min], axis=1)

    def update_avg_file(self, df_nuevo, path):

        if not isinstance(df_nuevo.index, pd.DatetimeIndex):
            df_nuevo.set_index(df_nuevo["FechaHora"], inplace=True)
        if "FechaHora" not in df_nuevo.columns:
            df_nuevo["FechaHora"] = df_nuevo.index

        if os.path.exists(path):
            df_actual = pd.read_csv(path)
            df_actual["FechaHora"] = pd.to_datetime(df_actual["FechaHora"])
            df_actual.set_index(df_actual["FechaHora"], inplace=True)
            df_actual = df_actual[~df_actual.index.duplicated(keep="first")]
        else:
            df_actual = pd.DataFrame(columns=df_nuevo.columns)

        resultado = df_actual.reindex(df_actual.index.union(df_nuevo.index))
        resultado.update(df_nuevo)

        resultado.to_csv(path, index=False)

    def get_last_local_timestamp(self):
        # el dia de hoy
        file_path, timestamp = self.generate_path(datetime.now(), "")
        if os.path.isfile(file_path):
            file = pd.read_csv(file_path)
            return file["FechaHora"].iloc[-1]
        # el dia de ayer
        file_path, timestamp = self.generate_path(datetime.now() - timedelta(days=1), "")
        if os.path.isfile(file_path):
            file = pd.read_csv(file_path)
            return file["FechaHora"].iloc[-1]

        # el dia de antes de ayer
        file_path, timestamp = self.generate_path(datetime.now() - timedelta(days=2), "")
        if os.path.isfile(file_path):
            file = pd.read_csv(file_path)
            return file["FechaHora"].iloc[-1]

        # mucho atras
        file_path, timestamp = self.generate_path(datetime.now() - timedelta(days=5), "")
        if os.path.isfile(file_path):
            file = pd.read_csv(file_path)
            return file["FechaHora"].iloc[-1]

        return False

    def detect_recover(self):
        # se tiene que evaluar que dos cosas pasen.
        # que haya entre un maximo y un minimo de faltantes de datos
        # por ejemplo hasta 1 dia de faltantes
        # y dos minutos de datos.
        # La otro condicion es que este habilitado la recuperacion automatica.

        # recuperar ultimo dato en archivo
        ultima_fecha = self.get_last_local_timestamp()
        # comparar hora de la compu.
        now =  pd.to_datetime("now", utc=True)
        if ultima_fecha:
            diff = now - pd.to_datetime(ultima_fecha, utc=True)
            if pd.to_timedelta(2, unit="minutes") < diff < pd.to_timedelta(150, unit="hour") :
                print("buscar datos")
                path, nada = self.generate_path(now, "crudo")
                path = path.replace("crudo","recover").replace(now.strftime("%Y-%m-%d"),
                                                               now.strftime("%Y-%m-%d_%H_%M_%S"))
                self.communication.recover_data(ultima_fecha, now, path)
                return path
            return False
        print("No se busco datos")
        return False


    def inst_recover_data(self, start, end):
            self.communication.recover_data(start, end)

    def generate_path(self, day=datetime.now(), folder="crudo" ):
        now = day
        year = now.strftime("%Y")
        date_str = now.strftime("%Y-%m-%d")
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        if folder:
            base_path = os.path.join("data", self.name, folder, year)
        else:
            base_path = os.path.join("data", self.name, year)
        os.makedirs(base_path, exist_ok=True)

        return  os.path.join(base_path, f"{date_str}.csv"), timestamp
        #file_exists = os.path.isfile(file_path)

    def read_recover_to_minute(self, path):
        if self.communication.type == "tcp":
            # cruzar datos
            df_recover = pd.read_csv(path)
            df_recover.rename(columns={"tmoPhotometerO3SWConcentrationBUR_1": "Concentration_(ppb_or_ug/m3)",
                                       "tmoPhotometerO3HWLampTemperatureR_0": "Photometer_Lamp_Temperature_(Deg._C)",
                                       "tmoPhotometerO3HWDetectorAFrequencyR_0": "Cell_A_Photometer_Frequency_(Hz)",
                                       "tmoPhotometerO3HWDetectorBFrequencyR_0": "Cell_B_Photometer_Frequency_(Hz)",
                                       "tmoPhotometerO3SWFlowPressHWPSensor2R_0": "Photometer_Pressure_A_(mmHg)",
                                       "tmoPhotometerO3SWFlowPressSWCalculatedFlow1W_0": "Calculated_Flow_A_(L/min)",
                                       "tmoPhotometerO3SWSpanCoefficientRW_1": "Span_Coefficient",
                                       "tmoPhotometerO3HWBenchTemperatureR_0": "Photometer_Bench_Temperature_(Deg._C)",
                                       "tmoPhotometerO3SWBackgroundBURW_0": "Photometer_Background_(ppb_or_ug/m3)",
                                       "tmoPhotometerO3SWGasModeR_0": "Selected_Gas_Mode",
                                       "tmoPhotometerO3SWAvgTimeRW_1": "Averaging_Time_(sec)",
                                       "tmoAnalogIOHWAlarmCountW_0": "Analog_Alarms",
                                       "tmoCommonRegsWarningsActive_0": "General_Alarm",
                                       "tmoCommonRegsInstrumentError_0": "Instrument_Error_",
                                       }, inplace=True)
            df_recover["date"] = pd.to_datetime(df_recover.time_stamp).dt.strftime("%Y-%m-%d")
            df_recover["time"] = pd.to_datetime(df_recover.time_stamp).dt.strftime("%H-%M-%S")

            # Separar en dias, para cargar en los archivos correspondientes.
            for dias in pd.date_range(pd.to_datetime(df_recover.time_stamp).min().floor('D'),
                                      pd.to_datetime(df_recover.time_stamp).max().floor('D'), freq="D", ):
                path_dias, nada = self.generate_path(dias, "")

                df_dia_recuperado = df_recover.loc[df_recover.date == dias.strftime("%Y-%m-%d")]
                df_dia_recuperado.set_index(df_dia_recuperado["time_stamp"], inplace=True)
                df_dia_recuperado.rename(columns={"time_stamp": "FechaHora"}, inplace=True)

                if os.path.exists(path_dias):
                    df_almacenado = pd.read_csv(path_dias)
                    df_almacenado.set_index(df_almacenado["FechaHora"], inplace=True)
                    df_almacenado = df_almacenado[~df_almacenado.index.duplicated(keep="first")]
                else:
                    df_almacenado = pd.DataFrame(columns=df_dia_recuperado.columns)

                resultado = df_almacenado.reindex(df_almacenado.index.union(df_dia_recuperado.index))
                resultado.update(df_dia_recuperado)

                self.update_avg_file(resultado, path_dias)
                #resultado.to_csv(path_dias, index=False)

            return True
        return False