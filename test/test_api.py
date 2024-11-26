import pytest
from app import createApp

@pytest.fixture
def client():
    app = createApp()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_tasks(client):
    """Prueba el endpoint GET /tasks/"""
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_post_task(client):
    """Prueba el endpoint POST /tasks/"""
    response = client.post("/tasks/", json={"titulo": "Prueba", "descripcion": "Tarea de prueba"})
    assert response.status_code == 201
    assert response.json["titulo"] == "Prueba"
