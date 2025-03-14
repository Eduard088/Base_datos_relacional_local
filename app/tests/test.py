from fastapi.testclient import TestClient
from app.main import app

def test_client():
    client = TestClient(app)
    assert isinstance(client, TestClient)