from marshmallow import Schema, fields, validate


class ResponseSchema(Schema):
    status = fields.Str(required=True, validate=validate.OneOf(["success", "success", "error"]))
    message = fields.Str(required=True)
    data = fields.Dict()