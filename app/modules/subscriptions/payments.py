import hashlib
import hmac
import os
import re
from urllib.parse import urlparse

import requests
from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import get_current_user, jwt_required

from app import db, logger
from app.modules.subscriptions.service import subscriptionPayment

bp = Blueprint('payment', __name__)


LAHZA_SECRET_KEY = os.getenv('LAHZA_SECRET_KEY', '')
LAHZA_STATUS_URL = os.getenv('LAHZA_STATUS_URL', '')
LAHZA_API_URL = os.getenv('LAHZA_API_URL', '')

raw_ips = os.getenv("LAHZA_ALLOWED_IPS", "")
ALLOWED_IPS = {ip.strip() for ip in raw_ips.split(",") if ip.strip()}

raw_domains = os.getenv("ALLOWED_DOMAINS", "")
ALLOWED_DOMAINS = {domain.strip() for domain in raw_domains.split(",") if domain.strip()}

RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT', 10))

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
        logger.info(f"event: {event}")
        if event.get("event") == "charge.success":
            subscriptionPayment(
                payment_data=event.get("data"),
                db= db
            )
            return jsonify({"message": "Webhook received", "status": "success"}), 200

        return jsonify({"message": event.get("event"), "status": "fail"}), 500

    return jsonify({"error": "Invalid signature"}), 403


@bp.route('/callback', methods=['GET'])
def payment_callback():
    reference = request.args.get('reference')
    return jsonify({"message": "Callback received", "reference":reference})


@bp.route('/verify/<reference>', methods=['GET'])
@jwt_required()
def get_payment_status(reference):
    user = get_current_user()
    if user.role == "admin":
        if not re.match(r'^[A-Za-z0-9_-]+$', reference):
            return jsonify({"error": "Invalid reference format"}), 400

        url = f"{LAHZA_STATUS_URL}{reference}"

        if not validate_domain(url):
            return jsonify({"error": "Untrusted payment provider domain"}), 403

        headers = {"Authorization": f"Bearer {LAHZA_SECRET_KEY}"}
        try:
            response = requests.get(url, headers=headers, timeout=RESPONSE_TIMEOUT)
            return jsonify(response.json()), response.status_code
        except Exception as e:
            logger.error(f"Payment verification error: {str(e)}")
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "you are not admin"}), 400


def validate_domain(url: str) -> bool:
    """Validate that the domain of the given URL is in the allowed list."""
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    return hostname in ALLOWED_DOMAINS