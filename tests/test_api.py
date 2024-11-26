import pytest
import sys
import os

# Asegurarnos de que el directorio raíz esté en sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import createApp
from db import db

# Cliente de pruebas
@pytest.fixture
def client():
    # Crear la aplicación en modo de pruebas
    app = createApp(testing=True)  # Usar modo de prueba con SQLite
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            # Crear todas las tablas en la base de datos en memoria
            db.create_all()
        yield client  # Proporcionar el cliente para las pruebas

def test_get_all_tasks(client):
    """
    Prueba el endpoint GET /tasks/
    """
    # Simula una solicitud al endpoint
    response = client.get("/tasks/")
    
    # Verifica que el código de estado sea 200
    assert response.status_code == 200

    # Verifica que el cuerpo de la respuesta sea una lista (puede estar vacía)
    assert isinstance(response.json, list)
