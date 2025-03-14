from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Estado, EstadoCreate, EstadoUpdate

router = APIRouter()

@router.post("/estados", response_model=Estado, status_code=status.HTTP_201_CREATED, tags=["estados"])
async def create_estado(estado_data: EstadoCreate, session: SessionDep):
    estado = Estado(**estado_data.dict())
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

@router.get("/estados/{estado_id}", response_model=Estado, tags=["estados"])
async def read_estado(estado_id: int, session: SessionDep):
    estado = session.get(Estado, estado_id)
    if not estado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estado no encontrado")
    return estado

@router.patch("/estados/{estado_id}", response_model=Estado, tags=["estados"])
async def update_estado(estado_id: int, estado_data: EstadoUpdate, session: SessionDep):
    estado = session.get(Estado, estado_id)
    if not estado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estado no encontrado")
    for key, value in estado_data.dict(exclude_unset=True).items():
        setattr(estado, key, value)
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

@router.delete("/estados/{estado_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["estados"])
async def delete_estado(estado_id: int, session: SessionDep):
    estado = session.get(Estado, estado_id)
    if not estado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estado no encontrado")
    session.delete(estado)
    session.commit()
    return {"detail": "Estado eliminado"}

@router.get("/estados", response_model=list[Estado], tags=["estados"])
async def list_estados(session: SessionDep):
    estados = session.exec(select(Estado)).all()
    return estados