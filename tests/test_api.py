import pytest
from app import createApp

# Configuración del cliente de pruebas
@pytest.fixture
def client():
    app = createApp()
    app.config["TESTING"] = True  # Configurar en modo de pruebas
    with app.test_client() as client:
        yield client

def test_dummy():
    """Prueba inicial de CI/CD"""
    assert 1 == 1

def test_get_tasks(client):
    """Prueba básica para el endpoint GET /tasks/"""
    response = client.get("/tasks/")  # Llama al endpoint
    assert response.status_code == 200  # Verifica que devuelva 200 OK
    assert isinstance(response.json, list)  # Verifica que la respuesta sea una lista
