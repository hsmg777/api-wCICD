from db import db
from datetime import datetime

class Tarea(db.Model):  
    __tablename__ = 'Tarea'  
    id_tarea = db.Column(db.Integer, primary_key=True)  
    titulo = db.Column(db.String(150), nullable=False)  
    descripcion = db.Column(db.Text, nullable=False) 
    fecha_creacion = db.Column(db.Date, default=datetime.utcnow)  
    estado = db.Column(db.String(100)) 

    def __init__(self, titulo, descripcion, fecha_creacion=None, estado="pendiente"):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion or datetime.utcnow().date()
        self.estado = estado

    