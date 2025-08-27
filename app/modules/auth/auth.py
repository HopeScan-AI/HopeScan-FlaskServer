from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.modules.user.service import (
    get_user_by_email,
    create,
    # set_verification_code,
    # get_verification_code,
    # verify_account,
)
from app.modules.user.schema import UserCreate
from .schema import LoginRequest, VerificationRequest
import os
# from email.message import EmailMessage
# import random
# import smtplib
from datetime import timedelta
from app import db
from app import bcrypt
from flask_jwt_extended import jwt_required, unset_access_cookies, create_access_token, get_jwt_identity, set_access_cookies
from app.modules.providers.service import get_owners

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
            # if email_exist.is_verified:
            return jsonify({"error": "Email already exists."}), 400
            # else:
            #     return jsonify({"error": "Email already exists but not verified."}), 400

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
            expires_delta=timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
        )
        owners = get_owners(db_user.id, db)
        response = jsonify(access_token=access_token, user=db_user.as_dict())
        set_access_cookies(response, access_token)
        return response
    except Exception as e:
        print(e)
        return jsonify({"error": f"An unexpected error occurred. {e}"}), 500


# @bp.post("/send-verification-code")
# def send_verification_code():
#     try:
#         email = request.json.get("email")
#         role = request.json.get("role")
#         if not email:
#             return jsonify({"error": "Email is required"}), 400
#         if role == "institution":
#             return jsonify({"message": "Your Account will be reviewed by Admins to approve"})
#         code = f"{random.randint(100000, 999999)}"
#         set_verification_code(email, code, db)

#         message = EmailMessage()
#         message["From"] = "hopescan@gmail.com"
#         message["To"] = email
#         message["Subject"] = "Account Verification Code"
#         message.set_content(f"Your verification code is: {code}")

#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login("famaliha2@gmail.com", "zyts xuvw tysz fszg")  # Use a secure app password
#             server.send_message(message)

#         return jsonify({"message": "Verification code sent, check spam"})
#     except Exception as e:
#         return jsonify({"error": f"Failed to send email: {str(e)}"}), 500


# @bp.post("/verify-code")
# def verify_code():
#     try:
#         verification_data = VerificationRequest(**request.json)
        
#         stored_code = get_verification_code(verification_data.email, db)
#         if not stored_code:
#             return jsonify({"error": "No code sent to this email."}), 400

#         if stored_code != verification_data.code:
#             return jsonify({"error": "Invalid verification code."}), 400

#         verify_account(verification_data.email, db)
#         return jsonify({"message": "Email verified successfully!"})
#     except Exception as e:
#         return jsonify({"error": f"An unexpected error occurred. {e}"}), 500



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
