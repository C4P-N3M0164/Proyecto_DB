import requests
import pandas as pd
import datetime
import time

# Configuración de fechas
FECHA_FIN = datetime.date(2024, 4, 30)
FECHA_INICIO = FECHA_FIN - datetime.timedelta(days=3*365)

# Endpoints correctos
URL_HOURLY = 'https://servapibi.xm.com.co/hourly'
URL_MONTHLY = 'https://servapibi.xm.com.co/monthly'
URL_LISTS = 'https://servapibi.xm.com.co/Lists'

# Función para obtener la lista de agentes
def obtener_agentes():
    payload = {"MetricId": "ListadoAgentes"}
    r = requests.post(URL_LISTS, json=payload)
    r.raise_for_status()
    data = r.json()
    # Ajusta aquí según la estructura real de la respuesta
    if 'Data' in data:
        return data['Data']
    if 'Items' in data:
        return data['Items']
    return []

# Función para dividir el rango de fechas en meses
def rangos_mensuales(fecha_inicio, fecha_fin):
    rangos = []
    actual = fecha_inicio
    while actual < fecha_fin:
        siguiente = (actual.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
        fin = min(siguiente - datetime.timedelta(days=1), fecha_fin)
        rangos.append((actual, fin))
        actual = siguiente
    return rangos

# DemaCome por Sistema (hourly)
def consultar_demacome(fecha_inicio, fecha_fin):
    datos = []
    rangos = rangos_mensuales(fecha_inicio, fecha_fin)
    for inicio, fin in rangos:
        payload = {
            "MetricId": "DemaCome",
            "StartDate": str(inicio),
            "EndDate": str(fin),
            "Entity": "Sistema",
            "Filter": []
        }
        r = requests.post(URL_HOURLY, json=payload)
        if r.status_code == 200:
            res = r.json()
            for item in res.get('Items', []):
                date = item.get('Date')
                for ent in item.get('HourlyEntities', []):
                    row = {'Date': date}
                    row.update(ent.get('Values', {}))
                    datos.append(row)
        else:
            print(f"Error consultando DemaCome de {inicio} a {fin}")

    return datos

# DemaReal por Agente (hourly)
def consultar_demareal(agentes, fecha_inicio, fecha_fin):
    datos = []
    rangos = rangos_mensuales(fecha_inicio, fecha_fin)
    for agente in agentes:
        # Extract agent code from the correct structure
        if 'ListEntities' in agente:
            for entity in agente['ListEntities']:
                if 'Values' in entity:
                    codigo = entity['Values'].get('Code')
                    if codigo:
                        print(f"Consultando DemaReal para agente: {codigo}")
                        for inicio, fin in rangos:
                            payload = {
                                "MetricId": "DemaReal",
                                "StartDate": str(inicio),
                                "EndDate": str(fin),
                                "Entity": "Agente",
                                "Filter": [codigo]
                            }
                            r = requests.post(URL_HOURLY, json=payload)
                            if r.status_code == 200:
                                res = r.json()
                                for item in res.get('Items', []):
                                    date = item.get('Date')
                                    for ent in item.get('HourlyEntities', []):
                                        row = {'Date': date, 'Agente': codigo}
                                        row.update(ent.get('Values', {}))
                                        datos.append(row)
                            else:
                                print(f"Error consultando DemaReal para {codigo} de {inicio} a {fin}")
                          
    return datos

# CERE por Sistema (monthly)
def consultar_cere(fecha_inicio, fecha_fin):
    datos = []
    rangos = rangos_mensuales(fecha_inicio, fecha_fin)
    for inicio, fin in rangos:
        payload = {
            "MetricId": "CERE",
            "StartDate": str(inicio),
            "EndDate": str(fin),
            "Entity": "Sistema",
            "Filter": []
        }
        r = requests.post(URL_MONTHLY, json=payload)
        if r.status_code == 200:
            res = r.json()
            for item in res.get('Items', []):
                date = item.get('Date')
                for ent in item.get('MonthlyEntities', []):
                    row = {'Date': date}
                    row.update(ent)
                    datos.append(row)
        else:
            print(f"Error consultando CERE de {inicio} a {fin}")
    return datos

# Guardar en CSV
def guardar_csv(datos, nombre):
    df = pd.DataFrame(datos)
    df.to_csv(nombre, index=False)

if __name__ == "__main__":
    print("Obteniendo lista de agentes...")
    agentes = obtener_agentes()
    print(f"Total agentes: {len(agentes)}")

    print("Consultando DemaCome...")
    datos_demacome = consultar_demacome(FECHA_INICIO, FECHA_FIN)
    guardar_csv(datos_demacome, "demacome.csv")
    print("DemaCome guardado en demacome.csv")

    print("Consultando DemaReal...")
    datos_demareal = consultar_demareal(agentes, FECHA_INICIO, FECHA_FIN)
    guardar_csv(datos_demareal, "demareal.csv")
    print("DemaReal guardado en demareal.csv")

    print("Consultando CERE...")
    datos_cere = consultar_cere(FECHA_INICIO, FECHA_FIN)
    guardar_csv(datos_cere, "cere.csv")
    print("CERE guardado en cere.csv")

    print("Extracción finalizada. Los archivos CSV están listos para cargar en la base de datos.") 