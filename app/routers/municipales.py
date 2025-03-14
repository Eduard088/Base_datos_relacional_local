# app/routers/municipales.py
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from db import SessionDep
from models import (
    ProcesoElectoralMunicipal,
    ProcesoElectoralMunicipalCreate,
    ProcesoElectoralMunicipalUpdate,
)

router = APIRouter()

@router.post("/municipales", response_model=ProcesoElectoralMunicipal, status_code=status.HTTP_201_CREATED, tags=["municipales"])
async def create_municipal(proceso_data: ProcesoElectoralMunicipalCreate, session: SessionDep):
    proceso = ProcesoElectoralMunicipal(**proceso_data.dict())
    session.add(proceso)
    session.commit()
    session.refresh(proceso)
    return proceso

@router.get("/municipales/{proceso_id}", response_model=ProcesoElectoralMunicipal, tags=["municipales"])
async def read_municipal(proceso_id: int, session: SessionDep):
    proceso = session.get(ProcesoElectoralMunicipal, proceso_id)
    if not proceso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proceso electoral municipal no encontrado")
    return proceso

@router.patch("/municipales/{proceso_id}", response_model=ProcesoElectoralMunicipal, tags=["municipales"])
async def update_municipal(proceso_id: int, proceso_data: ProcesoElectoralMunicipalUpdate, session: SessionDep):
    proceso = session.get(ProcesoElectoralMunicipal, proceso_id)
    if not proceso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proceso electoral municipal no encontrado")
    for key, value in proceso_data.dict(exclude_unset=True).items():
        setattr(proceso, key, value)
    session.add(proceso)
    session.commit()
    session.refresh(proceso)
    return proceso

@router.delete("/municipales/{proceso_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["municipales"])
async def delete_municipal(proceso_id: int, session: SessionDep):
    proceso = session.get(ProcesoElectoralMunicipal, proceso_id)
    if not proceso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proceso electoral municipal no encontrado")
    session.delete(proceso)
    session.commit()
    return {"detail": "Proceso electoral municipal eliminado"}

@router.get("/municipales", response_model=list[ProcesoElectoralMunicipal], tags=["municipales"])
async def list_municipales(
    session: SessionDep,
    skip: int = Query(0, description="Registros a omitir"),
    limit: int = Query(10, description="Cantidad de registros a mostrar")
):
    procesos = session.exec(select(ProcesoElectoralMunicipal).offset(skip).limit(limit)).all()
    return procesos