from app.api.filters_properties.models import Property
from app.core.extensions import db

class PropertyService:
    @staticmethod
    def get_filter_options():
        """
        Get distinct values for filter dropdowns.
        """
        from app.api.propertyStatus.models import PropertyStatus
        types = db.session.query(Property.type).filter(Property.type != None).distinct().all()
        locations = db.session.query(Property.location).filter(Property.location != None).distinct().all()
        statuses = db.session.query(PropertyStatus).all()
        
        return {
            'types': sorted([t[0] for t in types if t[0]]),
            'locations': sorted([l[0] for l in locations if l[0]]),
            'statuses': [{'id': s.id, 'name': s.name} for s in statuses]
        }

    @staticmethod
    def get_filtered_properties(filters):
        """
        Search properties based on various filters with priority for 'type' and 'location'.
        Priority filters are applied first to the query builder.
        """
        query = Property.query

        # 1. First apply priority filters if they exist
        if filters.get('type'):
            query = query.filter(Property.type == filters['type'])
        
        if filters.get('location'):
            query = query.filter(Property.location.ilike(f"%{filters['location']}%"))

        # 2. Then apply secondary filters
        if filters.get('status-ID'):
            query = query.filter(Property.status_id == filters['status-ID'])

        if filters.get('min_price'):
            try:
                min_price = float(filters['min_price'])
                # Filtrar propiedades donde price_min está dentro del rango solicitado
                query = query.filter(Property.price_min >= min_price)
            except (ValueError, TypeError):
                pass
            
        if filters.get('max_price'):
            try:
                max_price = float(filters['max_price'])
                # Filtrar propiedades donde price_min está dentro del rango solicitado
                query = query.filter(Property.price_min <= max_price)
            except (ValueError, TypeError):
                pass
            
        if filters.get('living_space_min'):
            try:
                min_space = float(filters['living_space_min'])
                query = query.filter(Property.living_space >= min_space)
            except (ValueError, TypeError):
                pass

        if filters.get('living_space_max'):
            try:
                max_space = float(filters['living_space_max'])
                query = query.filter(Property.living_space <= max_space)
            except (ValueError, TypeError):
                pass
            
        if filters.get('rooms'):
            try:
                query = query.filter(Property.rooms >= int(filters['rooms']))
            except (ValueError, TypeError):
                pass
            
        if filters.get('bathrooms'):
            try:
                query = query.filter(Property.bathrooms >= int(filters['bathrooms']))
            except (ValueError, TypeError):
                pass

        return query.all()

    @staticmethod
    def get_property_by_id(property_id):
        """
        Get a specific property by ID.
        """
        return db.session.get(Property, property_id)

    @staticmethod
    def create_property(data):
        """
        Create a new property record.
        Mapping keys if necessary.
        """
        # Minor mapping if key names in JSON don't match model exactly
        if 'status-ID' in data:
            data['status_id'] = data.pop('status-ID')
            
        new_property = Property(**data)
        db.session.add(new_property)
        db.session.commit()
        return new_property
