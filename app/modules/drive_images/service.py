from googleapiclient.discovery import build
from google.oauth2 import service_account
from flask import abort
from app.models import DriveImage, DoctorDiagnose
from app import db
import re
from sqlalchemy.dialects.sqlite import insert
from math import ceil


SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'pelagic-program-445912-r3-b33eeec4dbea.json'
HOPE_FOLDER_ID = "1woUoYjfWOEfb5uRTKZyF-7Yv9bfChxhj"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=credentials)



def get_different_results(page, limit):
    skip = (page - 1) * limit

    images = (
        db.session.query(DriveImage)
        .order_by(DriveImage.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = []

    for img in images:
        doctor_diagnoses = (
            db.session.query(DoctorDiagnose)
            .filter(DoctorDiagnose.image_drive_id == img.id)
            .all()
        )

        if any(diagnose.diagnose != img.old_diagnose for diagnose in doctor_diagnoses):
            temp = img.as_dict()
            temp["doctore_diagnose"] = [
                {
                    "id": diagnose.id,
                    "user": diagnose.user.name,
                    "user_id": diagnose.user_id,
                    "diagnose": diagnose.diagnose,
                }
                for diagnose in doctor_diagnoses
            ]
            result.append(temp)

    return result


def get_results(page, limit=10000):
    skip = (page - 1) * limit

    images = (
        db.session.query(DriveImage)
        .options(db.joinedload(DriveImage.doctore_diagnose))
        .order_by(DriveImage.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    images_data = [
        {
            "id": image.id,
            "name": image.name,
            "old_diagnose": image.old_diagnose,
            "doctore_diagnose": [
                {
                    "id": diagnose.id,
                    "user": diagnose.user.name,
                    "user_id": diagnose.user_id,
                    "diagnose": diagnose.diagnose,
                }
                for diagnose in image.doctore_diagnose
            ]
        }
        for image in images
    ]
    total_results = db.session.query(DriveImage).count()
    total_pages = ceil(total_results / limit)
    return {"data":images_data, "pages": total_pages}



def get_images_with_diagnoses_paginated(skip, limit, user_id):
    results = (
        db.session.query(
            DriveImage.id.label("image_id"),
            DriveImage.name.label("image_name"),
            DoctorDiagnose.diagnose.label("diagnose"),
        )
        .outerjoin(
            DoctorDiagnose,
            (DriveImage.id == DoctorDiagnose.image_drive_id) & (DoctorDiagnose.user_id == user_id),
        )
        .order_by(DriveImage.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Transform results into a list of dictionaries
    images_with_diagnoses = [
        {
            "image_id": result.image_id,
            "image_name": result.image_name,
            "diagnose": result.diagnose or "Not diagnosed",  # Handle images without a diagnose
        }
        for result in results
    ]

    return images_with_diagnoses


def get_images_not_diagnosed(skip, limit, user_id):
    diagnosed_image_ids = {
        id[0] for id in db.session.query(DoctorDiagnose.image_drive_id)
        .filter(DoctorDiagnose.user_id == user_id)
        .all()
    }

    images = (
        db.session.query(DriveImage)
        .filter(~DriveImage.id.in_(diagnosed_image_ids))
        .order_by(DriveImage.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    final_images = [
        {
            "image_id": image.id,
            "image_name": image.name,
            "diagnose": "Not diagnosed",
        }
        for image in images
    ]

    return final_images



def add_doctor_diagnose(doctor_diagnose):
    db_doctor_diagnose = db.session.query(DoctorDiagnose).filter(
        DoctorDiagnose.user_id == doctor_diagnose.user_id,
        DoctorDiagnose.image_drive_id == doctor_diagnose.image_drive_id
    ).first()

    if db_doctor_diagnose:
        db_doctor_diagnose.diagnose = doctor_diagnose.diagnose
    else:
        db_doctor_diagnose = DoctorDiagnose(
            user_id=doctor_diagnose.user_id,
            image_drive_id=doctor_diagnose.image_drive_id,
            diagnose=doctor_diagnose.diagnose
        )
        db.session.add(db_doctor_diagnose)

    # Commit the transaction
    db.session.commit()

    # Refresh the mapped instance to ensure it has the latest data
    db.session.refresh(db_doctor_diagnose)

    return db_doctor_diagnose


def create_many(images):
    stmt = insert(DriveImage).values(images)
    stmt = stmt.prefix_with("OR IGNORE")
    db.session.execute(stmt)
    db.session.commit()


def store_images_db():
    folders = get_content(HOPE_FOLDER_ID)
    for folder in folders:
        images = get_content(folder.get('id'))
        images_to_save = create_images_objects(images, folder)
        create_many(images_to_save)
    return "done"

def create_images_objects(images, folder):
    images_objects = []
    for image in images:
        if allowed_file(image.get("name")):
            obj = {
                "id": image.get("id"),
                "name": image.get("name"),
                "folder_id": folder.get("id"),
                "folder_name": folder.get("name"),
                "old_diagnose": re.findall(r"[a-zA-Z]+", folder.get("name"))[0].lower()
            }
            images_objects.append(obj)
        else:
            print(f"File {image.get('name')} is not allowed")
    return images_objects

def get_content(folder_id):
    all_files = []
    page_token = None
    while True:
        results = drive_service.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            pageSize=1000,
            pageToken=page_token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            fields="nextPageToken, files(id, name)"
        ).execute()

        all_files.extend(results.get('files', []))

        page_token = results.get('nextPageToken')
        if not page_token:
            break 
    return all_files


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
