from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_current_user, jwt_required

from app import db, logger
from app.modules.plans.schema import *
from app.modules.plans.service import *

bp = Blueprint('plans', __name__, url_prefix='/plans')

@bp.post('/')
@jwt_required()
def create_plan():
    try:
        user = get_current_user()
        if user.role == "admin":
            plan_data = PlanCreate(**request.json)
            saved_plan = createPlan(plan_data, db)
            return jsonify(saved_plan.as_dict()), 201
        else:
            return jsonify({"errors": "UNAUTORIZED"}), 401
    except Exception as e:
        print(e)
        return jsonify({"errors": e.__str__()}), 500


@bp.get('/')
def get_plans():
    try:
        plans = getPlans(db)
        
        return jsonify(plans), 200
    except Exception as e:
        return jsonify({"errors": e.__str__()}), 500

@bp.get('/<int:plan_id>')
def get_plan(plan_id):
    try:
        plan = getPlan(plan_id, db)
        
        return jsonify(plan), 200
    except Exception as e:
        return jsonify({"errors": e.__str__()}), 500
    

@bp.put('/<int:plan_id>')
@jwt_required()
def update_plan(plan_id):
    try:
        user = get_current_user()
        sub_data = PlanUpdate(**request.json)
        if user.role == "admin":
            updated_plan = updatePlan(plan_id, sub_data, db)
            return jsonify({"plan": updated_plan.as_dict()}), 200
        else:
            return jsonify({"errors": "UNAUTORIZED"}), 401
    except Exception as e:
        return jsonify({"errors": e.__str__()}), 500

@bp.delete('/<int:plan_id>')
@jwt_required()
def delete_plan(plan_id):
    try:
        user = get_current_user()
        if user.role == "admin":
            db_plan = deletePlan(plan_id, db)
            return jsonify({"message": " plan deleted", "plan": db_plan.as_dict()})
        else:
            return jsonify({"errors": "UNAUTORIZED"}), 401
    except Exception as e:
        return jsonify({"errors": e.__str__()}), 500


