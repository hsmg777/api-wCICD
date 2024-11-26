import pytest
from app import createApp

@pytest.fixture
def client():
    app = createApp()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_tasks(client):
    response = client.get("/tasks/")
    assert response.status_code == 200

def test_post_task(client):
    response = client.post("/tasks/", json={"titulo": "Prueba", "descripcion": "Descripción de prueba"})
    assert response.status_code == 201
