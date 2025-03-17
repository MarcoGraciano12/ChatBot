from marshmallow import Schema, fields

class PlainTestSchema(Schema):
    name = fields.Str(required=True)