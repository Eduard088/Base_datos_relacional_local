from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_dummy_references():
    # Crear un Estado
    estado_response = client.post("/estados", json={"nombre": "Estado Test"})
    assert estado_response.status_code == 201
    estado_id = estado_response.json()["id"]

    # Crear un Municipio relacionado al Estado
    municipio_response = client.post("/municipios", json={"nombre": "Municipio Test", "estado_id": estado_id})
    assert municipio_response.status_code == 201
    municipio_id = municipio_response.json()["id"]

    # Crear un Partido
    partido_response = client.post("/partidos", json={"nombre": "Partido Test"})
    assert partido_response.status_code == 201
    partido_id = partido_response.json()["id"]

    return estado_id, municipio_id, partido_id

def test_create_proceso():
    _, municipio_id, partido_id = create_dummy_references()
    data = {
        "año": 2023,
        "municipio_id": municipio_id,
        "partido_id": partido_id,
        "votos": 1000,
        "votos_validos": 950,
        "votos_candidato_sin_registro": 5,
        "votos_nulos": 45,
        "total_de_votos": 1000,
        "lista_nominal": 1500,
        "coalicion": "sí"
    }
    response = client.post("/procesos", json=data)
    assert response.status_code == 201, response.text
    json_resp = response.json()
    assert json_resp["año"] == 2023
    assert json_resp["coalicion"] == "sí"

def test_read_proceso():
    _, municipio_id, partido_id = create_dummy_references()
    data = {
        "año": 2023,
        "municipio_id": municipio_id,
        "partido_id": partido_id,
        "votos": 2000,
        "votos_validos": 1900,
        "votos_candidato_sin_registro": 10,
        "votos_nulos": 90,
        "total_de_votos": 2000,
        "lista_nominal": 2500,
        "coalicion": "no"
    }
    create_response = client.post("/procesos", json=data)
    assert create_response.status_code == 201, create_response.text
    proceso_id = create_response.json()["id"]

    get_response = client.get(f"/procesos/{proceso_id}")
    assert get_response.status_code == 200, get_response.text
    json_resp = get_response.json()
    assert json_resp["año"] == 2023