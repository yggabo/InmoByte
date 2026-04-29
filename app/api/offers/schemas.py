from marshmallow import Schema, fields, validate

class OfferSchema(Schema):
    id = fields.Integer(dump_only=True)
    offered_price = fields.Decimal(required=True, validate=validate.Range(min=0))
    status = fields.String(dump_only=True)
    property_id = fields.Integer(required=True)
    client_id = fields.Integer(required=True)
    status_id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class OfferStatusUpdateSchema(Schema):
    status_id = fields.Integer(required=True, validate=validate.OneOf([2, 3, 4]))