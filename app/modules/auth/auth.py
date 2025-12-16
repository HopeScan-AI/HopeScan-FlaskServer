import os
from datetime import timedelta

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required, set_access_cookies,
                                unset_access_cookies)
from sqlalchemy.exc import SQLAlchemyError

from app import bcrypt, db
from app.modules.auth.schema import LoginRequest, VerificationRequest
from app.modules.providers.service import get_owners
from app.modules.user.schema import UserCreate
from app.modules.user.service import create, get_user_by_email

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.post("/signup")
def signup_user():
    try:
        user = UserCreate(**request.json)
        email = user.email
        if not email:
            return jsonify({"error": "Email is required"}), 400

        email_exist = get_user_by_email(email, db)
        if email_exist:
            return jsonify({"error": "Email already exists."}), 400

        user.is_verified = True
        db_user = create(user, db, "email")
        return jsonify({"message": "User created successfully!", "data": db_user.as_dict()})
    except SQLAlchemyError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred. {e}"}), 500


@bp.post("/login")
def login_for_access_token():
    try:
        login_data = LoginRequest(**request.json)
        db_user = get_user_by_email(login_data.email, db)
        if not db_user or not bcrypt.check_password_hash(db_user.password, login_data.password):
            return jsonify({"error": "Invalid email or password"}), 401

        if not db_user.is_verified:
            return jsonify({"error": "Account is not verified"}), 401

        access_token = create_access_token(
            identity=db_user,
            expires_delta=timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 180)))
        )
        owners = get_owners(db_user.id, db)
        response = jsonify(access_token=access_token, user=db_user.as_dict())
        set_access_cookies(response, access_token)
        return response
    except Exception as e:
        print(e)
        return jsonify({"error": f"An unexpected error occurred. {e}"}), 500


@bp.post("/logout")
@jwt_required()
def logout():
    response = jsonify({"msg": "Logged out successfully!"})
    unset_access_cookies(response)
    return response, 200


@bp.get('/validate-token')
@jwt_required()
def validate_token():
    user = get_jwt_identity()
    return jsonify({"signed_in": True, "user": user}), 200
