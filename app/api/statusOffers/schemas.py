from marshmallow import Schema, fields, validate, EXCLUDE


class OfferStatusCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=30))
    status = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class OfferStatusUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    name = fields.Str(validate=validate.Length(min=1, max=30))


offer_status_create_schema = OfferStatusCreateSchema()
offer_status_update_schema = OfferStatusUpdateSchema()
