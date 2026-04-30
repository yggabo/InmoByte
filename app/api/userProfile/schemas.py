from marshmallow import Schema, fields, validate, EXCLUDE


class UserProfileSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=100))
    lastNames = fields.Str(required=True, validate=validate.Length(max=150))
    telefono = fields.Str(validate=validate.Length(max=20))
    rolId = fields.Int(required=True)
    userId = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserProfileUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(validate=validate.Length(max=100))
    lastNames = fields.Str(validate=validate.Length(max=150))
    telefono = fields.Str(validate=validate.Length(max=20))
    rolId = fields.Int()


user_profile_schema = UserProfileSchema()
user_profiles_schema = UserProfileSchema(many=True)
user_profile_update_schema = UserProfileUpdateSchema()