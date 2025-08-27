from flask import Blueprint, request, jsonify
from .service import store_images_db, get_images_with_diagnoses_paginated, get_images_not_diagnosed, add_doctor_diagnose, get_results, get_different_results
from .schema import DoctorDiagnoseCreate
from flask_jwt_extended import jwt_required, get_current_user



bp = Blueprint('drive_images', __name__, url_prefix='/drive-images')


    
@bp.get("/results/data")
@jwt_required()
def results_data():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=1000000, type=int)
    user = get_current_user()
    if user.role == "admin":
        results = get_results(page, limit)
        return jsonify(results)
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401
    
@bp.get("/different_diagnoses")
@jwt_required()
def different_diagnoses():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10000, type=int)
    user = get_current_user()
    if user.role == "admin":
        result = get_different_results(page, limit)
        return jsonify(result)
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401


@bp.get("/update_content")
@jwt_required()
def updated_images_in_db():
    user = get_current_user()
    if user.role == "admin":
        return jsonify({"status": store_images_db()}), 200
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401
    

@bp.get("/get")
@jwt_required()
def get_all():
    user = get_current_user()
    if user.role == "admin" or user.role == "annotator":
        user = get_current_user()
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10000))
        images = get_images_with_diagnoses_paginated(skip, limit, user.id)
        # images_dicts = [image.as_dict() for image in images]
        return jsonify(images)
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401

@bp.get("/get_no_diagnose")
@jwt_required()
def get_all_no_diagnose():
    user = get_current_user()
    if user.role == "admin" or user.role == "annotator":
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10000))
        user = get_current_user()
        images = get_images_not_diagnosed(skip, limit, user.id)
        return jsonify(images)
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401


@bp.post("/create-doctor-diagnose") 
@jwt_required()
def create_doctor_diagnose():
    user = get_current_user()
    if user.role == "admin" or user.role == "annotator":
        user = get_current_user()
        image_data = DoctorDiagnoseCreate(**request.json)
        image_data.user_id = user.id
        return jsonify(add_doctor_diagnose(image_data).as_dict())
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401