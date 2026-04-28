from marshmallow import Schema, fields, validate, EXCLUDE


class AppointmentCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    appointment_date = fields.Date(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    client_id = fields.Int(required=True)
    property_id = fields.Int(required=True)
    agent_id = fields.Int(required=True)
    status_id = fields.Int(required=False)  # Usually starts with a default status like PROGRAMADA
    notes = fields.Str(validate=validate.Length(max=500))
    is_active = fields.Bool(dump_only=True)
    
    # Camppos para serialización (dump_only)
    client_name = fields.Str(attribute="client.name", dump_only=True)
    property_location = fields.Str(attribute="property.location", dump_only=True)
    status_name = fields.Str(attribute="status.name", dump_only=True)
    
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class AppointmentUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    appointment_date = fields.Date()
    start_time = fields.Time()
    end_time = fields.Time()
    status_id = fields.Int()
    notes = fields.Str(validate=validate.Length(max=500))
    is_active = fields.Bool()


appointment_create_schema = AppointmentCreateSchema()
appointment_update_schema = AppointmentUpdateSchema()
