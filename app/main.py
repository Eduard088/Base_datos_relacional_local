# app/main.py
import time
import zoneinfo
from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from db import create_all_tables
from .routers import estados, municipios, partidos, municipales, congresos

app = FastAPI(lifespan=create_all_tables)

app.include_router(estados.router)
app.include_router(municipios.router)
app.include_router(partidos.router)
app.include_router(municipales.router)  # Procesos electorales municipales
app.include_router(congresos.router)    # Procesos electorales de congresos

@app.middleware("http")
async def log_request_headers(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.url} completed in: {process_time} seconds")
    return response

security = HTTPBasic()

@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if credentials.username == "eduardo" and credentials.password == "123456":
        return {"message": "Hello, Eduardo!"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

country_zones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima"
}

@app.get("/time/{iso_code}")
async def get_time_by_iso_code(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_zones.get(iso)
    if not timezone_str:
        raise HTTPException(status_code=404, detail="Zona horaria no encontrada para el ISO code proporcionado")
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

@app.get("/time1/{iso_code}")
async def time1(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_zones.get(iso)
    if not timezone_str:
        raise HTTPException(status_code=404, detail="Zona horaria no encontrada para el ISO code proporcionado")
    tz = zoneinfo.ZoneInfo(timezone_str)
    current_time = datetime.now(tz)
    formatted_time = current_time.strftime("%A, %Y-%m-%d %H:%M:%S")
    return {"time": formatted_time}