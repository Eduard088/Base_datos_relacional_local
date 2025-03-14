import pandas as pd
from sqlmodel import Session, select
from models import Estado, Municipio, Partido, ProcesoElectoralMunicipal, CoalicionEnum
from db import engine

def import_municipales(csv_file: str):
    # Leer el CSV desde la ruta indicada
    df = pd.read_csv(csv_file)
    
    # Abrir la sesión de la base de datos
    with Session(engine) as session:
        for index, row in df.iterrows():
            # --- 1. Verificar o insertar Estado ---
            id_estado = int(row['ID_estado'])
            nombre_estado = row['Nombre_estado']
            estado = session.exec(
                select(Estado).where(Estado.id == id_estado)
            ).first()
            if not estado:
                estado = Estado(id=id_estado, nombre=nombre_estado)
                session.add(estado)
                session.commit()  # Persistir el registro
                session.refresh(estado)
            
            # --- 2. Verificar o insertar Municipio (clave primaria compuesta: estado_id + id_municipio) ---
            estado_id = id_estado
            id_municipio = int(row['ID_municipio'])
            municipio_nombre = row['Municipio']
            municipio = session.exec(
                select(Municipio).where(
                    Municipio.estado_id == estado_id,
                    Municipio.id_municipio == id_municipio
                )
            ).first()
            if not municipio:
                municipio = Municipio(
                    estado_id=estado_id,
                    id_municipio=id_municipio,
                    nombre=municipio_nombre
                )
                session.add(municipio)
                session.commit()
                session.refresh(municipio)
            
            # --- 3. Verificar o insertar Partido ---
            partido_nombre = row['Partido']
            partido = session.exec(
                select(Partido).where(Partido.nombre == partido_nombre)
            ).first()
            if not partido:
                partido = Partido(nombre=partido_nombre)
                session.add(partido)
                session.commit()
                session.refresh(partido)
            
            # --- 4. Insertar el registro del Proceso Electoral Municipal ---
            año = int(row['Año'])
            votos = int(row['Votos'])
            votos_validos = int(row['Votos_validos'])
            votos_candidato_sin_registro = int(row['Votos_candidato_sin_registro'])
            votos_nulos = int(row['Votos_nulos'])
            total_de_votos = int(row['Total_de_votos'])
            lista_nominal = int(row['Lista_nominal'])
            
            # Convertir la columna "Coalición" al valor del Enum
            coalicion_valor = str(row['Coalición']).strip().lower()
            if coalicion_valor in ['sí', 'si']:
                coalicion_enum = CoalicionEnum.SI
            else:
                coalicion_enum = CoalicionEnum.NO
            
            # Crear el registro en ProcesoElectoralMunicipal
            proceso = ProcesoElectoralMunicipal(
                año=año,
                estado_id=estado_id,
                id_municipio=id_municipio,
                partido_id=partido.id,
                votos=votos,
                votos_validos=votos_validos,
                votos_candidato_sin_registro=votos_candidato_sin_registro,
                votos_nulos=votos_nulos,
                total_de_votos=total_de_votos,
                lista_nominal=lista_nominal,
                coalicion=coalicion_enum
            )
            session.add(proceso)
        
        # Commit final para guardar todos los registros
        session.commit()
    print("Datos municipales importados exitosamente.")

if __name__ == "__main__":
    # Ruta del CSV de ayuntamientos
    csv_file = "/home/barea/limpieza/ayuntamientos/{{cookiecutter.project_slug}}/data/final/datos_electorales_2015_2023.csv"
    import_municipales(csv_file)