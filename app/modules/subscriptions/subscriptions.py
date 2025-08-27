from flask import Blueprint, request, jsonify
from .schema import *
from app import db, logger
from .service import *
from flask_jwt_extended import jwt_required, get_current_user
 


bp = Blueprint('subscription', __name__, url_prefix='/subscription')

@bp.post('/')
@jwt_required()
def create_subscription():
    try:
        user = get_current_user()
        if user.role == "admin":
            subscription_data = SubscriptionCreate(**request.json)
            saved_subscription = createSubscription(subscription_data, db, subscription_data.user_id)
            return jsonify(saved_subscription.as_dict()), 201
        else:
            return jsonify({"errors": "UNAUTORIZED"}), 401
    except Exception as e:
        return jsonify({"errors": e.__str__()}), 500


@bp.get('/')
@jwt_required()
def get_subscriptions():
    try:
        user = get_current_user()
        if user.role == "admin":
            subscriptions = getSubscriptions(db)
            
            return jsonify(subscriptions), 200
        else:
            return jsonify({"errors": "UNAUTORIZED"}), 401
    except Exception as e:
        return jsonify({"errors": e.__str__()}), 500

@bp.get('/<int:subscription_id>')
@jwt_required()
def get_subscription(subscription_id):
    try:
        user = get_current_user()
        if user.role == "admin":
            subscription = getSubscription(subscription_id, db)
            
            return jsonify(subscription), 200
        else:
            return jsonify({"errors": "UNAUTORIZED"}), 401
    except Exception as e:
        return jsonify({"errors": e.__str__()}), 500
    

@bp.put('/<int:subscription_id>')
@jwt_required()
def update_subscription(subscription_id):
    try:
        user = get_current_user()
        sub_data = SubscriptionUpdate(**request.json)
        if user.role == "admin":
            updated_subscription = updateSubscription(subscription_id, sub_data, db)
            return jsonify({"subscription": updated_subscription.as_dict()}), 200
        else:
            return jsonify({"errors": "UNAUTORIZED"}), 401
    except Exception as e:
        return jsonify({"errors": e.__str__()}), 500

@bp.delete('/<int:subscription_id>')
@jwt_required()
def delete_subscription(subscription_id):
    try:
        user = get_current_user()
        if user.role == "admin":
            db_subscription = deleteSubscription(subscription_id, db)
            return jsonify({"message": "subscription deleted", "subscription": db_subscription.as_dict()})
        else:
            return jsonify({"errors": "UNAUTORIZED"}), 401
    except Exception as e:
        return jsonify({"errors": e.__str__()}), 500
