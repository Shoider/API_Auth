from marshmallow import Schema, fields

class Schema(Schema):
    emailInput = fields.String(required=True)
    passwordInput = fields.String(required=True)
    privilegesInput =fields.String(required=False)
    token = fields.String(required=False)
