import serial
from .base_comm import BaseCommunication
import pandas as pd

cmd_Remote = b'Set Mode Remote'
cmd_format = b'set format 01'
cmd_InsName = b'Instr Name'  # no se lo encuentra en ningun lado.
cmd_PrgName = b'Program No'

cmd_time = b'set time'
cmd_date = b'set date'
#
# 'O3', 'Flag', 'CellA', 'CellB', 'BenchTemp', 'LampTemp', 'FlowA', 'FlowB', 'Pres']
cmd_O3 = b'O3'
cmd_Flags = b'flags'
cmd_CellA = b'cell a int'
cmd_CellB = b'cell b int'
cmd_BenchTemp = b'bench temp'
cmd_LampTemp = b'lamp temp'
cmd_FlowA = b'flow a'
cmd_FlowB = b'flow b'
cmd_Pres = b'pres'

cmd_gasMode = b'gas mode'

cmd_SetSample = b'set sample'
cmd_SetZero = b'set zero'
cmd_SetSpan = b'set span'

cmd_Lrec = b'lrec'

FgSamp = int('0000000', 16)
FgZero = int('1000000', 16)
FgSpan = int('2000000', 16)
FgErro = int('3000000', 16)


class SerialCommunication(BaseCommunication):

    type = "serial"

    def __init__(self, port, id):
        self.port = port
        self.baudrate = 9600#baudrate
        self.connected = False
        self.conn = None
        self.ID = id
        self.Test = b'TEST'


    def connect(self):

        try:
            self.conn = serial.Serial(self.port, self.baudrate)
            self.conn.timeout = .15  # .15
            self.conn.open()
            # Testear si està abierto
            self.conn.write(self.Test)
            linea = self.conn.readline()  # vacia el buffer
        except Exception as e:
            print("Error conectando: ", e)
            self.connected = False
            return False

        if self.conn.is_open:
            self.connected = True
            return True

    def read(self):
        col = ['O3', 'Flags', 'CellA', 'CellB', 'BenchTemp', 'LampTemp', 'FlowA', 'FlowB', 'Pres']
        df_aux = pd.DataFrame(columns=col)
        df_aux.index.name = 'DateTime'

        try:
            data = (self.send_command(cmd_O3) + self.send_command(cmd_Flags) + self.send_command(cmd_CellA) +
                    self.send_command(cmd_CellB) +  self.send_command(cmd_BenchTemp) + self.send_command(cmd_LampTemp) +
                    self.send_command(cmd_FlowA) + self.send_command(cmd_FlowB) + self.send_command(cmd_Pres))
        except:
            print("OCURRIO ALGUN PROBLEMA AL TOMAR DATOS")
            data = None
        return data

    def ID_P(self, string):
        if self.ID < 128:
            ID = self.ID + 128
        else:
            ID = self.ID
        return bytes([ID]) + string + b'\r\n'

    def send_command(self, mensaje):
        if self.conn.is_open:
            try:
                mensaje = self.ID_P(mensaje)
                self.conn.write(mensaje)

                respuesta = self.conn.readlines()

                try:
                    if b'lrec' in respuesta[0]:
                        return respuesta[1:11]  # .decode())
                    if b'bad' in respuesta[0]:
                        print("Problemas de envio")
                    return str(respuesta[0].decode())
                except:
                    print(respuesta)
                    return []
            except serial.serialutil.SerialException:
                self.conn.close()
                print("ERROR de Comunicacion-Puerto Desconectado")
                return []
        else:
            return b'ERROR'

        #return self.conn.readline().decode().strip()

    def close(self):

        if self.conn:
            self.conn.close()

    def recover_data(self, start, end):
        ...
