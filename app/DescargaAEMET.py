#!/usr/bin/env python
# coding: utf-8

## Importación de librerías

import requests
import json
import pandas as pd
import math
from datetime import datetime, timedelta
from sqlalchemy import create_engine

## Definición de funciones

# Recategorización del estado de tiempo
def switch_estadoCielo(cod):
    switcher = {
        11: [1, "Cielos despejados"],
        12: [2, "Intervalos nubosos"], 13: [2, "Intervalos nubosos"], 17: [2, "Intervalos nubosos"],
        14: [3, "Cielos nubosos"], 15: [3, "Cielos nubosos"],
        16: [4, "Cielos cubiertos"],
        43: [5, "Intervalos nubosos con lluvias débiles"],
        44: [6, "Cielos nubosos con lluvias débiles"], 45: [6, "Cielos nubosos con lluvias débiles"],
        46: [7, "Cielos cubiertos con lluvias débiles"],
        23: [8, "Intervalos nubosos con lluvias moderadas"],
        24: [9, "Cielos nubosos con lluvias moderadas"], 25: [9, "Cielos nubosos con lluvias moderadas"],
        26: [10, "Cielos cubiertos con lluvias moderadas"],
        61: [11, "Intervalos nubosos con chubascos tormentosos"], 51: [11, "Intervalos nubosos con chubascos tormentosos"],
        62: [12, "Cielos nubosos con chubascos tormentosos"], 52: [12, "Cielos nubosos con chubascos tormentosos"],
            63: [12, "Cielos nubosos con chubascos tormentosos"], 53: [12, "Cielos nubosos con chubascos tormentosos"],
        64: [13, "Cielos cubiertos con chubascos tormentosos"], 54: [13, "Cielos cubiertos con chubascos tormentosos"],
        71: [17, "Intervalos nubosos con nevadas"], 33: [17, "Intervalos nubosos con nevadas"],
        72: [18, "Cielos nubosos con nevadas"], 34: [18, "Cielos nubosos con nevadas"], 73: [18, "Cielos nubosos con nevadas"], 
            35: [18, "Cielos nubosos con nevadas"],
        19: [74, "Cielos cubiertos con nevadas"], 36: [19, "Cielos cubiertos con nevadas"], 
    }
    return(switcher.get(cod, [99, "Otro"]))


## Acceso a los datos

# Llamada a la URL que contiene los datos
url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/23050/"
apikey = {"api_key":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJncXVlc2FkYUB1amFlbi5lcyIsImp0aSI6IjlkN2VmNzFiLTgwMWQtNDEwOS1iNTZiLTNjYjNjNTMxZTRjNSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTQyMzU4MTIzLCJ1c2VySWQiOiI5ZDdlZjcxYi04MDFkLTQxMDktYjU2Yi0zY2IzYzUzMWU0YzUiLCJyb2xlIjoiIn0.Ws7sLfNahPNKKqd9lLtukRmettFORbXibzjdbb-CAJs"}
responseUrl = requests.request("GET", url, params=apikey)
jsonUrl = responseUrl.text
pyUrl = json.loads(jsonUrl)
responseData = requests.request("GET", pyUrl["datos"])

# Obtención del JSON con los datos
jsonData = responseData.text
data = json.loads(jsonData[1:-1])


## Preprocesamiento y creación de dataset con los datos

# Creación del dataframe a partir de los campos con periodiciadad horaria del JSON
for i in range(0, len(data['prediccion']['dia'])):
    dataDia = data['prediccion']['dia'][i]
    if i == 0:
        estadoCielo = pd.DataFrame.from_dict(dataDia['estadoCielo'])
        estadoCielo['fecha'] = dataDia['fecha']
        estadoCielo['salidaSol'] = str(dataDia['orto'])
        estadoCielo['puestaSol'] = str(dataDia['ocaso'])
        estadoCielo['minLuz'] = estadoCielo['puestaSol'].apply(lambda x: int(x[0:2]))*60 + estadoCielo['puestaSol'].apply(lambda x: int(x[3:5])) - (estadoCielo['salidaSol'].apply(lambda x: int(x[0:2]))*60 + estadoCielo['salidaSol'].apply(lambda x: int(x[3:5])))
        precipitacion = pd.DataFrame.from_dict(dataDia['precipitacion'])
        precipitacion['fecha'] = dataDia['fecha']
        probPrecipitacion = pd.DataFrame.from_dict(dataDia['probPrecipitacion'])
        probPrecipitacion['fecha'] = dataDia['fecha']
        probTormenta = pd.DataFrame.from_dict(dataDia['probTormenta'])
        probTormenta['fecha'] = dataDia['fecha']
        nieve = pd.DataFrame.from_dict(dataDia['nieve'])
        nieve['fecha'] = dataDia['fecha']
        probNieve = pd.DataFrame.from_dict(dataDia['probNieve'])
        probNieve['fecha'] = dataDia['fecha']
        temperatura = pd.DataFrame.from_dict(dataDia['temperatura'])
        temperatura['fecha'] = dataDia['fecha']
        sensTermica = pd.DataFrame.from_dict(dataDia['sensTermica'])
        sensTermica['fecha'] = dataDia['fecha']
        humedadRelativa = pd.DataFrame.from_dict(dataDia['humedadRelativa'])
        humedadRelativa['fecha'] = dataDia['fecha']
        vientoAndRachaMax = pd.DataFrame.from_dict(dataDia['vientoAndRachaMax'])
        vientoAndRachaMax['fecha'] = dataDia['fecha']
    else:
        eC = pd.DataFrame.from_dict(dataDia['estadoCielo'])
        eC['fecha'] = dataDia['fecha']
        eC['salidaSol'] = str(dataDia['orto'])
        eC['puestaSol'] = str(dataDia['ocaso'])
        eC['minLuz'] = eC['puestaSol'].apply(lambda x: int(x[0:2]))*60 + eC['puestaSol'].apply(lambda x: int(x[3:5])) - (eC['salidaSol'].apply(lambda x: int(x[0:2]))*60 + eC['salidaSol'].apply(lambda x: int(x[3:5])))
        estadoCielo = estadoCielo.append(eC, ignore_index = True)
        p = pd.DataFrame.from_dict(dataDia['precipitacion'])
        p['fecha'] = dataDia['fecha']
        precipitacion = precipitacion.append(p, ignore_index = True)
        pP = pd.DataFrame.from_dict(dataDia['probPrecipitacion'])
        pP['fecha'] = dataDia['fecha']
        probPrecipitacion = probPrecipitacion.append(pP, ignore_index = True)
        pT = pd.DataFrame.from_dict(dataDia['probTormenta'])
        pT['fecha'] = dataDia['fecha']
        probTormenta = probTormenta.append(pT, ignore_index = True)
        n = pd.DataFrame.from_dict(dataDia['nieve'])
        n['fecha'] = dataDia['fecha']
        nieve = nieve.append(n, ignore_index = True)
        pN = pd.DataFrame.from_dict(dataDia['probNieve'])
        pN['fecha'] = dataDia['fecha']
        probNieve = probNieve.append(pN, ignore_index = True)
        t = pd.DataFrame.from_dict(dataDia['temperatura'])
        t['fecha'] = dataDia['fecha']
        temperatura = temperatura.append(t, ignore_index = True)
        sT = pd.DataFrame.from_dict(dataDia['sensTermica'])
        sT['fecha'] = dataDia['fecha']
        sensTermica = sensTermica.append(sT, ignore_index = True)
        hR = pd.DataFrame.from_dict(dataDia['humedadRelativa'])
        hR['fecha'] = dataDia['fecha']
        humedadRelativa = humedadRelativa.append(hR, ignore_index = True)
        v = pd.DataFrame.from_dict(dataDia['vientoAndRachaMax'])
        v['fecha'] = dataDia['fecha']
        vientoAndRachaMax = vientoAndRachaMax.append(v, ignore_index = True)
# Reagrupación de categorías del estado del tiempo
estadoCielo['valueEC'] = estadoCielo['value'].apply(lambda x: unicode.replace(x,'n','')).apply(lambda x: int(x) if x!='' else x)
estadoCielo['codEstadoTiempo'] = estadoCielo['valueEC'].apply(lambda x: switch_estadoCielo(x)[0])
estadoCielo['descEstadoTiempo'] = estadoCielo['valueEC'].apply(lambda x: switch_estadoCielo(x)[1])
estadoCielo = estadoCielo.drop(columns = ['value'])
        
# Obtención de los campos con formato especial
viento = vientoAndRachaMax[0::2].drop(['value'], axis=1).reset_index(drop = True)
rachaMax = vientoAndRachaMax[1::2].drop(['direccion', 'velocidad'], axis=1).reset_index(drop = True)
probPrecipitacion = probPrecipitacion[probPrecipitacion["value"]!=""].reset_index(drop = True)
probTormenta = probTormenta[probTormenta["value"]!=""].reset_index(drop = True)
probNieve = probNieve[probNieve["value"]!=""].reset_index(drop = True)
pPrec = pd.DataFrame({'fecha': [], 'periodo': [], 'value': []})
pTorm = pd.DataFrame({'fecha': [], 'periodo': [], 'value': []})
pNiev = pd.DataFrame({'fecha': [], 'periodo': [], 'value': []})

for row in range(0, len(probPrecipitacion)):
    for inter in range(int(probPrecipitacion['periodo'][row][0:2]), int(probPrecipitacion['periodo'][row][0:2])+6):
        auxP = probPrecipitacion.iloc[row]
        auxP['periodo'] = str(inter%24).zfill(2)
        if (inter == 24):
            auxP['fecha'] = (datetime.strptime(auxP['fecha'], '%Y-%m-%d') + timedelta(days=1)).strftime("%Y-%m-%d") 
        pPrec = pPrec.append(auxP)
        pPrec = pPrec.reset_index(drop = True)
for row in range(0, len(probTormenta)):
    for inter in range(int(probTormenta['periodo'][row][0:2]), int(probTormenta['periodo'][row][0:2])+6):
        auxT = probTormenta.iloc[row]
        auxT['periodo'] = str(inter%24).zfill(2)
        if (inter == 24):
            auxT['fecha'] = (datetime.strptime(auxT['fecha'], '%Y-%m-%d') + timedelta(days=1)).strftime("%Y-%m-%d")  
        pTorm = pTorm.append(auxT)
        pTorm = pTorm.reset_index(drop = True)
for row in range(0, len(probNieve)):
    for inter in range(int(probNieve['periodo'][row][0:2]), int(probNieve['periodo'][row][0:2])+6):
        auxN = probNieve.iloc[row]
        auxN['periodo'] = str(inter%24).zfill(2)
        if (inter == 24):
            auxN['fecha'] = (datetime.strptime(auxN['fecha'], '%Y-%m-%d') + timedelta(days=1)).strftime("%Y-%m-%d")          
        pNiev = pNiev.append(auxN)
        pNiev = pNiev.reset_index(drop = True)
# Adicción de los campos con formato especial al dataframe        
tablaAEMET = pd.merge(estadoCielo, precipitacion, on=['fecha', 'periodo'], how='outer')
tablaAEMET = pd.merge(tablaAEMET, nieve, on=['fecha', 'periodo'], how='outer', suffixes=('_precipitacion', '_nieve'))
tablaAEMET = pd.merge(tablaAEMET, temperatura, on=['fecha', 'periodo'], how='outer')
tablaAEMET = pd.merge(tablaAEMET, sensTermica, on=['fecha', 'periodo'], how='outer', suffixes=('_temperatura', '_sensTermica'))
tablaAEMET = pd.merge(tablaAEMET, humedadRelativa, on=['fecha', 'periodo'], how='outer')
tablaAEMET = pd.merge(tablaAEMET, viento, on=['fecha', 'periodo'], how='outer')
tablaAEMET = pd.merge(tablaAEMET, rachaMax, on=['fecha', 'periodo'], how='outer', suffixes=('_humedadRelativa', '_rachaMax'))
tablaAEMET = pd.merge(tablaAEMET, pPrec, on=['fecha', 'periodo'], how='outer')
tablaAEMET = pd.merge(tablaAEMET, pTorm, on=['fecha', 'periodo'], how='outer', suffixes=('_pPrec', '_pTorm'))
tablaAEMET = pd.merge(tablaAEMET, pNiev, on=['fecha', 'periodo'], how='outer').rename(columns = {'value':'probNieve',
             'value_precipitacion':'precipitacion', 'value_nieve':'nieve', 'value_temperatura':'temperatura', 'value_sensTermica':'sensTermica',
             'value_humedadRelativa':'humedadRel', 'direccion':'dirViento', 'velocidad':'velViento', 'value_rachaMax':'velRachaMax',
             'value_pPrec':'probPrecipitacion', 'value_pTorm':'probTormenta'})
# Preprocesamos los tipos de datos de los campos
tablaAEMET['dirViento'] = tablaAEMET['dirViento'].apply(lambda x: x[0])
tablaAEMET['velViento'] = tablaAEMET['velViento'].apply(lambda x: x[0])
tablaAEMET['precipitacion'] = tablaAEMET['precipitacion'].apply(lambda x: unicode.replace(x, 'Ip', '0.05')).apply(lambda x: float(x) if x!='' else float(0))
tablaAEMET['nieve'] = tablaAEMET['nieve'].apply(lambda x: unicode.replace(x, 'Ip', '0.05')).apply(lambda x: float(x))
tablaAEMET['temperatura'] = tablaAEMET['temperatura'].apply(lambda x: float(x))
tablaAEMET['sensTermica'] = tablaAEMET['sensTermica'].apply(lambda x: float(x))
tablaAEMET['humedadRel'] = tablaAEMET['humedadRel'].apply(lambda x: int(x) if x!='' else int(50))
tablaAEMET['velViento'] = tablaAEMET['velViento'].apply(lambda x: float(x) if x!='' else float(0))
tablaAEMET['dirViento'] = tablaAEMET['dirViento'].apply(lambda x: str(0) if x=='' else x)
tablaAEMET['velRachaMax'] = tablaAEMET['velRachaMax'].apply(lambda x: float(x) if x!='' else float(0))
tablaAEMET['probPrecipitacion'] = tablaAEMET['probPrecipitacion'].apply(lambda x: int(x) if x!='' else int(0))
tablaAEMET['probTormenta'] = tablaAEMET['probTormenta'].apply(lambda x: int(x) if not math.isnan(float(x)) else int(0))
tablaAEMET['probNieve'] = tablaAEMET['probNieve'].apply(lambda x: int(x) if x!='' else int(0))
    
# Preprocesamiento de claves primarias para ambas tablas 
tablaAEMET['fechaPrediccion'] = data['elaborado'].replace('-', '') + data['prediccion']['dia'][0]['estadoCielo'][0]['periodo']
if (data['prediccion']['dia'][0]['estadoCielo'][0]['periodo'] == '20'):
    tablaAEMET['fechaPrediccion'] = str(datetime.strptime(data['elaborado'], '%Y-%m-%d').date() - timedelta(days=1)).replace('-', '') + data['prediccion']['dia'][0]['estadoCielo'][0]['periodo']
tablaAEMET['periodoPredicho'] = (tablaAEMET['fecha'] + " " + tablaAEMET['periodo']).apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H'))
tablaAEMET = tablaAEMET.drop(['fecha', 'periodo', 'valueEC', 'descripcion'], axis = 1)

# Ordenación de campos de ambas tablas
cols = tablaAEMET.columns.tolist()
cols = cols[-2:] + cols[:-2]
tablaAEMET = tablaAEMET[cols]


## Creación de tablas e introducción de datos en SQL

# Conexión a la base de datos
engine = create_engine("mysql+mysqldb://root:$PASSWORD@mariadb/predicciones")
try:
    tablaAEMET.to_sql(con=engine, name='aemet', if_exists='append', index = False)
except:
    pass

## Descarga de datos brutos
with open('./Brutos/AEMET/aemet' + tablaAEMET['fechaPrediccion'][0] + '.json', 'w') as outfile:
    json.dump(data, outfile)
