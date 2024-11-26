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


def test_post_task(client):
    """
    Prueba el endpoint POST /tasks/:
    - Verifica que se pueda crear una tarea correctamente.
    - Verifica que los datos de la respuesta coincidan con los enviados.
    """
    # Datos para crear una nueva tarea
    nueva_tarea = {
        "titulo": "Tarea de prueba",
        "descripcion": "Descripción de prueba",
        "estado": "pendiente"
    }

    # Simula una solicitud POST al endpoint
    response = client.post("/tasks/", json=nueva_tarea)
    
    # Verifica que el código de estado sea 201 (Creado)
    assert response.status_code == 201

    # Verifica que los datos de la respuesta coincidan con los enviados
    response_json = response.json
    assert response_json["titulo"] == nueva_tarea["titulo"]
    assert response_json["descripcion"] == nueva_tarea["descripcion"]
    assert response_json["estado"] == nueva_tarea["estado"]

