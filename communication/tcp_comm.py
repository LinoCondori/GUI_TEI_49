import socket
from .base_comm import BaseCommunication
import time

header = "time date Alerts Analog_Alarms Analog_Input_1 Analog_Input_2 Analog_Input_3 Analog_Input_4 Averaging_Time_(sec) Bench_Temp_Alarm Bench_Temp_Alarm_Status Calculated_Flow_A_(L/min) Cell_A_Noise_(Hz) Cell_A_Photometer_Frequency_(Hz) Cell_A_Reference_Frequency_(Hz) Cell_A_Sample_Frequency_(Hz) Cell_B_Noise_(Hz) Cell_B_Photometer_Frequency_(Hz) Cell_B_Reference_Frequency_(Hz) Cell_B_Sample_Frequency_(Hz) Concentration_(ppb_or_ug/m3) DF_High_Range_Enable DF_Low_Range_Enable Ethernet_Configuration_Alarm Ethernet_DNS_Configuration_Alarm Ethernet_Gateway_Configuration_Alarm Ethernet_IP_Address_Configuration_Alarm Ethernet_Subnet_Mask_Configuration_Alarm External_Alarm_1 External_Alarm_2 External_Alarm_3 General_Alarm High_Averaging_Time_(sec) High_Concentration_(ppb_or_ug/m3) High_Span_Coefficient Instrument_Error_ Ozonator_Level_1_Check_Alarm Ozonator_Level_2_Check_Alarm Ozonator_Level_3_Check_Alarm Ozonator_Level_4_Check_Alarm Ozonator_Level_5_Check_Alarm Ozonator_Level_6_Check_Alarm PSB_Alarms Photometer_Background_(ppb_or_ug/m3) Photometer_Bench_Temperature_(Deg._C) Photometer_Flow_A_Alarm_Status Photometer_Heater_Current_(A) Photometer_Lamp_Temperature_(Deg._C) Photometer_Pressure_A_(mmHg) Photometer_Pressure_A_Alarm Selected_Gas_Mode Span_Check_Alarm Span_Coefficient Zero_Check_Alarm"

header = "time date Alerts Analog_Alarms Analog_Input_1 Analog_Input_2 Analog_Input_3 Analog_Input_4 Averaging_Time_(sec) Bench_Temp_Alarm Bench_Temp_Alarm_Status Calculated_Flow_A_(L/min) Cell_A_Noise_(Hz) Cell_A_Photometer_Frequency_(Hz) Cell_A_Reference_Frequency_(Hz) Cell_A_Sample_Frequency_(Hz) Cell_B_Noise_(Hz) Cell_B_Photometer_Frequency_(Hz) Cell_B_Reference_Frequency_(Hz) Cell_B_Sample_Frequency_(Hz) Concentration_(ppb_or_ug/m3) DF_High_Range_Enable DF_Low_Range_Enable Ethernet_Configuration_Alarm Ethernet_DNS_Configuration_Alarm Ethernet_Gateway_Configuration_Alarm Ethernet_IP_Address_Configuration_Alarm Ethernet_Subnet_Mask_Configuration_Alarm External_Alarm_1 External_Alarm_2 External_Alarm_3 General_Alarm High_Averaging_Time_(sec) High_Concentration_(ppb_or_ug/m3) High_Span_Coefficient Instrument_Error_ Ozonator_Level_1_Check_Alarm Ozonator_Level_2_Check_Alarm Ozonator_Level_3_Check_Alarm Ozonator_Level_4_Check_Alarm Ozonator_Level_5_Check_Alarm Ozonator_Level_6_Check_Alarm PSB_Alarms Photometer_Background_(ppb_or_ug/m3) Photometer_Bench_Temperature_(Deg._C) Photometer_Flow_A_Alarm_Status Photometer_Heater_Current_(A) Photometer_Lamp_Temperature_(Deg._C) Photometer_Pressure_A_(mmHg) Photometer_Pressure_A_Alarm Selected_Gas_Mode Span_Check_Alarm Span_Coefficient Zero_Check_Alarm"
class TCPCommunication(BaseCommunication):

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.sock = None
        self.connected = False

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)
            self.sock.connect((self.host, self.port))
            self.connected = True
            print("Conectado")
            return True

        except Exception as e:
            print("Error conectando:", e)
            self.connected = False
            return False

    def read(self):
        try:
            data = self.sock.recv(4096)
            if not data:
                print("Conexión cerrada por el servidor")
                self.connected = False
                return None
            print(data)
            print(type(data))
            return data

        except Exception as e:
            print("Error leyendo:", e)
            self.connected = False
            return None


    def close(self):
        if self.sock:
            self.sock.close()
            self.connected = False
