from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class PropertySchema(Schema):
    # dump_only=True significa que el campo se devuelve en el JSON, pero se ignora al recibir datos
    id = fields.Integer(dump_only=True)
    type = fields.String(required=True, validate=validate.Length(min=3))
    location = fields.String(required=True)
    price = fields.Decimal(required=True, validate=validate.Range(min=0))
    living_space_min = fields.Decimal(required=True)
    living_space_max = fields.Decimal(required=True)
    rooms = fields.Integer(required=True)
    bathrooms = fields.Integer(required=True)
    description = fields.String(validate=validate.Length(max=255))
    client_id = fields.Integer(required=True)
    status_id = fields.Integer(required=True)
    agent_id = fields.Integer(allow_none=True)

    @validates_schema
    def validate_ranges(self, data, **kwargs):
        # Validamos solo la superficie porque el precio ahora es un valor único
        s_min = data.get('living_space_min')
        s_max = data.get('living_space_max')
        if s_min and s_max and s_min > s_max:
            raise ValidationError("La superficie mínima no puede ser mayor a la máxima", "living_space_min")
