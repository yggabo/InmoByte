from marshmallow import Schema, fields, validate

class OfferTypeEnum:
    COMPRA = "COMPRA"
    ALQUILER = "ALQUILER"


class OfferSchema(Schema):
    id = fields.Integer(dump_only=True)
    type = fields.String(required=True, validate=validate.OneOf([OfferTypeEnum.COMPRA, OfferTypeEnum.ALQUILER]))
    offered_price = fields.Decimal(required=True, validate=validate.Range(min=0))
    status = fields.String(dump_only=True)
    property_id = fields.Integer(required=True)
    client_id = fields.Integer(required=True)
    agent_id = fields.Integer(allow_none=True)
    status_id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class OfferStatusUpdateSchema(Schema):
    status_id = fields.Integer(required=True, validate=validate.OneOf([2, 3, 4]))