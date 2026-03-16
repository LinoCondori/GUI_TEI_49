import pandas as pd
from glob import glob
from glob import iglob
import os
from sqlalchemy import create_engine
from time import time

#from __main__ import __file__ as nameMain

def buscarEnBaseDeDatos(engine, Tabla, inicio, fin):
    try:
        consulta = 'Select * from "' + Tabla + '" where "time_stamp" >= \'' + inicio._repr_base + '\' and "time_stamp" < \'' + fin._repr_base + '\' order by "time_stamp"'
        print(consulta)
        df_aux = pd.read_sql_query(consulta, con=engine)
        df_aux.DateTime = pd.to_datetime(df_aux.DateTime)
        df_aux.set_index(['time_stamp'], inplace=True)
        df_aux['DateTime'] = df_aux.index
        df_aux.index.name = 'DateTime'
        # df_aux.rename({'TambC': 'TempA', 'Hr': 'HR', 'PrhPa': 'Pres', 'VdGrad': 'Dir'}, axis=1, inplace=True)
    except:
        print("No se pudo Obtener Datos de " + inicio._repr_base)
        df_aux = pd.DataFrame()
    # print(df_aux)
    return df_aux
