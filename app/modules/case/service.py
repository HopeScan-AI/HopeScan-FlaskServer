from flask import abort
from app.models import Case
from .schema import CaseCreate, CaseUpdate
from sqlalchemy.orm import joinedload
from app.modules.providers.service import get_one_provider, is_provider
from app.modules.user.service import get_one_user, get_user_by_email


def create(case: CaseCreate, db, owner_id, creator_id):
    db_case = Case(
        name= case.name,
        create_date= case.create_date,
        comments= case.comments,
        owner_id= owner_id,
        creator_id=creator_id,
    )
    db.session.add(db_case)
    db.session.commit()
    db.session.refresh(db_case)
    return db_case

def get_all_cases(db, skip, limit, user_id):
    return db.session.query(Case)\
    .options(joinedload(Case.creator),joinedload(Case.owner))\
    .filter(Case.owner_id == user_id).offset(skip).limit(limit).all()

def get_all_provider_cases(db, skip, limit, user_id, owner_id=None):
    cases = db.session.query(Case) \
        .options(joinedload(Case.creator), joinedload(Case.owner)) \
        .filter(Case.creator_id == user_id) \
        .all()
    filtered_cases = [
        case for case in cases
        if case.creator_id == case.owner_id or 
        (get_one_provider(case.creator_id, case.owner_id, db) and get_one_provider(case.creator_id, case.owner_id, db).status == 'accepted')
    ]

    return filtered_cases

def get_all_provider_cases2(db, skip, limit, user_id, owner_id=None):
    cases = db.session.query(Case) \
        .options(joinedload(Case.creator), joinedload(Case.owner)) \
        .filter(Case.creator_id == user_id) \
        .filter(Case.owner_id == owner_id) \
        .all()
    filtered_cases = [
        case for case in cases
        if (get_one_provider(case.creator_id, owner_id, db) and get_one_provider(case.creator_id, owner_id, db).status == 'accepted')
    ]

    return filtered_cases

# def get_one_case(case_id, db, user_id):
#     db_case = db.session.query(Case).filter(or_(Case.owner_id == user_id, Case.creator_id == user_id)).filter(Case.id == case_id).first()
#     if db_case is None:
#         abort(404, description="Case not found")
#     return db_case
def get_one_case_by_owner(case_id, db, user_id):
    db_case = db.session.query(Case).filter(Case.owner_id == user_id).filter(Case.id == case_id).first()
    if db_case is None:
        abort(404, description="Case not found Or you are not the owner")
    return db_case

def get_one_case_by_provider(case_id, db, user_id):
    db_case = db.session.query(Case).filter(Case.creator_id == user_id).filter(Case.id == case_id).first()
    if db_case is None:
        abort(404, description="Case not found")
    return db_case


def update(case_id, case_data, db, user):
    db_case = db.session.query(Case).filter(Case.id == case_id).first()
    
    if db_case:
        if case_data.name:
            db_case.name = case_data.name
        if case_data.create_date:
            db_case.create_date = case_data.create_date
        if case_data.comments:
            db_case.comments = case_data.comments
        if case_data.owner != None and case_data.owner != db_case.as_dict().get('owner').get('email'):
            change_owner(db_case.owner_id, case_data.owner, case_id, db)
        if case_data.provider != None and case_data.provider != db_case.as_dict().get('creator').get('email'):
            change_provider(db_case.creator_id, case_data.provider, case_id, db)

        db_case.updated_by = user.id
        db.session.commit()
        db.session.refresh(db_case)
    else:
        abort(404, description="Case not found")
    return db_case
    
def delete(case_id, db):
    db_case = db.session.query(Case).filter(Case.id == case_id).first()
    if db_case:
        db.session.delete(db_case)
        db.session.commit()
        return db_case
    else:
       abort(404, description="Case not found")


# def change_owner(user, new_owner, case_id, db):
#     new_user = get_one_user(new_owner, db)
#     if not new_user: abort(404, description="New Owner not found")
#     case = get_one_case(case_id, db, user.id)
#     if user.role == "institution":
#         if is_provider(new_user.id, user.id, db):
#             case.creator_id = new_user.id
#         else:
#             case.creator_id = new_user.id
#             case.owner_id = new_user.id
#     else:
#         if case.owner_id == user.id:
#             case.creator_id = new_user.id
#             case.owner_id = new_user.id
#         else:
#             abort(500, description="you are not the owner")
    
#     db.session.commit()
#     db.session.refresh(case)
#     return case

def change_owner_by_email(user, change_owner_data, db):
    case = get_one_case_by_owner(change_owner_data.case_id, db, user.id)
    new_owner = get_user_by_email(change_owner_data.email, db)
    if not new_owner: abort(404, description="new owner not found")
    case.owner_id = new_owner.id
    db.session.commit()
    db.session.refresh(case)
    return case


def change_owner(old_owner_id, new_owner, case_id, db):
    new_user = get_one_user(new_owner, db)
    if not new_user: abort(404, description="New Owner not found")
    case = get_one_case_by_owner(case_id, db, old_owner_id)
    case.owner_id = new_user.id

    db.session.commit()
    db.session.refresh(case)
    return case

def change_provider(old_provider_id, new_provider, case_id, db):
    new_user = get_one_user(new_provider, db)
    if not new_user: abort(404, description="New Provider not found")
    case = get_one_case_by_provider(case_id, db, old_provider_id)
    case.creator_id = new_user.id

    db.session.commit()
    db.session.refresh(case)
    return case
