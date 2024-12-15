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

def test_update_task(client):
    """
    Prueba el endpoint PUT /tasks/<id>:
    - Verifica que se pueda actualizar una tarea específica por su ID.
    - Verifica que los datos actualizados se reflejen correctamente.
    """

    nueva_tarea = {
        "titulo": "Tarea original",
        "descripcion": "Descripción original",
        "estado": "pendiente"
    }

    post_response = client.post("/tasks/", json=nueva_tarea)
    assert post_response.status_code == 201  
    task_id = post_response.json["id_tarea"]  

    datos_actualizados = {
        "titulo": "Tarea actualizada",
        "descripcion": "Descripción actualizada",
        "estado": "completada"
    }

    put_response = client.put(f"/tasks/{task_id}", json=datos_actualizados)
    assert put_response.status_code == 200  

    response_json = put_response.json
    assert response_json["titulo"] == datos_actualizados["titulo"]
    assert response_json["descripcion"] == datos_actualizados["descripcion"]
    assert response_json["estado"] == datos_actualizados["estado"]

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json["titulo"] == datos_actualizados["titulo"]
    assert get_response.json["descripcion"] == datos_actualizados["descripcion"]
    assert get_response.json["estado"] == datos_actualizados["estado"]
