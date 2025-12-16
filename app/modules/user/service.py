from flask import abort

from app import jwt
from app.models import User
from app.modules.user.schema import UserCreate
from app.utils import hash_password


@jwt.user_identity_loader
def user_identity_lookup(user):
    return str(user.id)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

def create(user: UserCreate, db, provider):
    role = user.role if user.role in ("user", "institution") else "user"
    is_exist = get_user_by_email(email=user.email, db=db)
    if is_exist: abort(500, description="User already exist")
    db_user = User(
        name=user.name,
        email=user.email,
        role=role,
        is_verified=user.is_verified,
        password=hash_password(user.password),
        provider=provider
    )
    db.session.add(db_user)
    db.session.commit()
    db.session.refresh(db_user)
    return db_user


def get_all_users(db, skip, limit):
    return db.session.query(User).offset(skip).limit(limit).all()


def get_one_user(user_id, db):
    db_user = db.session.query(User).filter(User.id == user_id).first()
    if db_user is None:
        abort(404, description="User not found")
    return db_user


def get_user_by_email(email, db):
    db_user = db.session.query(User).filter(User.email == email).first()
    return db_user


def set_verification_code(email, code, db):
    db_user = get_user_by_email(email, db)
    if db_user:
        db_user.verification_code = code
        db.session.commit()
        db.session.refresh(db_user)


def get_verification_code(email, db):
    db_user = get_user_by_email(email, db)
    if db_user:
        return db_user.verification_code
    return None


def verify_account(email, db):
    db_user = get_user_by_email(email, db)
    if db_user:
        db_user.is_verified = True
        db.session.commit()
        db.session.refresh(db_user)


def update(user_id, user_data, db):
    db_user = db.session.query(User).filter(User.id == user_id).first()
    if db_user:
        if user_data.name:
            db_user.name = user_data.name
        if user_data.email:
            db_user.email = user_data.email
        if user_data.password:
            db_user.password = user_data.password
        if user_data.role:
            db_user.role = user_data.role
        if user_data.is_verified is not None:
            db_user.is_verified = user_data.is_verified
        if user_data.password:
            db_user.password = hash_password(user_data.password)
        db.session.commit()
        db.session.refresh(db_user)
    else:
        abort(404, description="User not found")
    return db_user


def delete(user_id, db):
    db_user = db.session.query(User).filter(User.id == user_id).first()
    if db_user:
        db.session.delete(db_user)
        db.session.commit()
        return db_user
    else:
        abort(404, description="User not found")
