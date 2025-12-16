import base64
import datetime
import os

from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_jwt_extended import get_current_user, jwt_required
from pydantic import ValidationError
from werkzeug.utils import secure_filename

from app import db, logger
from app.modules.ai.service import predict_image
from app.modules.image.schema import ImageCreate
from app.modules.image.service import (allowed_file, create, delete,
                                       get_all_images, get_one_image)
from app.modules.subscriptions.service import (getActiveSubscriptionByUserId,
                                               substractImagesCount)

bp = Blueprint('images', __name__, url_prefix='/images')




@bp.post('/upload/<int:case_id>')
@jwt_required()
def create_image(case_id):
    try:
        user = get_current_user()
        subscription = getActiveSubscriptionByUserId(user_id=user.id, db=db)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        comments = request.form.get('comments')

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            if user.role == 'admin' or (subscription and subscription.images_count > 0):
                filename = secure_filename(file.filename)
                new_name = f"{user.id}_{case_id}_{int(datetime.datetime.now().timestamp())}.{filename.split('.')[1]}"
                path = os.path.join(os.getenv('UPLOAD_FILE', "uploaded_images"), new_name)
                file.save(path)
                diagnose = predict_image(path)
                if subscription: substractImagesCount(subscription_id=subscription.id, db=db)
                db_image = ImageCreate(
                    file_name= filename,
                    file_path= new_name,
                    diagnose=diagnose,
                    comments= comments
                )
                db_image = create(image=db_image, db=db, case_id=case_id)
                return jsonify(db_image.as_dict()), 200
            else:
                return jsonify({"error": "Your balance is not enough!"}), 400
            
        return "400"
    
    
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"errors": e}), 500

@bp.get('/<int:case_id>')
@jwt_required()
def list_images(case_id):
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10000))
    images = get_all_images(db, skip, limit, case_id)
    image_dicts= []
    for image in images:
        to_send = image.as_dict()
        if os.path.exists(image.file_path):
            with open(image.file_path, "rb") as image_file:
                to_send["image"] = base64.b64encode(image_file.read()).decode('utf-8')
        else:
            to_send["image"] = None
        image_dicts.append(
            to_send
        )
    return jsonify(image_dicts)

@bp.get('/get/<int:image_id>')
@jwt_required()
def get_image(image_id):
    db_image = get_one_image(image_id, db)
    return jsonify(db_image.as_dict())

@bp.delete('/<int:image_id>')
@jwt_required()
def delete_image(image_id):
    db_image = delete(image_id, db)
    return jsonify({"message": "image deleted", "image": db_image.as_dict()})