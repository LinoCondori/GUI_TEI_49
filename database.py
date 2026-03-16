import pandas as pd
import numpy as np
from glob import glob
import os
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import BaseDeDatos_Lib_v04 as BD


engine = create_engine('mysql+pymysql://root:@192.168.1.50:3306/dichot')
Tabla_Data = 'LogEntry'

inicio = pd.to_datetime('2026-03-01 00:00')
fin = pd.to_datetime('2026-03-02 00:00')

import pymysql

import pymysql

conn = pymysql.connect(
    host="192.168.1.50",
    port=3306,
    user="root",
    password=""
)

cursor = conn.cursor()

# seleccionar la base
df = BD.buscarEnBaseDeDatos(engine, Tabla_Data, inicio, fin)
print(df)