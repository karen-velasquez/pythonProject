'''import cv2
from datetime import datetime

# the duration (in seconds)
duration = 5
cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
print(cv2.CAP_DSHOW)
print(cap)
qu = 0
while True:

    ret, frame = cap.read()
    start_time = datetime.now()
    diff = (datetime.now() - start_time).seconds  # converting into seconds
    while (diff <= duration):
        ret, frame = cap.read()
        cv2.putText(frame, str(diff), (70, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                    cv2.LINE_AA)  # adding timer text
        cv2.imshow('frame', frame)
        diff = (datetime.now() - start_time).seconds

        k = cv2.waitKey(10)
        if k & 0xFF == ord("r"):  # reset the timer
            break
        if k & 0xFF == ord("q"):  # quit all
            qu = 1
            break

    if qu == 1:
        break

cap.release()
cv2.destroyAllWindows()
'''

from tkinter import *
import matplotlib
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import mplcyberpunk
import numpy as np
matplotlib.style.use("cyberpunk")

import pandas as pd
import matplotlib.pyplot as plt



'''    AQUI COMENZAMOS EL PEDIDO HACIA EL STRING BOOT    '''
import requests  #Importamos la librería requests
token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkaWVnbyIsImV4cCI6MTY3MDMyMDE2OCwiaWF0IjoxNjcwMjg0MTY4fQ.LkfSC1p2FQErLS0x1924w8N9jjcNt7_06M642YBxhyQ'
endpoint = 'http://localhost:5000/'

headers = {"Authorization": "Bearer " +str(token)}

'''----------------------------------------------- EL REQUEST ---------------------------------------------'''
usuarioNombre = 'james'

# creando el request
requestAsignado = requests.get(str(endpoint) + "asignado/codigo/"+str(usuarioNombre), headers=headers)
# obteniendo la data
dataAsignado = requestAsignado.json()
if (requestAsignado.status_code == 200):
    # Obteniendo el data del request
    print('----------dataAsignado--------')
    print(dataAsignado)
else:
    if (requestAsignado.status_code == 500):
        print('Hubo un error al pedir los datos')
    else:
        if (requestAsignado.status_code == 0):
            print('No hay conexion con el servidor')
'''----------------------------------------------- EL REQUEST ---------------------------------------------'''



'''    FINALIZA: AQUI COMENZAMOS EL PEDIDO HACIA EL STRING BOOT    '''

df = pd.read_json(json.dumps(dataAsignado), orient='records')
df.columns = ['CodigoAsignado', 'Nombre']

#Legends que se pondran en el grafico
legendsNames = []  # Opción 1

for i in range(len(df)):
    print(df.iloc[i]['CodigoAsignado'])
    '''----------------------------------------------- EL REQUEST ---------------------------------------------'''
    # creando el request
    requestCodigoAsignado = requests.get(str(endpoint) + "cumplimiento/"+str(usuarioNombre)+"/"+str(df.iloc[i]['CodigoAsignado']), headers=headers)
    # obteniendo la data
    dataCodigoAsignado = requestCodigoAsignado.json()
    if (requestCodigoAsignado.status_code == 200 and len(dataCodigoAsignado)>0):
        # Obteniendo el data del request
        print(dataCodigoAsignado)
        print(type(dataCodigoAsignado))
        '''----------------------------------------------- EL REQUEST ---------------------------------------------'''
        df2 = pd.read_json(json.dumps(dataCodigoAsignado), orient='records')
        df2.columns = ['fechaCumplimiento', 'aciertos']
        df2['fechaCumplimiento'] = pd.to_datetime(df2['fechaCumplimiento'], format='%d-%m-%Y')
        # Convirtiendo la fila a float
        df2 = df2.astype({'aciertos': 'float'})
        # Ordenando los valores segun la fecha
        df2 = df2.sort_values(by='fechaCumplimiento', ascending=True)
        plt.plot(df2['fechaCumplimiento'], df2['aciertos'], marker='o')
        legendsNames.append(df.iloc[i]['Nombre'])
        print('Hola entre una vez')
        print(df2)
    else:
        if (requestCodigoAsignado.status_code == 500):
            print('Hubo un error al pedir los datos')
        else:
            if (requestCodigoAsignado.status_code == 0):
                print('No hay conexion con el servidor')


plt.legend(legendsNames)
plt.show()







