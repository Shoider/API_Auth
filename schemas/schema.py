from marshmallow import Schema, fields, ValidationError

class Schema(Schema):
    emailInput = fields.String(required=True)
    passwordInput = fields.String(required=True)
    token = fields.String(required=False)
