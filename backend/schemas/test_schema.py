from marshmallow import Schema, fields, validate






class PlainChangeModel(Schema):
    index = fields.Int(required=True)

class PlainChangeCategory(Schema):
    category = fields.Str(required=True)

class PlainChangeK(Schema):
    k = fields.Int(required=True)

class PlainChangeLevel(Schema):
    level = fields.Int(required=True)

class PlainQueryCollection(PlainChangeCategory):
    query = fields.Str(required=True)









class QuerySchema(Schema):
    """
    Clase para validar el rag.
    """
    query = fields.Str(required=True)  # El usuario debe enviar una consulta
    k = fields.Int(missing=7)  # Valor por defecto si no se especifica


class PlainQueryUser(Schema):
    query = fields.Str(required=True, validate=validate.Length(min=1),
                       description="La consulta que se enviará al modelo.")
    rag = fields.Int(missing=1, description="El valor de RAG. Si no se proporciona, se usa 1 por defecto.")
    level = fields.Int(missing=0, description="El nivel de respuesta. Si no se proporciona, se usa 0 por defecto.")
    category = fields.Str(required=True, validate=validate.Length(min=1))


class PlainChangeModel(Schema):
    index = fields.Int(required=True)

class PlainQueryRag(Schema):
    query = fields.Str(required=True, validate=validate.Length(min=1))
    category = fields.Str(required=True, validate=validate.Length(min=1))
    k = fields.Int(missing=1, description="El valor de RAG. Si no se proporciona, se usa 1 por defecto.")

