from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class PropertySchema(Schema):
    # dump_only=True significa que el campo se devuelve en el JSON, pero se ignora al recibir datos
    id = fields.Integer(dump_only=True)
    type = fields.String(required=True, validate=validate.Length(min=3))
    location = fields.String(required=True)
    price_min = fields.Decimal(required=True, validate=validate.Range(min=0))
    price_max = fields.Decimal(required=True, validate=validate.Range(min=0))
    living_space = fields.Decimal(required=True)
    rooms = fields.Integer(required=True)
    bathrooms = fields.Integer(required=True)
    description = fields.String(validate=validate.Length(max=255))
    
    # Campos para recibir al crear/actualizar
    client_id = fields.Integer(required=True)
    status_id = fields.Integer(required=True)
    agent_id = fields.Integer(allow_none=True)
    
    # Campos para devolver (computed fields from to_dict())
    client = fields.Function(lambda obj: obj.client.to_dict() if obj.client else None)
    status = fields.Function(lambda obj: obj.status.to_dict() if obj.status else None)
    agent = fields.Function(lambda obj: obj.agent.to_dict() if obj.agent else None)

    @validates_schema
    def validate_ranges(self, data, **kwargs):
        # Solo validamos si ambos campos están presentes (útil para actualizaciones parciales)
        p_min = data.get('price_min')
        p_max = data.get('price_max')
        if p_min and p_max and p_min > p_max:
            raise ValidationError("El precio mínimo no puede ser mayor al máximo", "price_min")
