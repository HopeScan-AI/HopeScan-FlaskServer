import os

import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_current_user, get_jwt, jwt_required
from werkzeug.utils import secure_filename

from app.modules.ai.service import predict_image

bp = Blueprint("ai", __name__, url_prefix='/ai')

RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT', 10))

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'app/ai-images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@bp.post("/classify")
@jwt_required()
def classify_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    img_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(img_path)

    result = predict_image(img_path)

    return jsonify({"filename": filename, "classification": result})

@bp.post("/classify-url")
@jwt_required()
def classify_image_from_url():
    data = request.get_json()
    image_url = data.get("image_url")

    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400

    try:
        response = requests.get(image_url, stream=True, timeout=RESPONSE_TIMEOUT)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch image"}), 400

        filename = image_url.split("/")[-1]
        if not filename.endswith(".png"):
            filename += ".png"
        img_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(img_path, "wb") as img_file:
            for chunk in response.iter_content(1024):
                img_file.write(chunk)

        result = predict_image(img_path)

        return jsonify({"filename": filename, "classification": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500