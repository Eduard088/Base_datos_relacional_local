# Proyecto de Base de Datos Relacional para Procesos Electorales Municipales y Congresos Locales en México

## Descripción

Este proyecto implementa una base de datos relacional enfocada en la normalización y almacenamiento de datos electorales de los procesos municipales y congresos locales en México. Utiliza **Python 3.9.21** y el framework **FastAPI [standard]** para la gestión y exposición de datos a través de servicios web RESTful.

Se estructura en módulos para facilitar la importación, consulta y administración de la información electoral.

## Requisitos

- **Python 3.9.21**
- **FastAPI [standard]**
- **SQLite3**
- **Dependencias adicionales** (ver archivo `requirements.txt` si aplica)

## Estructura del Proyecto

```
project_root/
├── db.py                         # Configuración y conexión a la base de datos
├── electoral.sqlite3              # Archivo de la base de datos SQLite3
├── import_data_congresos.py       # Script de importación de datos de congresos locales
├── import_data_municipales.py     # Script de importación de datos de procesos municipales
├── models.py                      # Definición de modelos de datos
│
├── app/                           # Aplicación FastAPI
│   ├── __init__.py
│   ├── main.py                    # Punto de entrada de la API
│   ├── routers/                    # Definición de endpoints
│   │   ├── __init__.py
│   │   ├── congresos.py            # Endpoints para congresos locales
│   │   ├── estados.py              # Endpoints para entidades federativas
│   │   ├── municipales.py          # Endpoints para procesos municipales
│   │   ├── municipios.py           # Endpoints para municipios
│   │   ├── partidos.py             # Endpoints para partidos políticos
│   │
│   ├── tests/                      # Pruebas del sistema
│       ├── __init__.py
│       ├── test.py                  # Pruebas generales
│       ├── test_procesos.py          # Pruebas específicas de procesos electorales
```

## Instalación y Configuración

1. **Clonar el repositorio:**
    ```sh
    git clone https://github.com/usuario/proyecto-electoral.git
    cd proyecto-electoral
    ```
2. **Instalar dependencias:**
    ```sh
    pip install -r requirements.txt
    ```
3. **Ejecutar la API:**
    ```sh
    uvicorn app.main:app --reload
    ```

## Uso de la API

Una vez que la API esté en ejecución, los endpoints estarán disponibles en:
- Documentación interactiva: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Documentación en formato OpenAPI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Contribuciones

Las contribuciones son bienvenidas. Para reportar errores o sugerir mejoras, por favor abre un issue en el repositorio o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Para más detalles, consulta el archivo `LICENSE`.

## Contacto

Para cualquier consulta o colaboración, puedes contactar al autor en: **eduardobareapoot@outlook.com**.