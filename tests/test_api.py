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

def test_delete_task(client):
    """
    Prueba el endpoint DELETE /tasks/<id>:
    - Verifica que se pueda eliminar una tarea específica por su ID.
    - Verifica que la tarea ya no exista después de ser eliminada.
    """
    
    nueva_tarea = {
        "titulo": "Tarea para eliminar",
        "descripcion": "Descripción para eliminar",
        "estado": "pendiente"
    }

    
    post_response = client.post("/tasks/", json=nueva_tarea)
    assert post_response.status_code == 201  
    task_id = post_response.json["id_tarea"]  

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200  

    
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404 
