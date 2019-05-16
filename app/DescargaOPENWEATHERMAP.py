#!/usr/bin/env python
# coding: utf-8

## Importación de librerías

import requests
import json
from pandas.io.json import json_normalize
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import numpy as np
import pandas as pd


## Definición de funciones

# Convertir grados a puntos cardinales
def degreesToText(deg):
    val = int((deg/45) + .5)
    arr = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
    text = arr[(val % 8)]
    return(text)

# Recategorización del estado de tiempo
def switch_estadoCielo(cod):
    switcher = {
        800: [1, "Cielos despejados"],
        801: [2, "Intervalos nubosos"], 802: [2, "Intervalos nubosos"],
        803: [3, "Cielos nubosos"],
        804: [4, "Cielos cubiertos"],
        300: [5, "Intervalos nubosos con lluvias débiles"],
        310: [6, "Cielos nubosos con lluvias débiles"], 500: [6, "Cielos nubosos con lluvias débiles"],
        520: [7, "Cielos cubiertos con lluvias débiles"],
        301: [8, "Intervalos nubosos con lluvias moderadas"], 302: [8, "Intervalos nubosos con lluvias moderadas"],
             313:[8, "Intervalos nubosos con lluvias moderadas"], 314: [8, "Intervalos nubosos con lluvias moderadas"],
             321:[8, "Intervalos nubosos con lluvias moderadas"],
        311: [9, "Cielos nubosos con lluvias moderadas"], 312: [9, "Cielos nubosos con lluvias moderadas"],
             501:[9, "Cielos nubosos con lluvias moderadas"], 502: [9, "Cielos nubosos con lluvias moderadas"],
             503:[9, "Cielos nubosos con lluvias moderadas"], 504: [9, "Cielos nubosos con lluvias moderadas"],
        521: [10, "Cielos cubiertos con lluvias moderadas"], 522: [10, "Cielos cubiertos con lluvias moderadas"],
             531: [10, "Cielos cubiertos con lluvias moderadas"],
        200: [11, "Intervalos nubosos con chubascos tormentosos"], 210: [11, "Intervalos nubosos con chubascos tormentosos"],
             221: [11, "Intervalos nubosos con chubascos tormentosos"], 230: [11, "Intervalos nubosos con chubascos tormentosos"],
        201: [12, "Cielos nubosos con chubascos tormentosos"], 211: [12, "Cielos nubosos con chubascos tormentosos"],
             231: [12, "Cielos nubosos con chubascos tormentosos"],
        202: [13, "Cielos cubiertos con chubascos tormentosos"], 212: [13, "Cielos cubiertos con chubascos tormentosos"],
             232: [13, "Cielos cubiertos con chubascos tormentosos"],
        511: [15, "Cielos nubosos con chubascos tormentosos y granizo"],
        600: [17, "Intervalos nubosos con nevadas"], 620: [17, "Intervalos nubosos con nevadas"], 621: [17, "Intervalos nubosos con nevadas"],
             622: [17, "Intervalos nubosos con nevadas"],   
        601: [18, "Cielos nubosos con nevadas"], 615: [18, "Cielos nubosos con nevadas"], 616: [18, "Cielos nubosos con nevadas"], 
        602: [19, "Cielos cubiertos con nevadas"],
        611: [21, "Cielos nubosos con aguanieve"],
        612: [22, "Cielos cubiertos con aguanieve"],
        701: [23, "Niebla"], 711: [23, "Niebla"], 721: [23, "Niebla"], 741: [23, "Niebla"]
    }
    return(switcher.get(cod, [99, "Otro"]))


## Acceso a los datos

# Llamada a la URL que contiene los datos
url = "http://api.openweathermap.org/data/2.5/forecast?id=6358500&appid=bbba35b0e71686219ccb2cf8ec7490f8&units=metric&lang=es"
responseData = requests.request("GET", url)

# Obtención del JSON con los datos
jsonData = responseData.text.replace('[{"id"', '{"id"').replace('}],"clouds"', '},"clouds"')
data = json.loads(jsonData)


## Preprocesamiento y creación de dataset con los datos

# Creación de un dataframe a partir del json
tablaOPEN = json_normalize(data['list'])

# Eliminación de campos no necesarios
tablaOPEN = tablaOPEN.drop(['dt', 'main.grnd_level', 'main.temp_kf', 'sys.pod', 'weather.icon', 
                            'weather.description', 'weather.main'], axis=1).rename(columns = {'dt_txt':'periodoPredicho',
                            'main.humidity':'humedadRel','main.pressure':'presion','main.temp':'temperatura', 
                            'main.temp_max':'tempMax', 'main.temp_min':'tempMin', 'rain.3h':'lluvia', 'wind.speed':'velViento',
                            'clouds.all':'porcNubosidad', 'main.sea_level':'presionNivMar', 'snow.3h':'nieve'})

# Preprocesamiento de la dirección del viento, lluvia y nieve
tablaOPEN['dirViento'] = tablaOPEN['wind.deg'].apply(lambda x: degreesToText(x))
if 'lluvia' in tablaOPEN:
    tablaOPEN['lluvia'] = tablaOPEN['lluvia']/3
if 'nieve' in tablaOPEN:
    tablaOPEN['nieve'] = tablaOPEN['nieve']/3

# Reagrupación de categorías del estado del tiempo
tablaOPEN['codEstadoTiempo'] = tablaOPEN['weather.id'].apply(lambda x: switch_estadoCielo(x)[0])
tablaOPEN['descEstadoTiempo'] = tablaOPEN['weather.id'].apply(lambda x: switch_estadoCielo(x)[1])

# Eliminación de columnas preprocesadas originales
tablaOPEN = tablaOPEN.drop(columns = ['wind.deg', 'weather.id'])

# Preprocesamiento de claves primarias
tablaOPEN['fechaPrediccion'] = data['list'][0]['dt_txt'].replace("-", "").replace(" ", "").replace(":00:00", "")
tablaOPEN['periodoPredicho'] = tablaOPEN['periodoPredicho'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

# Ordenación de campos de las dos tablas
cols = tablaOPEN.columns.tolist()
cols =cols[-1:] + cols[1:-1] + cols[0:1]
tablaOPEN = tablaOPEN[cols]

# Sustitución de campos nulos por cero
tablaOPEN = tablaOPEN.fillna(0)


## Interpolación de los datos intermedios

# Interpolación de los datos de las horas +1

tablaOPEN1 = tablaOPEN.copy() 
tablaOPEN1['periodoPredicho'] = tablaOPEN['periodoPredicho'] + timedelta(hours=1)
tablaOPEN1['humedadRel'] = (tablaOPEN['humedadRel'] + (tablaOPEN.groupby('fechaPrediccion').humedadRel.transform(np.roll, shift=-1) - tablaOPEN['humedadRel'])/3).apply(lambda x: int(x))
tablaOPEN1['presion'] = (tablaOPEN['presion'] + (tablaOPEN.groupby('fechaPrediccion').presion.transform(np.roll, shift=-1) - tablaOPEN['presion'])/3).apply(lambda x: round(x,2))
tablaOPEN1['presionNivMar'] = (tablaOPEN['presionNivMar'] + (tablaOPEN.groupby('fechaPrediccion').presionNivMar.transform(np.roll, shift=-1) - tablaOPEN['presionNivMar'])/3).apply(lambda x: round(x,2))
tablaOPEN1['temperatura'] = (tablaOPEN['temperatura'] + (tablaOPEN.groupby('fechaPrediccion').temperatura.transform(np.roll, shift=-1) - tablaOPEN['temperatura'])/3).apply(lambda x: round(x,2))
tablaOPEN1['tempMax'] = (tablaOPEN['tempMax'] + (tablaOPEN.groupby('fechaPrediccion').tempMax.transform(np.roll, shift=-1) - tablaOPEN['tempMax'])/3).apply(lambda x: round(x,2))
tablaOPEN1['tempMin'] = (tablaOPEN['tempMin'] + (tablaOPEN.groupby('fechaPrediccion').tempMin.transform(np.roll, shift=-1) - tablaOPEN['tempMin'])/3).apply(lambda x: round(x,2))
tablaOPEN1['velViento'] = (tablaOPEN['velViento'] + (tablaOPEN.groupby('fechaPrediccion').velViento.transform(np.roll, shift=-1) - tablaOPEN['velViento'])/3).apply(lambda x: round(x,2))
tablaOPEN1['porcNubosidad'] = (tablaOPEN['porcNubosidad'] + (tablaOPEN.groupby('fechaPrediccion').porcNubosidad.transform(np.roll, shift=-1) - tablaOPEN['porcNubosidad'])/3).apply(lambda x: int(x))
tablaOPEN1 = tablaOPEN1[0:len(tablaOPEN1)-1]

# Interpolación de los datos de las horas +2

tablaOPEN2 = tablaOPEN.copy() 
tablaOPEN2['periodoPredicho'] = tablaOPEN['periodoPredicho'] + timedelta(hours=2)
tablaOPEN2['humedadRel'] = (tablaOPEN['humedadRel'] + (tablaOPEN.groupby('fechaPrediccion').humedadRel.transform(np.roll, shift=-1) - tablaOPEN['humedadRel'])*2/3).apply(lambda x: int(x))
tablaOPEN2['presion'] = (tablaOPEN['presion'] + (tablaOPEN.groupby('fechaPrediccion').presion.transform(np.roll, shift=-1) - tablaOPEN['presion'])*2/3).apply(lambda x: round(x,2))
tablaOPEN2['presionNivMar'] = (tablaOPEN['presionNivMar'] + (tablaOPEN.groupby('fechaPrediccion').presionNivMar.transform(np.roll, shift=-1) - tablaOPEN['presionNivMar'])*2/3).apply(lambda x: round(x,2))
tablaOPEN2['temperatura'] = (tablaOPEN['temperatura'] + (tablaOPEN.groupby('fechaPrediccion').temperatura.transform(np.roll, shift=-1) - tablaOPEN['temperatura'])*2/3).apply(lambda x: round(x,2))
tablaOPEN2['tempMax'] = (tablaOPEN['tempMax'] + (tablaOPEN.groupby('fechaPrediccion').tempMax.transform(np.roll, shift=-1) - tablaOPEN['tempMax'])*2/3).apply(lambda x: round(x,2))
tablaOPEN2['tempMin'] = (tablaOPEN['tempMin'] + (tablaOPEN.groupby('fechaPrediccion').tempMin.transform(np.roll, shift=-1) - tablaOPEN['tempMin'])*2/3).apply(lambda x: round(x,2))
tablaOPEN2['velViento'] = (tablaOPEN['velViento'] + (tablaOPEN.groupby('fechaPrediccion').velViento.transform(np.roll, shift=-1) - tablaOPEN['velViento'])*2/3).apply(lambda x: round(x,2))
tablaOPEN2['dirViento'] = tablaOPEN.groupby('fechaPrediccion').dirViento.transform(np.roll, shift=-1)
tablaOPEN2['codEstadoTiempo'] = tablaOPEN.groupby('fechaPrediccion').codEstadoTiempo.transform(np.roll, shift=-1)
tablaOPEN2['descEstadoTiempo'] = tablaOPEN.groupby('fechaPrediccion').descEstadoTiempo.transform(np.roll, shift=-1)
tablaOPEN2['porcNubosidad'] = (tablaOPEN['porcNubosidad'] + (tablaOPEN.groupby('fechaPrediccion').porcNubosidad.transform(np.roll, shift=-1) - tablaOPEN['porcNubosidad'])*2/3).apply(lambda x: int(x))
if 'lluvia' in tablaOPEN2:
    tablaOPEN2['lluvia'] = tablaOPEN.groupby('fechaPrediccion').lluvia.transform(np.roll, shift=-1)
if 'nieve' in tablaOPEN2:
    tablaOPEN2['nieve'] = tablaOPEN.groupby('fechaPrediccion').nieve.transform(np.roll, shift=-1)
tablaOPEN2 = tablaOPEN2[0:len(tablaOPEN2)-1]

# Concatenación de todos los datos

tablaOPEN = pd.concat([tablaOPEN, tablaOPEN1, tablaOPEN2])
tablaOPEN.reset_index(inplace = True)
tablaOPEN = tablaOPEN.drop(['index'], axis = 1)


## Creación de tablas e introducción de datos en SQL

if (tablaOPEN['fechaPrediccion'][0][-2:] in ('00', '06', '12', '18')):
    # Conexión a la base de datos
    engine = create_engine("mysql+mysqldb://root:$PASSWORD@mariadb:3306/predicciones")
    try:
        # Creación de tabla SQL
        tablaOPEN.to_sql(con=engine, name='open', if_exists='append', index = False)
    except:
        pass

    ## Descarga de datos brutos
    with open('./Brutos/OPEN/open' + tablaOPEN['fechaPrediccion'][0] + '.json', 'w') as outfile:
        json.dump(data, outfile)
