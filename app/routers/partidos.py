from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Partido, PartidoCreate, PartidoUpdate

router = APIRouter()

@router.post("/partidos", response_model=Partido, status_code=status.HTTP_201_CREATED, tags=["partidos"])
async def create_partido(partido_data: PartidoCreate, session: SessionDep):
    partido = Partido(**partido_data.dict())
    session.add(partido)
    session.commit()
    session.refresh(partido)
    return partido

@router.get("/partidos/{partido_id}", response_model=Partido, tags=["partidos"])
async def read_partido(partido_id: int, session: SessionDep):
    partido = session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    return partido

@router.patch("/partidos/{partido_id}", response_model=Partido, tags=["partidos"])
async def update_partido(partido_id: int, partido_data: PartidoUpdate, session: SessionDep):
    partido = session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    for key, value in partido_data.dict(exclude_unset=True).items():
        setattr(partido, key, value)
    session.add(partido)
    session.commit()
    session.refresh(partido)
    return partido

@router.delete("/partidos/{partido_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["partidos"])
async def delete_partido(partido_id: int, session: SessionDep):
    partido = session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    session.delete(partido)
    session.commit()
    return {"detail": "Partido eliminado"}

@router.get("/partidos", response_model=list[Partido], tags=["partidos"])
async def list_partidos(session: SessionDep):
    partidos = session.exec(select(Partido)).all()
    return partidos