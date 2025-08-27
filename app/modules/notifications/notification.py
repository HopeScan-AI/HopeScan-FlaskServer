from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_current_user
from .service import get_notifications, mark_as_read, create
from app import db

bp = Blueprint('notification', __name__, url_prefix='/notification')


@bp.get('/')
@jwt_required()
def list_users():
    user = get_current_user()
    notifications = get_notifications(user.id, db)
    notifications_dicts = [notification.as_dict() for notification in notifications]
    return jsonify(notifications_dicts)


@bp.post('/<int:notification_id>/mark-read')
@jwt_required()
def mark_read(notification_id):
    user = get_current_user()
    notification = mark_as_read(user.id, notification_id, db)
    return jsonify(notification.as_dict())

