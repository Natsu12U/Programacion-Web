# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI(
    title="API Tipo de Cambio Dólar 2026 (USD/MXN)",
    description="API para consultar el precio oficial del dólar por fecha (Formato DD-MM o DD-MM-AAAA)",
    version="1.0.0"
)

NOMBRE_ARCHIVO = "dolar_2026.json"

if not os.path.exists(NOMBRE_ARCHIVO):
    raise RuntimeError(f"No se encontró el archivo '{NOMBRE_ARCHIVO}'. Ejecuta primero 'obtener_datos.py'.")

with open(NOMBRE_ARCHIVO, "r", encoding="utf-8") as archivo:
    HISTORICO_DOLAR = json.load(archivo)


class RegistroDolar(BaseModel):
    fecha: str  # Formato DD-MM-AAAA o DD-MM
    precio: float
    moneda: str = "MXN"


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API del Precio del Dólar 2026",
        "formato_busqueda": "Puedes buscar como DD-MM (ej. 12-10) o DD-MM-AAAA (ej. 12-10-2026)",
        "total_registros": len(HISTORICO_DOLAR),
        "documentacion": "/docs"
    }

@app.get("/dolar")
def obtener_todos():
    return HISTORICO_DOLAR

# Endpoint que acepta tanto DD-MM como DD-MM-2026
@app.get("/dolar/{fecha}")
def obtener_por_fecha(fecha: str):
    clave_busqueda = fecha

    # Si el usuario solo manda el día y mes (ej. "12-10"), le añadimos automáticamente "-2026"
    if len(fecha) == 5 and "-" in fecha:
        clave_busqueda = f"{fecha}-2026"

    if clave_busqueda not in HISTORICO_DOLAR:
        raise HTTPException(
            status_code=404,
            detail=f"No hay registro para la fecha '{fecha}'. Usa formato DD-MM (ej: 12-10) o DD-MM-2026. Recuerda que fines de semana no se opera."
        )
    return HISTORICO_DOLAR[clave_busqueda]

@app.post("/dolar")
def agregar_registro(registro: RegistroDolar):
    clave = registro.fecha
    if len(clave) == 5 and "-" in clave:
        clave = f"{clave}-2026"
        
    HISTORICO_DOLAR[clave] = registro.model_dump()
    
    with open(NOMBRE_ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(HISTORICO_DOLAR, archivo, indent=4, ensure_ascii=False)
        
    return {"mensaje": "Registro agregado correctamente", "datos": registro}

