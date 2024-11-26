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

def test_get_task_by_id(client):
    """
    Prueba el endpoint GET /tasks/<id>:
    - Verifica que se pueda obtener una tarea específica por su ID.
    """
    
    nueva_tarea = {
        "titulo": "Tarea específica",
        "descripcion": "Descripción específica",
        "estado": "pendiente"
    }

    
    post_response = client.post("/tasks/", json=nueva_tarea)
    assert post_response.status_code == 201  
    task_id = post_response.json["id_tarea"]  

    
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200  

    response_json = get_response.json
    assert response_json["titulo"] == nueva_tarea["titulo"]
    assert response_json["descripcion"] == nueva_tarea["descripcion"]
    assert response_json["estado"] == nueva_tarea["estado"]
