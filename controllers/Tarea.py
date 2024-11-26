from flask_smorest import Blueprint
from flask import jsonify
from models.Tarea import Tarea, db
from schemas.TareaSchema import TareaSchema

blp = Blueprint("tareas", __name__, url_prefix="/tasks", description="Operaciones CRUD para tareas")

tarea_schema = TareaSchema()
tareas_schema = TareaSchema(many=True)


# (POST)**
@blp.route("/", methods=["POST"])
@blp.arguments(TareaSchema)  
@blp.response(201, TareaSchema)
def create_task(data):
    """Crea una nueva tarea"""
    nueva_tarea = Tarea(**data)
    db.session.add(nueva_tarea)
    db.session.commit()
    return nueva_tarea



# (GET)**
@blp.route("/", methods=["GET"])
@blp.response(200, TareaSchema(many=True))
def get_tasks():
    """Obtiene todas las tareas"""
    tareas = Tarea.query.all()
    return tareas

# ID (GET)**
@blp.route("/<int:id_tarea>", methods=["GET"])
@blp.response(200, TareaSchema)
def get_task_by_id(id_tarea):
    """Obtiene una tarea específica por su ID"""
    tarea = Tarea.query.get_or_404(id_tarea)
    return tarea


# (PATCH)**
@blp.route("/<int:id_tarea>", methods=["PUT"])
@blp.arguments(TareaSchema)
@blp.response(200, TareaSchema)
def update_task(data, id_tarea):
    """Actualiza una tarea específica por su ID"""
    tarea = Tarea.query.get_or_404(id_tarea)
    if "titulo" in data:
        tarea.titulo = data["titulo"]
    if "descripcion" in data:
        tarea.descripcion = data["descripcion"]
    if "estado" in data:
        tarea.estado = data["estado"]
    db.session.commit()
    return tarea



# (DELETE)**
@blp.route("/<int:id_tarea>", methods=["DELETE"])
@blp.response(200, dict)
def delete_task(id_tarea):
    """
    Elimina una tarea específica por su ID.
    """
    tarea = Tarea.query.get_or_404(id_tarea, description=f"Tarea con ID {id_tarea} no encontrada.")

    try:
        db.session.delete(tarea)
        db.session.commit()
        return jsonify({"message": f"Tarea con ID {id_tarea} eliminada exitosamente."})
    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": f"Error al eliminar la tarea: {str(e)}"}), 500
