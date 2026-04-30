from app.core.extensions import db
from app.api.userProfile.models import UserProfile
from app.api.roles.models import Roles
from app.api.auth.models import Users


def get_all_user_profiles():
    return UserProfile.query.all()


def get_user_profile_by_id(profile_id):
    return UserProfile.query.filter(UserProfile.id == profile_id).first()


def get_user_profile_by_user_id(user_id):
    return UserProfile.query.filter(UserProfile.userId == user_id).first()


def create_user_profile(data):
    if 'name' not in data or 'lastNames' not in data or 'rolId' not in data or 'userId' not in data:
        return None

    existing_user = db.session.get(Users, data['userId'])
    if not existing_user:
        return None

    existing_role = db.session.get(Roles, data['rolId'])
    if not existing_role:
        return None

    existing_profile = UserProfile.query.filter(UserProfile.userId == data['userId']).first()
    if existing_profile:
        return False

    profile = UserProfile(
        name=data['name'],
        lastNames=data['lastNames'],
        telefono=data.get('telefono'),
        rolId=data['rolId'],
        userId=data['userId']
    )
    db.session.add(profile)
    db.session.commit()
    return profile


def update_user_profile(profile_id, data):
    profile = db.session.get(UserProfile, profile_id)
    if not profile:
        return None

    if 'name' in data:
        profile.name = data['name']
    if 'lastNames' in data:
        profile.lastNames = data['lastNames']
    if 'telefono' in data:
        profile.telefono = data['telefono']
    if 'rolId' in data:
        existing_role = db.session.get(Roles, data['rolId'])
        if not existing_role:
            return False
        profile.rolId = data['rolId']

    db.session.commit()
    return profile


def delete_user_profile(profile_id):
    profile = db.session.get(UserProfile, profile_id)
    if not profile:
        return None

    db.session.delete(profile)
    db.session.commit()
    return profile