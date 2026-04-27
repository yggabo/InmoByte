from marshmallow import Schema, fields, validate, EXCLUDE, validates_schema, ValidationError


class ClientCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True, validate=validate.Length(max=150))
    phone = fields.Str(validate=validate.Length(max=20))
    address = fields.Str(validate=validate.Length(max=255))
    age = fields.Int(validate=validate.Range(min=0, max=150))
    status = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ClientUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(validate=validate.Length(min=1, max=100))
    email = fields.Email(validate=validate.Length(max=150))
    phone = fields.Str(validate=validate.Length(max=20))
    address = fields.Str(validate=validate.Length(max=255))
    age = fields.Int(validate=validate.Range(min=0, max=150))


client_create_schema = ClientCreateSchema()
client_update_schema = ClientUpdateSchema()