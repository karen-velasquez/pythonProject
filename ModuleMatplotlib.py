from tkinter import *
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import mplcyberpunk
import numpy as np
matplotlib.style.use("cyberpunk")

import pandas as pd
import requests  #Importamos la librería requests
import json

#Este es el endpoint donde se realiza la consulta
endpoint = 'http://springbootbackend-env.eba-mmt3kmxg.us-east-1.elasticbeanstalk.com/'


''' ---------------------------------------- ANALIZANDO LA ENTRADA DE DATOS CON MATPLOLIB -----------------------------------------------------------'''

def order_data(json_str):
    #Leyendo los datos que son Json
    df = pd.read_json(json_str, orient='records')
    # Convirtiendo la fila del dataframe en fechas
    df['Duration'] = pd.to_datetime(df['Duration'], format='%Y-%m-%d')
    # Convirtiendo la fila a float
    df = df.astype({'Discount':'float'})
    #Ordenando los valores segun la fecha
    df = df.sort_values(by='Duration',ascending=True)
    column_headers = list(df.columns.values)

    return df

def order_data2():
    json_str = '[{"Fee":"80","Duration":"1-10-2022","Discount":"80"},\
                    {"Fee":"70","Duration":"1-09-2022","Discount":"60"},\
                    {"Fee":"69","Duration":"2-09-2022","Discount":"61.2"},\
                    {"Fee":"70","Duration":"3-09-2022","Discount":"50.0"}, \
                    {"Fee":"90","Duration":"5-10-2022","Discount":"69.9"},\
                    {"Fee":"80","Duration":"6-10-2022","Discount":"85"}, \
                    {"Fee":"80","Duration":"8-02-2023","Discount":"90.2"},\
                    {"Fee":"90","Duration":"11-03-2023","Discount":"61.2"}]'
    #Leyendo los datos que son Json
    df = pd.read_json(json_str, orient='records')
    # Convirtiendo la fila del dataframe en fechas
    df['Duration'] = pd.to_datetime(df['Duration'], format='%Y-%m-%d')
    # Convirtiendo la fila a float
    df = df.astype({'Discount':'float'})
    #Ordenando los valores segun la fecha
    df = df.sort_values(by='Duration',ascending=True)

    column_headers = list(df.columns.values)

    return df


''' -------------------------------------------- FINALIZA:  ANALIZANDO LA ENTRADA DE DATOS CON MATPLOLIB --------------------------------------------'''

def plot(json_str):
    #Creando la ventana en Tkinter
    window = Tk()
    df = order_data(json_str)
    df2= order_data2()
    #Creando la figura
    fig = Figure(figsize=(12, 7), dpi=100)
    plot1 = fig.add_subplot(111)





    #Llenando la figura y colocando marcadores
    plot1.plot(df['Duration'], df['Discount'], marker='o')
    plot1.plot(df2['Duration'], df2['Fee'], marker='o')
    fruits = ["apple", "banana"]
    plot1.legend(fruits)

    fig.autofmt_xdate()

    #Dibujando la figura en Canvas
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack()


    window.title('Plotting in Tkinter')
    window.state('zoomed')  # zooms the screen to maxm whenever executed

    '''plot_button = Button(master=window, command=plot, height=2, width=10, text="Plot")
    plot_button.pack()'''
    window.mainloop()




'''*********************************** AQUI ES EL ANALISIS DE LOS EJERCICIOS *******************************************'''


def plotEjercicios(usernameGlobal, token):
    # -**********************************************************
    #Creando la ventana en Tkinter
    window = Tk()
    headers = {"Authorization": "Bearer " + str(token)}
    #Creando la figura
    fig = Figure(figsize=(12, 7), dpi=100)
    plt = fig.add_subplot(111)
    #-**********************************************************


    # creando el request
    requestAsignado = requests.get(str(endpoint) + "asignado/codigo/" + str(usernameGlobal), headers=headers)
    # obteniendo la data
    dataAsignado = requestAsignado.json()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    if (requestAsignado.status_code == 200 and len(dataAsignado) > 0):
        # Obteniendo el data del request
        df = pd.read_json(json.dumps(dataAsignado), orient='records')
        df.columns = ['CodigoAsignado', 'Nombre']

        # Legends que se pondran en el grafico
        legendsNames = []  # Opción 1

        for i in range(len(df)):
            '''----------------------------------------------- EL REQUEST ---------------------------------------------'''
            # creando el request
            requestCodigoAsignado = requests.get(
                str(endpoint) + "cumplimiento/" + str(usernameGlobal) + "/" + str(df.iloc[i]['CodigoAsignado']),
                headers=headers)
            # obteniendo la data
            dataCodigoAsignado = requestCodigoAsignado.json()
            if (requestCodigoAsignado.status_code == 200 and len(dataCodigoAsignado) > 0):
                # Obteniendo el data del request
                '''----------------------------------------------- EL REQUEST ---------------------------------------------'''
                df2 = pd.read_json(json.dumps(dataCodigoAsignado), orient='records')
                df2.columns = ['fechaCumplimiento', 'aciertos']
                df2['fechaCumplimiento'] = pd.to_datetime(df2['fechaCumplimiento'], format='%Y-%m-%d')
                # Convirtiendo la fila a float
                df2 = df2.astype({'aciertos': 'float'})
                # Ordenando los valores segun la fecha
                '''df2 = df2.sort_values(by='fechaCumplimiento', ascending=True)'''
                plt.plot(df2['fechaCumplimiento'], df2['aciertos'], marker='o')
                legendsNames.append(df.iloc[i]['Nombre'])
            else:
                if (requestCodigoAsignado.status_code == 500):
                    print('Hubo un error al pedir los datos')
                else:
                    if (requestCodigoAsignado.status_code == 0):
                        print('No hay conexion con el servidor')

        plt.legend(legendsNames)
    else:
        if (requestAsignado.status_code == 500):
            print('Hubo un error al pedir los datos')
        else:
            if (requestAsignado.status_code == 0):
                print('No hay conexion con el servidor')
    '''----------------------------------------------- EL REQUEST ---------------------------------------------'''

    '''    FINALIZA: AQUI COMENZAMOS EL PEDIDO HACIA EL STRING BOOT    '''


    #Colocando los datos en diagonal
    fig.autofmt_xdate()
    #Dibujando la figura en Canvas
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack()

    window.title('Avances')
    window.state('zoomed')  # zooms the screen to maxm whenever executed

    '''plot_button = Button(master=window, command=plot, height=2, width=10, text="Plot")
    plot_button.pack()'''
    window.mainloop()





