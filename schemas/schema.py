from marshmallow import Schema, fields, validate

class Schema(Schema):
    emailInput = fields.String(required=True, validate=validate.Length(min=1, max=64))
    passwordInput = fields.String(required=True, validate=validate.Length(min=8, max=64))
