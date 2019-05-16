#!/usr/bin/env python
# coding: utf-8

## Importación de librerías

import requests
import json
from pandas.io.json import json_normalize
from datetime import datetime
from sqlalchemy import create_engine


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
        1: [1, "Cielos despejados"], 33: [1, "Cielos despejados"],
        2: [2, "Intervalos nubosos"], 3: [2, "Intervalos nubosos"],4: [2, "Intervalos nubosos"], 5: [2, "Intervalos nubosos"],
        34: [2, "Intervalos nubosos"], 35: [2, "Intervalos nubosos"], 36: [2, "Intervalos nubosos"], 37: [2, "Intervalos nubosos"],
        6: [3, "Cielos nubosos"], 7: [3, "Cielos nubosos"], 38: [3, "Cielos nubosos"],
        8: [4, "Cielos cubiertos"],
        14: [8, "Intervalos nubosos con lluvias moderadas"], 39: [8, "Intervalos nubosos con lluvias moderadas"],
        13: [9, "Cielos nubosos con lluvias moderadas"], 40: [9, "Cielos nubosos con lluvias moderadas"],
        12: [10, "Cielos cubiertos con lluvias moderadas"], 18: [10, "Cielos cubiertos con lluvias moderadas"],
        17: [11, "Intervalos nubosos con chubascos tormentosos"], 41: [11, "Intervalos nubosos con chubascos tormentosos"],
        16: [12, "Cielos nubosos con chubascos tormentosos"], 42: [12, "Cielos nubosos con chubascos tormentosos"],
        15: [13, "Cielos cubiertos con chubascos tormentosos"],
        24: [15, "Cielos nubosos con chubascos tormentosos y granizo"], 26: [15, "Cielos nubosos con chubascos tormentosos y granizo"],
        21: [17, "Intervalos nubosos con nevadas"],
        20: [18, "Cielos nubosos con nevadas"], 23: [18, "Cielos nubosos con nevadas"], 43: [18, "Cielos nubosos con nevadas"], 
        44: [18, "Cielos nubosos con nevadas"],
        19: [19, "Cielos cubiertos con nevadas"], 22: [19, "Cielos cubiertos con nevadas"], 29: [19, "Cielos cubiertos con nevadas"],
        25: [22, "Cielos cubiertos con aguanieve"],
        11: [23, "Niebla"]
    }
    return(switcher.get(cod, [99, "Otro"]))


## Acceso a los datos

# Llamada a la URL que contiene los datos
url = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/306731?apikey=wsAm7ccLSeHMhaEMtJVJ9qvceNetUcz9&language=es-es&details=true&metric=true"
responseData = requests.request("GET", url)

# Obtención del JSON con los datos
jsonData = responseData.text
data = json.loads(jsonData)


## Preprocesamiento y creación de dataset con los datos

# Creación de un dataframe a partir del json
tablaACCU = json_normalize(data)

# Seleccionamos las columnas para la tabla preprocesada
tablaACCU = tablaACCU[['DateTime', 'Ceiling.Value', 'CloudCover', 'DewPoint.Value', 'Ice.Value', 'IceProbability', 'WeatherIcon', 
                       'IsDaylight', 'PrecipitationProbability', 'Rain.Value', 'RainProbability', 'RealFeelTemperature.Value', 
                       'RelativeHumidity', 'Snow.Value', 'SnowProbability', 'Temperature.Value', 'TotalLiquid.Value', 'UVIndex', 
                       'UVIndexText', 'Visibility.Value', 'WetBulbTemperature.Value', 'Wind.Direction.Degrees', 'Wind.Speed.Value', 
                       'WindGust.Speed.Value']].rename(columns = {'DateTime':'periodoPredicho', 'Ceiling.Value':'altitudNubes', 
                       'CloudCover':'porcNubosidad', 'DewPoint.Value':'puntoRocio', 'Ice.Value':'granizo', 'IceProbability':'probGranizo',
                       'IsDaylight':'esDeDia', 'PrecipitationProbability':'probPrecipitacion', 'Rain.Value':'lluvia',
                       'RainProbability':'probLluvia', 'RealFeelTemperature.Value':'sensTermica', 'RelativeHumidity':'humedadRel',
                       'Snow.Value':'nieve', 'SnowProbability':'probNieve', 'Temperature.Value':'temperatura', 
                       'TotalLiquid.Value':'precipitacion', 'UVIndex':'indiceUV', 'UVIndexText':'catUV', 'Visibility.Value':'visibilidad',
                       'WetBulbTemperature.Value':'tempEPC', 'Wind.Speed.Value':'velViento', 'WindGust.Speed.Value': 'velRachaMax'})

# Preprocesamiento de la dirección del viento
tablaACCU['dirViento'] = tablaACCU['Wind.Direction.Degrees'].apply(lambda x: degreesToText(x))

# Reagrupación de categorías del estado del tiempo
tablaACCU['codEstadoTiempo'] = tablaACCU['WeatherIcon'].apply(lambda x: switch_estadoCielo(x)[0])
tablaACCU['descEstadoTiempo'] = tablaACCU['WeatherIcon'].apply(lambda x: switch_estadoCielo(x)[1])

# Eliminación de columnas preprocesadas originales
tablaACCU = tablaACCU.drop(columns = ['Wind.Direction.Degrees', 'WeatherIcon'])

# Preprocesamiento de claves primarias para ambas tablas
tablaACCU['periodoPredicho'] = tablaACCU['periodoPredicho'].apply(lambda x: x[:19]).apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
tablaACCU['fechaPrediccion'] = data[0]['DateTime'][:13].replace("-", "").replace("T", "")

# Ordenación de campos para ambas tablas
cols = tablaACCU.columns.tolist()
cols = cols[-1:] + cols[0:-1]
tablaACCU = tablaACCU[cols]


## Creación de tablas e introducción de datos en SQL

if (tablaACCU['fechaPrediccion'][0][-2:] in ('01', '07', '13', '19')):
	# Conexión a la base de datos
	engine = create_engine("mysql+mysqldb://root:$PASSWORD@mariadb:3306/predicciones")
	try:
  	# Creación de tabla SQL
  		tablaACCU.to_sql(con=engine, name='accuweather', if_exists='append', index = False)
	except:
		pass
  
	## Descarga de datos brutos
	with open('./Brutos/ACCUWEATHER/accuweather' + tablaACCU['fechaPrediccion'][0] + '.json', 'w') as outfile:
	    json.dump(data, outfile)
