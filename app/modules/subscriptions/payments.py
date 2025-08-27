import hashlib
import hmac
import os
import requests
from flask import request, Blueprint, jsonify, abort
from .service import subscriptionPayment
from app import db

bp = Blueprint('payment', __name__)


# @bp.route('/webhook', methods=['POST'])
# def handle_webhook():
#     data = request.get_json()
#     # Process the data or perform desired actions
#     # ...
#     return '200 OK'

LAHZA_SECRET_KEY = os.getenv('LAHZA_SECRET_KEY')
LAHZA_STATUS_URL = "https://api.lahza.io/transaction/verify/"


ALLOWED_IPS = {"161.35.20.140", "165.227.134.20"}

def ip_whitelist(f):
    def decorated_function(*args, **kwargs):
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        if client_ip not in ALLOWED_IPS:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/webhook', methods=['POST'])
@ip_whitelist
def handle_webhook():
    payload = request.get_data()
    signature = request.headers.get('x_lahza_signature')

    hmac_digest = hmac.new(LAHZA_SECRET_KEY.encode(), payload, hashlib.sha256).hexdigest()
    if hmac.compare_digest(hmac_digest, signature):
        event = request.get_json()
        if event.event == "charge.success":
            subscriptionPayment(
                payment_data=event.data,
                db= db
            )
            return jsonify({"message": "Webhook received", "status": "success"}), 200

        return jsonify({"message": event.event, "status": "fail"}), 500

    return jsonify({"error": "Invalid signature"}), 403


# @bp.route('/payment-callback', methods=['GET'])
# def payment_callback():
#     reference = request.args.get('reference')
#     # Process and verify payment
#     payment_id = data.get("payment_id")
#     status = data.get("status")
#     print("*"*100)
#     print(request)
#     print("*"*100)
#     # Store payment status in your database (not implemented here)
#     return jsonify({"message": "Callback received", "payment_id": payment_id, "status": status})

@bp.route('/verify/<reference>', methods=['GET'])
def get_payment_status(reference):
    headers = {"Authorization": f"Bearer {LAHZA_SECRET_KEY}"}
    try:
        response = requests.get(f"{LAHZA_STATUS_URL}{reference}", headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


