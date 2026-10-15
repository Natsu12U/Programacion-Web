# obtener_datos.py
import yfinance as yf
import json
from datetime import date, timedelta

print("Descargando datos oficiales USD/MXN desde Yahoo Finance...")

# Descargamos los datos oficiales desde el 1 de enero de 2026
datos = yf.download("USDMXN=X", start="2026-01-01", end="2026-10-13", interval="1d")

# Guardamos las cotizaciones disponibles en un diccionario con formato YYYY-MM-DD
datos_descargados = {}
for fecha, fila in datos.iterrows():
    str_fecha_std = fecha.strftime("%Y-%m-%d")
    precio_cierre = round(float(fila['Close'].item()), 2)
    datos_descargados[str_fecha_std] = precio_cierre

historico_dolar = {}

# Rango exacto de fechas (1 de enero al 14 de octubre de 2026 -> 287 días)
fecha_inicio = date(2026, 1, 1)
fecha_fin = date(2026, 10, 14)

# Precio inicial de respaldo
ultimo_precio_conocido = 17.98 
fecha_actual = fecha_inicio

# Recorremos día por día sin omitir fines de semana o festivos
while fecha_actual <= fecha_fin:
    clave_std = fecha_actual.strftime("%Y-%m-%d")
    clave_es = fecha_actual.strftime("%d-%m-%Y")  # Formato DD-MM-AAAA
    
    # Si hubo cotización oficial ese día, actualizamos el precio
    if clave_std in datos_descargados:
        ultimo_precio_conocido = datos_descargados[clave_std]
    
    # Asignamos el precio al diccionario
    historico_dolar[clave_es] = {
        "fecha": clave_es,
        "precio": ultimo_precio_conocido,
        "moneda": "MXN"
    }
    
    fecha_actual += timedelta(days=1)

# Guardamos el resultado en el archivo JSON
with open("dolar_2026.json", "w", encoding="utf-8") as archivo:
    json.dump(historico_dolar, archivo, indent=4, ensure_ascii=False)

print(f"¡Listo! Se guardaron exactamente {len(historico_dolar)} registros en 'dolar_2026.json'.")