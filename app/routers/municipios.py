from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Municipio, MunicipioCreate, MunicipioUpdate

router = APIRouter()

@router.post("/municipios", response_model=Municipio, status_code=status.HTTP_201_CREATED, tags=["municipios"])
async def create_municipio(municipio_data: MunicipioCreate, session: SessionDep):
    municipio = Municipio(**municipio_data.dict())
    session.add(municipio)
    session.commit()
    session.refresh(municipio)
    return municipio

@router.get("/municipios/{municipio_id}", response_model=Municipio, tags=["municipios"])
async def read_municipio(municipio_id: int, session: SessionDep):
    municipio = session.get(Municipio, municipio_id)
    if not municipio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Municipio no encontrado")
    return municipio

@router.patch("/municipios/{municipio_id}", response_model=Municipio, tags=["municipios"])
async def update_municipio(municipio_id: int, municipio_data: MunicipioUpdate, session: SessionDep):
    municipio = session.get(Municipio, municipio_id)
    if not municipio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Municipio no encontrado")
    for key, value in municipio_data.dict(exclude_unset=True).items():
        setattr(municipio, key, value)
    session.add(municipio)
    session.commit()
    session.refresh(municipio)
    return municipio

@router.delete("/municipios/{municipio_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["municipios"])
async def delete_municipio(municipio_id: int, session: SessionDep):
    municipio = session.get(Municipio, municipio_id)
    if not municipio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Municipio no encontrado")
    session.delete(municipio)
    session.commit()
    return {"detail": "Municipio eliminado"}

@router.get("/municipios", response_model=list[Municipio], tags=["municipios"])
async def list_municipios(session: SessionDep):
    municipios = session.exec(select(Municipio)).all()
    return municipios