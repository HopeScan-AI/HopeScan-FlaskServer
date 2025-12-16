import os

import requests
from flask import Blueprint, jsonify, redirect, request
from flask_jwt_extended import get_current_user, jwt_required

from app import db, logger
from app.modules.subscriptions.payments import LAHZA_API_URL, LAHZA_SECRET_KEY
from app.modules.subscriptions.schema import *
from app.modules.subscriptions.service import *

bp = Blueprint('subscription', __name__, url_prefix='/subscription')
RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT', 10))

@bp.post('/subscribe')
@jwt_required()
def subscribe():
    try:
        subscribe_data = PaymentCreate(**request.json)
        user = get_current_user()
        currency = "USD"

        payload = {
            "amount": subscribe_data.amount * 100,
            "currency": currency,
            "email": user.email,
            "callback_url": "https://hopescan.ai/payment/callback",
            "metadata": {
                "user_id": user.id,
                "plan_id": subscribe_data.plan_id,
                "plan_type_id": subscribe_data.plan_type_id
            }
        }

        headers = {
            "Authorization": f"Bearer {LAHZA_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(LAHZA_API_URL, json=payload, headers=headers, timeout=RESPONSE_TIMEOUT)
        logger.info(f"response: {response}")
        if not response.ok:
            logger.error("Failed to initialize payment", str(response.text))
            return jsonify({"error": "Failed to initialize payment", "details": response.text}), 400

        resp_json = response.json()
        payment_url = resp_json["data"]["authorization_url"]
        logger.info(f"payment_url: {payment_url}")
        return redirect(payment_url)

    except Exception as e:
        logger.error("Error in /subscribe", str(e))
        return jsonify({"errors": str(e)}), 500


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
        subscription = getSubscription(subscription_id, db)
        if user.role == "admin" or subscription.user_id == user.id:
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
