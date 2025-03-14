from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum

# --- Modelos para Estado ---
class Estado(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str

class EstadoCreate(SQLModel):
    nombre: str

class EstadoUpdate(SQLModel):
    nombre: Optional[str] = None

# --- Modelo para Municipio con clave primaria compuesta ---
class Municipio(SQLModel, table=True):
    estado_id: int = Field(foreign_key="estado.id", primary_key=True)
    id_municipio: int = Field(primary_key=True)  # Identificador del municipio en cada estado
    nombre: str

class MunicipioCreate(SQLModel):
    estado_id: int
    id_municipio: int
    nombre: str

class MunicipioUpdate(SQLModel):
    nombre: Optional[str] = None

# --- Modelo para Partido ---
class Partido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str

class PartidoCreate(SQLModel):
    nombre: str

class PartidoUpdate(SQLModel):
    nombre: Optional[str] = None

# --- Enum para la propiedad coalicion ---
class CoalicionEnum(str, Enum):
    SI = "sí"
    NO = "no"

# --- Modelo para Procesos Electorales Municipales ---
class ProcesoElectoralMunicipal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    año: int
    estado_id: int = Field(foreign_key="estado.id")
    id_municipio: int  # Debe corresponder a la clave compuesta en Municipio
    partido_id: int = Field(foreign_key="partido.id")
    votos: int
    votos_validos: int
    votos_candidato_sin_registro: int
    votos_nulos: int
    total_de_votos: int
    lista_nominal: int
    coalicion: CoalicionEnum

class ProcesoElectoralMunicipalCreate(SQLModel):
    año: int
    estado_id: int
    id_municipio: int
    partido_id: int
    votos: int
    votos_validos: int
    votos_candidato_sin_registro: int
    votos_nulos: int
    total_de_votos: int
    lista_nominal: int
    coalicion: CoalicionEnum

class ProcesoElectoralMunicipalUpdate(SQLModel):
    año: Optional[int] = None
    estado_id: Optional[int] = None
    id_municipio: Optional[int] = None
    partido_id: Optional[int] = None
    votos: Optional[int] = None
    votos_validos: Optional[int] = None
    votos_candidato_sin_registro: Optional[int] = None
    votos_nulos: Optional[int] = None
    total_de_votos: Optional[int] = None
    lista_nominal: Optional[int] = None
    coalicion: Optional[CoalicionEnum] = None

# --- Modelo para Congresos Electorales (se mantiene igual) ---
class CongresoElectoral(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    año: int
    estado_id: int = Field(foreign_key="estado.id")
    id_municipio: int  # Corresponde a la clave compuesta en Municipio
    partido_id: int = Field(foreign_key="partido.id")
    votos: int
    votos_validos: int
    votos_candidato_sin_registro: int
    votos_nulos: int
    total_de_votos: int
    lista_nominal: int
    coalicion: CoalicionEnum

class CongresoElectoralCreate(SQLModel):
    año: int
    estado_id: int
    id_municipio: int
    partido_id: int
    votos: int
    votos_validos: int
    votos_candidato_sin_registro: int
    votos_nulos: int
    total_de_votos: int
    lista_nominal: int
    coalicion: CoalicionEnum

class CongresoElectoralUpdate(SQLModel):
    año: Optional[int] = None
    estado_id: Optional[int] = None
    id_municipio: Optional[int] = None
    partido_id: Optional[int] = None
    votos: Optional[int] = None
    votos_validos: Optional[int] = None
    votos_candidato_sin_registro: Optional[int] = None
    votos_nulos: Optional[int] = None
    total_de_votos: Optional[int] = None
    lista_nominal: Optional[int] = None
    coalicion: Optional[CoalicionEnum] = None