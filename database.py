import pandas as pd
import numpy as np
from glob import glob
import os
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import BaseDeDatos_Lib_v04 as BD


engine = create_engine('postgresql://postgres:vag@10.30.19.5:5432/GAWUSH_DATABASE')
Tabla_Data = 'O3_SN_0330102717'
Tabla_Coef = 'O3_SN_0330102717_Coeficientes'
Tabla_Zero = 'O3_Calibraciones'
inicio = pd.to_datetime('2025-01-01 00:00')
fin = pd.to_datetime('2026-01-01 00:00')

import socket

ip = "192.168.1.50"
port = 3306

s = socket.socket()
s.connect((ip, port))

data = s.recv(1024)
print(data)

s.close()