import pytest
from app import createApp

# Configuración del cliente de pruebas
@pytest.fixture
def client():
    app = createApp()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# **Test 1: GET /tasks/** (Obtener todas las tareas)
def test_get_tasks(client):
    """Prueba el endpoint GET /tasks/"""
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Verificar que devuelve una lista

# **Test 2: POST /tasks/** (Crear una tarea)
def test_post_task(client):
    """Prueba el endpoint POST /tasks/"""
    data = {"titulo": "Tarea de prueba", "descripcion": "Descripción de prueba", "estado": "pendiente"}
    response = client.post("/tasks/", json=data)
    assert response.status_code == 201
    assert response.json["titulo"] == "Tarea de prueba"

# **Test 3: GET /tasks/<id>** (Obtener tarea por ID)
def test_get_task_by_id(client):
    """Prueba el endpoint GET /tasks/<id>"""
    # Crear una tarea primero
    data = {"titulo": "Tarea individual", "descripcion": "Prueba de obtener por ID", "estado": "pendiente"}
    post_response = client.post("/tasks/", json=data)
    task_id = post_response.json["id_tarea"]

    # Obtener la tarea creada
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json["titulo"] == "Tarea individual"

# **Test 4: PUT /tasks/<id>** (Actualizar una tarea)
def test_update_task(client):
    """Prueba el endpoint PUT /tasks/<id>"""
    # Crear una tarea primero
    data = {"titulo": "Tarea original", "descripcion": "Prueba de actualizar", "estado": "pendiente"}
    post_response = client.post("/tasks/", json=data)
    task_id = post_response.json["id_tarea"]

    # Actualizar la tarea creada
    updated_data = {"titulo": "Tarea actualizada", "descripcion": "Actualización realizada", "estado": "completada"}
    response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json["titulo"] == "Tarea actualizada"

# **Test 5: DELETE /tasks/<id>** (Eliminar una tarea)
def test_delete_task(client):
    """Prueba el endpoint DELETE /tasks/<id>"""
    # Crear una tarea primero
    data = {"titulo": "Tarea para eliminar", "descripcion": "Prueba de eliminación", "estado": "pendiente"}
    post_response = client.post("/tasks/", json=data)
    task_id = post_response.json["id_tarea"]

    # Eliminar la tarea creada
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert "Tarea con ID" in response.json["message"]
