from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from .service import predict_image
from flask_jwt_extended import jwt_required,  get_jwt, get_current_user
import requests 

# Define Blueprint
bp = Blueprint("ai", __name__, url_prefix='/ai')

# Ensure ai-images directory exists
UPLOAD_FOLDER = "app/ai-images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@bp.post("/classify")
@jwt_required()
def classify_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Secure filename and save the image
    filename = secure_filename(file.filename)
    img_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(img_path)

    # Run prediction
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
        # Download the image
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch image"}), 400

        # Extract filename from URL and save
        filename = image_url.split("/")[-1]  # Extract last part of the URL
        if not filename.endswith(".png"):  # Ensure it ends with .png
            filename += ".png"
        img_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(img_path, "wb") as img_file:
            for chunk in response.iter_content(1024):
                img_file.write(chunk)

        # Run prediction
        result = predict_image(img_path)

        return jsonify({"filename": filename, "classification": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500