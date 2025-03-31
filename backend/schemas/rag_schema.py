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

class PlainQueryModel(Schema):
    query = fields.Str(required=True)


