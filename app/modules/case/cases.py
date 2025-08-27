from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from .schema import CaseCreate, ChangeOwner
from app import db
from .service import *
from flask_jwt_extended import jwt_required, get_current_user
from app.modules.providers.service import get_one_provider, get_one_provider_without_user

bp = Blueprint('case', __name__, url_prefix='/case')


@bp.post('/')
@jwt_required()
def create_case():
    try:
        case_data = CaseCreate(**request.json)
        # print(case_data)
        provider_id =  case_data.provider_id if case_data.provider_id else request.args.get('provider_id')
        owner_id =  case_data.owner_id
        user = get_current_user()
        # if provider_id:
        saved_case = create(case_data, db, owner_id, provider_id)
        # else:
        #     if case_data.owner_id ==  user.id:
        #         saved_case = create(case_data, db, user.id, user.id)
        #     else:
        #         print(case_data.owner_id)
        #         saved_case = create(case_data, db, case_data.owner_id, user.id)
        return jsonify(saved_case.as_dict()), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400


@bp.get('/')
@jwt_required()
def list_cases():
    provider_id = request.args.get('provider_id')
    user = get_current_user()
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10000))
    provider = get_one_provider(provider_id, user.id, db)

    if provider_id and provider:
        cases = get_all_provider_cases2(db, skip, limit, provider_id, user.id)
    else:
        provider = get_one_provider_without_user(user.id, db)
        if provider:
            cases = get_all_provider_cases(db, skip, limit, user.id)
        else:
            cases = get_all_cases(db, skip, limit, user.id)
    case_dicts = [case.as_dict() for case in cases]
    return jsonify(case_dicts)

@bp.get('/<int:case_id>')
@jwt_required()
def get_case(case_id):
    provider_id = request.args.get('provider_id')
    user = get_current_user()
    is_exist = get_one_provider(provider_id, user.id, db)
    if provider_id and is_exist:
        db_case = get_one_case_by_provider(case_id, db, provider_id)
    else:
        provider = get_one_provider_without_user(user.id, db)
        if provider:
            db_case = get_one_case_by_provider(case_id, db, provider.provider_id)
        else:
            db_case = get_one_case_by_owner(case_id, db, user.id)
    return jsonify(db_case.as_dict())


@bp.put('/<int:case_id>')
@jwt_required()
def update_case(case_id):
    try:
        user = get_current_user()
        case_data = CaseUpdate(**request.json)
        if user.id == int(case_data.owner) or user.id == int(case_data.provider):
            update(case_id, case_data, db, user)
            return jsonify({"status": 200}), 200
        else: return jsonify({"error": "Not Authorized"}), 401
    except Exception as e:
            return jsonify({"error": str(e)}), 500

@bp.post('/change_owner')
@jwt_required()
def change_owner():
    try:
        user = get_current_user()
        change_owner_data = ChangeOwner(**request.json)
        case = change_owner_by_email(user, change_owner_data, db)
        return jsonify({"case": case.as_dict()}), 200
    except Exception as e:
            return jsonify({"error": str(e)}), 500

@bp.delete('/<int:case_id>')
@jwt_required()
def delete_case(case_id):
    db_case = delete(case_id, db)
    return jsonify({"message": "case deleted", "case": db_case.as_dict()})