from marshmallow import Schema, fields, validate, EXCLUDE


class AgentCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    userProfileId = fields.Int(required=True)
    status = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


agent_create_schema = AgentCreateSchema()