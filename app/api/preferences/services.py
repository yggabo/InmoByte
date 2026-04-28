from app.api.preferences.models import Preference
from app.core.extensions import db
from app.core.exceptions import APIException


class PreferenceService:
    @staticmethod
    def create_preference(client_id, data):
        existing = Preference.query.filter_by(client_id=client_id).first()
        if existing:
            raise APIException("Preferences already exist for this client", status_code=409)

        preference = Preference(
            client_id=client_id,
            property_type_id=data.get('property_type_id'),
            price=data.get('price'),
            location=data.get('location'),
            bedrooms=data.get('bedrooms'),
            bathrooms=data.get('bathrooms'),
            additional_features=data.get('additional_features'),
            living_space_min=data.get('living_space_min'),
            living_space_max=data.get('living_space_max')
        )
        db.session.add(preference)
        db.session.commit()
        return preference

    @staticmethod
    def get_preference_by_client(client_id):
        preference = Preference.query.filter_by(client_id=client_id).first()
        if not preference:
            raise APIException("Preferences not found", status_code=404)
        return preference

    @staticmethod
    def update_preference(client_id, data):
        preference = Preference.query.filter_by(client_id=client_id).first()
        if not preference:
            raise APIException("Preferences not found", status_code=404)

        if 'property_type_id' in data:
            preference.property_type_id = data['property_type_id']
        if 'price' in data:
            preference.price = data['price']
        if 'location' in data:
            preference.location = data['location']
        if 'bedrooms' in data:
            preference.bedrooms = data['bedrooms']
        if 'bathrooms' in data:
            preference.bathrooms = data['bathrooms']
        if 'additional_features' in data:
            preference.additional_features = data['additional_features']
        if 'living_space_min' in data:
            preference.living_space_min = data['living_space_min']
        if 'living_space_max' in data:
            preference.living_space_max = data['living_space_max']

        db.session.commit()
        return preference