from marshmallow import Schema, fields

class QuerySchema(Schema):
    """
    Clase para validar el rag.
    """
    query = fields.Str(required=True)  # El usuario debe enviar una consulta
    k = fields.Int(missing=7)  # Valor por defecto si no se especifica


class PlainQueyOllama(Schema):
    """
    Clase para validar el rag.
    """
    query = fields.Str(required=True)  # El usuario debe enviar una consulta