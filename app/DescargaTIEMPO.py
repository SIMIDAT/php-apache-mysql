#!/usr/bin/env python
# coding: utf-8

## Importación de librerías

import requests
import json
from json import dumps
from xmljson import abdera as ab
from xml.etree.ElementTree import fromstring
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine


## Acceso a los datos

# Llamada a la URL que contiene los datos
url = "http://api.tiempo.com/index.php?api_lang=es&localidad=3593&affiliate_id=aw5yegz36j7l&v=2.0&h=1"
responseData = requests.request("GET", url)

# Obtención del JSON con los datos
jsonXml = responseData.text
data = json.loads(dumps(ab.data(fromstring(jsonXml.encode('utf8'))),  ensure_ascii=False))


## Preprocesamiento y creación de dataset con los datos

# Formación del dataframe a partir de los campos del JSON
for dia in range(1, 3):
    salidaSol = str(data['report']['location']['children'][dia]['day']['children'][9]['sun']['attributes']['in'])
    puestaSol = str(data['report']['location']['children'][dia]['day']['children'][9]['sun']['attributes']['out'])
    cenitSol = str(data['report']['location']['children'][dia]['day']['children'][9]['sun']['attributes']['mid'])
    minLuz = int(puestaSol[0:2])*60 + int(puestaSol[3:5]) - (int(salidaSol[0:2])*60 + int(salidaSol[3:5]))
    for i in range(12, len(data['report']['location']['children'][dia]['day']['children'])):
        dataDia = data['report']['location']['children'][dia]['day']['children'][i]['hour']
        fecha = str(data['report']['location']['children'][dia]['day']['attributes']['value'])
        periodo = dataDia['attributes']['value']
        if(periodo == '24:00'):
            periodo = '00:00'
            fecha = (datetime.strptime(fecha, '%Y%m%d') + timedelta(days=1)).strftime('%Y%m%d')
        temperatura = float(dataDia['children'][0]['temp']['attributes']['value'])
        codEstadoCielo = dataDia['children'][1]['symbol']['attributes']['value2']
        estadoCielo = dataDia['children'][1]['symbol']['attributes']['desc2']
        vientoVeloc = float(dataDia['children'][2]['wind']['attributes']['value'])
        vientoDir = dataDia['children'][2]['wind']['attributes']['dir']
        rachaMax = float(dataDia['children'][3]['wind-gusts']['attributes']['value'])
        lluvia = float(dataDia['children'][4]['rain']['attributes']['value'])
        humedad = dataDia['children'][5]['humidity']['attributes']['value']
        presion = float(dataDia['children'][6]['pressure']['attributes']['value'])
        pNubosidad = int(dataDia['children'][7]['clouds']['attributes']['value'].replace('%', ''))
        cotaNieve = dataDia['children'][8]['snowline']['attributes']['value']
        sensTermica = float(dataDia['children'][9]['windchill']['attributes']['value'])
        if dia == 1 and i == 12:
            tablaTIEMPO = pd.DataFrame([[salidaSol, puestaSol, cenitSol, minLuz, fecha, periodo, temperatura, codEstadoCielo, estadoCielo, vientoVeloc, vientoDir, rachaMax,
                                        lluvia, humedad, presion, pNubosidad, cotaNieve, sensTermica]], 
                                        columns = ['salidaSol', 'puestaSol', 'cenitSol', 'minLuz', 'fecha', 'periodo', 'temperatura', 'codEstadoTiempo', 'descEstadoTiempo', 'velViento', 
                                                  'dirViento', 'velRachaMax', 'precipitacion', 'humedadRel', 'presion', 'porcNubosidad', 'cotaNieve', 'sensTermica'])
        else:
            tT = pd.DataFrame([[salidaSol, puestaSol, cenitSol, minLuz, fecha, periodo, temperatura, codEstadoCielo, estadoCielo, vientoVeloc, vientoDir, rachaMax,
                                lluvia, humedad, presion, pNubosidad, cotaNieve, sensTermica]], 
                                columns = ['salidaSol', 'puestaSol', 'cenitSol', 'minLuz', 'fecha', 'periodo', 'temperatura', 'codEstadoTiempo', 'descEstadoTiempo', 'velViento', 
                                           'dirViento', 'velRachaMax', 'precipitacion', 'humedadRel', 'presion', 'porcNubosidad', 'cotaNieve', 'sensTermica'])     
            tablaTIEMPO = tablaTIEMPO.append(tT, ignore_index = True)

# Preprocesamiento de la dirección del viento
tablaTIEMPO['dirViento'] = tablaTIEMPO['dirViento'].apply(lambda x: unicode.replace(x, 'W', 'O'))          
   
# Preprocesamiento de claves primarias para ambas tablas          
tablaTIEMPO['fechaPrediccion'] = str(data['report']['location']['children'][1]['day']['attributes']['value'])+data['report']['location']['children'][1]['day']['children'][12]['hour']['attributes']['value'][0:2] 
tablaTIEMPO['periodoPredicho'] = (tablaTIEMPO['fecha'] + " " + tablaTIEMPO['periodo']).apply(lambda x: datetime.strptime(x, '%Y%m%d %H:%M'))
tablaTIEMPO = tablaTIEMPO.drop(['fecha', 'periodo'], axis = 1)

# Ordenación de campos de ambas tablas
cols = tablaTIEMPO.columns.tolist()
cols = cols[-2:] + cols[:-2]
tablaTIEMPO = tablaTIEMPO[cols]
	

## Creación de tablas e introducción de datos en SQL

# Conexión a la base de datos
engine = create_engine("mysql+mysqldb://root:$PASSWORD@mariadb:3306/predicciones")
try:
    # Creación de tabla SQL
    tablaTIEMPO.to_sql(con=engine, name='tiempo', if_exists='append', index = False)
except:
    pass
	
## Descarga de datos brutos
with open('./Brutos/TIEMPO/tiempo' + tablaTIEMPO['fechaPrediccion'][0] + '.json', 'w') as outfile:
    json.dump(data, outfile)
