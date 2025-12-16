from flask import abort
from sqlalchemy.orm import joinedload

from app.models import HealthProvider
from app.modules.providers.schema import ProviderCreate


def create(user_id, provider_id, db):
    provider_exists = get_one_provider(provider_id, user_id, db)
    if provider_exists:
        abort(400, description="Provider already exists")
    else:
        db_provider = HealthProvider(
            user_id=user_id,
            provider_id=provider_id,
            status="pending"
        )
        db.session.add(db_provider)
        db.session.commit()
        db.session.refresh(db_provider)
        return db_provider


def get_all_providers(user_id, db, skip, limit):
    providers = db.session.query(HealthProvider) \
        .options(joinedload(HealthProvider.provider)) \
        .filter(HealthProvider.user_id == user_id) \
        .offset(skip) \
        .limit(limit) \
        .all()

    return [
        {**provider.as_dict(), 'provider': provider.provider.as_dict()}
        for provider in providers
    ]


def get_one_provider_without_user(provider_id, db):
    db_provider = db.session.query(HealthProvider).options(joinedload(HealthProvider.user)).filter(HealthProvider.provider_id == provider_id).first()
    return db_provider

def get_one_provider(provider_id, user_id, db):
    db_provider = db.session.query(HealthProvider).options(joinedload(HealthProvider.user))\
    .filter(HealthProvider.user_id == user_id)\
    .filter(HealthProvider.provider_id == provider_id)\
    .first()
    return db_provider

def get_owners(provider_id, db):
    owners = db.session.query(HealthProvider).options(joinedload(HealthProvider.user))\
    .filter(HealthProvider.provider_id == provider_id)\
    .filter(HealthProvider.status == 'accepted')\
    .all()
    
    return [
        owner.as_dict() for owner in owners
    ]

def update_provider(action, provider_id, user_id, db):
    db_provider = db.session.query(HealthProvider).options(joinedload(HealthProvider.user)).filter(HealthProvider.user_id == user_id).filter(HealthProvider.provider_id == provider_id).first()
    if db_provider:
        db_provider.status = action
        db.session.commit()
        db.session.refresh(db_provider)
    else:
        abort(404, description="Provider not found")
    return db_provider

def delete(provider_id, user_id, db):
    db_provider = db.session.query(HealthProvider).filter(HealthProvider.user_id == user_id).filter(HealthProvider.id == provider_id).first()
    if db_provider:
        db.session.delete(db_provider)
        db.session.commit()
        return db_provider
    else:
        abort(404, description="Provider not found")


def is_provider(provider_id, user_id, db):
    db_provider = db.session.query(HealthProvider)\
    .filter(HealthProvider.user_id == user_id)\
    .filter(HealthProvider.provider_id == provider_id).first()
    if db_provider:
        return True 
    else:
        return False