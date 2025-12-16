from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_current_user, jwt_required
from pydantic import ValidationError

from app import db
from app.modules.notifications.notification import \
    create as create_notification
from app.modules.notifications.schema import NotificationCreate
from app.modules.providers.schema import ProviderCreate
from app.modules.providers.service import (create, delete, get_all_providers,
                                           get_one_provider, update_provider)
from app.modules.user.service import get_user_by_email

bp = Blueprint('provider', __name__, url_prefix='/provider')

    

@bp.post('/')
@jwt_required()
def create_user():
    try:
        user = get_current_user()
        if user.role == "admin" or user.role == "institution":
            provider_data = ProviderCreate(**request.json)
            provider = get_user_by_email(provider_data.user_email, db)
            if provider:
                create_notification(
                    NotificationCreate(
                        user_id=provider.id, 
                        title="Invite to institution",
                        message=f"Institution {user.name} is inviting you to join them",
                        action_url= f"/provider/join-institution/{user.id}"
                    ),
                    db
                )
                saved_provider = create(user.id, provider.id, db)
                return jsonify(saved_provider.as_dict()), 201
            else:
                return jsonify({"errors": "Provider with this email does not exist"}), 404
        
        return jsonify({"errors": "UNAUTORIZED"}), 401
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

@bp.get('/')
@jwt_required()
def list_providers():
    user = get_current_user()
    if user.role == "admin" or user.role == "institution":
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10000))
        providers = get_all_providers(user.id, db, skip, limit)
        return jsonify(providers)
    return jsonify({"errors": "UNAUTORIZED"}), 401


@bp.post('/respond-invitation')
@jwt_required()
def respond():
    data = request.json
    provider = update_provider(data.get("action"), data.get("provider_id"), data.get("user_id"), db)
    return jsonify(provider.as_dict()), 200

@bp.delete('/<int:provider_id>')
@jwt_required()
def delete_user(provider_id):
    user = get_current_user()
    if user.role == "admin" or user.role == "institution":
        db_provider = delete(provider_id, user.id, db)
        return jsonify({"message": "Provider deleted", "provider": db_provider.as_dict()})
    return jsonify({"errors": "UNAUTORIZED"}), 401