import pytest
import sys
import os

# Asegurarnos de que el directorio raíz esté en sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import createApp

# Cliente de pruebas
@pytest.fixture
def client():
    app = createApp()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_all_tasks(client):
    """
    Prueba el endpoint GET /tasks/
    """
    # Simula una solicitud al endpoint
    response = client.get("/tasks/")
    
    # Verifica que el código de estado sea 200
    assert response.status_code == 200

    # Verifica que el cuerpo de la respuesta sea una lista
    assert isinstance(response.json, list)
