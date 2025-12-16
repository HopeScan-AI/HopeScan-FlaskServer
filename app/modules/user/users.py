from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_current_user, jwt_required
from pydantic import ValidationError

from app import db
from app.modules.user.schema import UserCreate, UserUpdate
from app.modules.user.service import (create, delete, get_all_users,
                                               get_one_user, update)

bp = Blueprint('user', __name__, url_prefix='/user')    



@bp.post('/')
@jwt_required()
def create_user():
    try:
        user = get_current_user()
        if user.role == "admin":
            user_data = UserCreate(**request.json)
            saved_user = create(user_data, db, provider="email")
            return jsonify(saved_user.as_dict()), 201
        else:
            return jsonify({"errors": "UNAUTORIZED"}), 401
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

@bp.get('/')
@jwt_required()
def list_users():
    user = get_current_user()
    if user.role == "admin":
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10000))
        users = get_all_users(db, skip, limit)
        user_dicts = [user.as_dict() for user in users]
        return jsonify(user_dicts)
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401


@bp.get('/<int:user_id>')
@jwt_required()
def get_user(user_id):
    user = get_current_user()
    if user.role == "admin":
        db_user = get_one_user(user_id, db)
        return jsonify(db_user.as_dict())
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401

@bp.put('/<int:user_id>')
@jwt_required()
def update_user(user_id):
    user = get_current_user()
    if user.role == "admin":
        user_data = UserUpdate(**request.json)
        db_user = update(user_id, user_data, db)
        return jsonify(db_user.as_dict())
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401
    
@bp.delete('/<int:user_id>')
@jwt_required()
def delete_user(user_id):
    user = get_current_user()
    if user.role == "admin":
        db_user = delete(user_id, db)
        return jsonify({"message": "User deleted", "user": db_user.as_dict()})
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401