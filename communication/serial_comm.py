import serial
from .base_comm import BaseCommunication

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