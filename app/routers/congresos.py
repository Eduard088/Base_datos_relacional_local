from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from db import SessionDep
from models import CongresoElectoral, CongresoElectoralCreate, CongresoElectoralUpdate

router = APIRouter()

@router.post("/congresos", response_model=CongresoElectoral, status_code=status.HTTP_201_CREATED, tags=["congresos"])
async def create_congreso(congreso_data: CongresoElectoralCreate, session: SessionDep):
    congreso = CongresoElectoral(**congreso_data.dict())
    session.add(congreso)
    session.commit()
    session.refresh(congreso)
    return congreso

@router.get("/congresos/{congreso_id}", response_model=CongresoElectoral, tags=["congresos"])
async def read_congreso(congreso_id: int, session: SessionDep):
    congreso = session.get(CongresoElectoral, congreso_id)
    if not congreso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Congreso electoral no encontrado")
    return congreso

@router.patch("/congresos/{congreso_id}", response_model=CongresoElectoral, tags=["congresos"])
async def update_congreso(congreso_id: int, congreso_data: CongresoElectoralUpdate, session: SessionDep):
    congreso = session.get(CongresoElectoral, congreso_id)
    if not congreso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Congreso electoral no encontrado")
    for key, value in congreso_data.dict(exclude_unset=True).items():
        setattr(congreso, key, value)
    session.add(congreso)
    session.commit()
    session.refresh(congreso)
    return congreso

@router.delete("/congresos/{congreso_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["congresos"])
async def delete_congreso(congreso_id: int, session: SessionDep):
    congreso = session.get(CongresoElectoral, congreso_id)
    if not congreso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Congreso electoral no encontrado")
    session.delete(congreso)
    session.commit()
    return {"detail": "Congreso electoral eliminado"}

@router.get("/congresos", response_model=list[CongresoElectoral], tags=["congresos"])
async def list_congresos(
    session: SessionDep,
    skip: int = Query(0, description="Registros a omitir"),
    limit: int = Query(10, description="Cantidad de registros a mostrar")
):
    congresos = session.exec(select(CongresoElectoral).offset(skip).limit(limit)).all()
    return congresos
