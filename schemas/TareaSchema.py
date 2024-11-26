from marshmallow import Schema, fields

class TareaSchema(Schema):
    id_tarea = fields.Int(dump_only=True)  
    titulo = fields.Str(required=True)  
    descripcion = fields.Str(required=True) 
    fecha_creacion = fields.Date(dump_only=True)  
    estado = fields.Str(required=True) 
