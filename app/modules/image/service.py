from flask import abort

from app.models import Image


def create(image, db, case_id):
    db_image = Image(
        file_name= image.file_name,
        file_path= f"uploaded_images/{image.file_path}",
        diagnose= image.diagnose,
        comments= image.comments,
        case_id= case_id
    )
    db.session.add(db_image)
    db.session.commit()
    db.session.refresh(db_image)
    return db_image

def get_all_images(db, skip, limit, case_id):
    db_image =  db.session.query(Image).filter(Image.case_id == case_id).offset(skip).limit(limit).all()
    return db_image

def get_one_image(image_id, db, case_id):
    db_image = db.session.query(Image).filter(Image.case_id == case_id).filter(Image.id == image_id).first()
    if db_image is None:
        abort(404, description="Image not found")
    return db_image


def update(image_id, image_data, db, case_id):
    db_image = db.session.query(Image).filter(Image.case_id == case_id).filter(Image.id == image_id).first()
    if db_image:
        if image_data.file_name:
            db_image.file_name = image_data.file_name
        if image_data.file_path:
            db_image.file_path = image_data.file_path
        if image_data.diagnose:
            db_image.diagnose = image_data.diagnose
        if image_data.comments:
            db_image.comments = image_data.comments
        db.session.commit()
        db.session.refresh(db_image)
    else:
        abort(404, description="Image not found")
    return db_image
    
def delete(image_id, db, case_id):
    db_image = db.session.query(Image).filter(Image.case_id == case_id).filter(Image.id == image_id).first()
    if db_image:
        db.session.delete(db_image)
        db.session.commit()
        return db_image
    else:
        abort(404, description="Image not found")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
