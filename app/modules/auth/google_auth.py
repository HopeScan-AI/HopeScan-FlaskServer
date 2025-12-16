import json
import os
from datetime import timedelta
from urllib.parse import urlencode

import requests
from flask import Blueprint, jsonify, make_response, redirect, request
from flask_jwt_extended import create_access_token, set_access_cookies

from app import db
from app.modules.user.schema import UserCreate
from app.modules.user.service import create, get_user_by_email

bp = Blueprint('auth_google', __name__, url_prefix='/auth/google')

GOOGLE_CLIENT_ID =  os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET =  os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "")

GOOGLE_AUTH_URL = os.getenv('GOOGLE_AUTH_URL', "")
GOOGLE_ACCESS_TOKEN_URL = os.getenv('GOOGLE_ACCESS_TOKEN_URL', "")
GOOGLE_USER_INFO_URL = os.getenv('GOOGLE_USER_INFO_URL', "")

RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT', 10))


@bp.route("/login")
def google_login():
    account_type = request.args.get("account_type", "user")
    custom_data = {"account_type": account_type}
    state = json.dumps(custom_data)

    params = {
        "response_type": "code",
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "scope": "openid profile email",
        "access_type": "offline",
        "prompt": "select_account",
        "state": state
    }
    google_auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    return redirect(google_auth_url)


@bp.route("/callback")
def google_callback():
    """Process login response from Google and return a JWT token"""
    try:
        code = request.args.get("code")
        if not code:
            return jsonify({"error": "No code found in the request"}), 400

        state = request.args.get("state")
        if not state:
            return jsonify({"error": "No state found in the request"}), 400
        account_type = json.loads(state).get("account_type", "user")

        token_data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        token_response = requests.post(GOOGLE_ACCESS_TOKEN_URL, data=token_data, timeout=RESPONSE_TIMEOUT)
        token_response_data = token_response.json()
        if "error" in token_response_data:
            return jsonify({"error": token_response_data["error_description"]}), 400

        access_token = token_response_data["access_token"]

        user_info_response = requests.get(
            GOOGLE_USER_INFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=RESPONSE_TIMEOUT
        )
        user_info = user_info_response.json()
        user_stored = get_user_by_email(user_info.get("email"), db)
        if user_stored is None:
            db_user = UserCreate(
                name=user_info.get("name"),
                email=user_info.get("email"),
                role="user",
                password= user_info.get("id"),
                is_verified=True,
            )
            user_stored = create(db_user, db=db, provider="google")

        jwt_token = create_access_token(
            identity=user_stored,
            expires_delta=timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 180)))
        )
        response = make_response(redirect(f"/?role={user_stored.role}"), timeout=RESPONSE_TIMEOUT)
        set_access_cookies(response, jwt_token)
        return response

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

