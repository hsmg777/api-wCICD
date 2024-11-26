def test_crud_operations(client):
    """
    Test integral para las operaciones CRUD:
    - Crea una tarea (POST).
    - Verifica que aparece en la lista de tareas (GET ALL).
    - Obtiene la tarea por su ID (GET BY ID).
    - Actualiza la tarea (PUT).
    - Elimina la tarea (DELETE).
    - Verifica que ya no existe (GET BY ID después de DELETE).
    """
    # Datos para crear una nueva tarea
    nueva_tarea = {
        "titulo": "Tarea completa",
        "descripcion": "Descripción completa",
        "estado": "pendiente"
    }

    # 1. Crear una tarea
    post_response = client.post("/tasks/", json=nueva_tarea)
    assert post_response.status_code == 201  # Verifica que se creó correctamente
    task_id = post_response.json["id_tarea"]  # Obtén el ID de la tarea creada

    # 2. Verificar que la tarea aparece en la lista (GET ALL)
    get_all_response = client.get("/tasks/")
    assert get_all_response.status_code == 200  # Verifica el código de estado
    tareas = get_all_response.json
    assert len(tareas) > 0  # Verifica que la lista no esté vacía
    assert any(tarea["id_tarea"] == task_id for tarea in tareas)  # Verifica que la tarea creada esté en la lista

    # 3. Obtener la tarea por su ID (GET BY ID)
    get_by_id_response = client.get(f"/tasks/{task_id}")
    assert get_by_id_response.status_code == 200  # Verifica el código de estado
    tarea = get_by_id_response.json
    assert tarea["titulo"] == nueva_tarea["titulo"]
    assert tarea["descripcion"] == nueva_tarea["descripcion"]
    assert tarea["estado"] == nueva_tarea["estado"]

    # 4. Actualizar la tarea (PUT)
    datos_actualizados = {
        "titulo": "Tarea actualizada",
        "descripcion": "Descripción actualizada",
        "estado": "completada"
    }
    put_response = client.put(f"/tasks/{task_id}", json=datos_actualizados)
    assert put_response.status_code == 200  # Verifica el código de estado
    tarea_actualizada = put_response.json
    assert tarea_actualizada["titulo"] == datos_actualizados["titulo"]
    assert tarea_actualizada["descripcion"] == datos_actualizados["descripcion"]
    assert tarea_actualizada["estado"] == datos_actualizados["estado"]

    # 5. Eliminar la tarea (DELETE)
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200  # Verifica el código de estado

    # 6. Verificar que la tarea ya no existe (GET BY ID después de DELETE)
    get_after_delete_response = client.get(f"/tasks/{task_id}")
    assert get_after_delete_response.status_code == 404  # Verifica que ya no existe
