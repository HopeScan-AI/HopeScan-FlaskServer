from flask import abort
from .schema import *
from app.models import Plans, PlanType
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from collections import defaultdict

from app import logger


def getPlans(db):
    try:
        plans = db.session.query(Plans).options(joinedload(Plans.plan_type)).all()
        return [plan.as_dict() for plan in plans]
    except Exception as e:
        logger.error(f"Failed to retrieve plans: {e}")
        abort(500, description="Error retrieving plans.")

def getPlan(plan_id: int, db):
    plan = db.session.query(Plans).options(joinedload(Plans.plan_type)).get(plan_id)
    if not plan:
        abort(404, description="Plan not found.")
    return plan.as_dict()

def getPlanType(plan_type_id: int, db):
    plan_type = db.session.query(PlanType).get(plan_type_id)
    if not plan_type:
        abort(404, description="plan type not found.")
    return plan_type.as_dict()

def createPlan(plan_data: PlanCreate, db):
    try:
        # Create the Plan
        new_plan = Plans(
            name=plan_data.name,
            num_of_providers=plan_data.num_of_providers,
            icon=plan_data.icon,
            name_arabic=plan_data.name_arabic,
            image_cost=plan_data.image_cost,
        )
        db.session.add(new_plan)
        db.session.flush()  # Get the plan ID before committing

        # Create the related PlanTypes

        if plan_data.plan_type:
            for pt in plan_data.plan_type:
                plan_type = PlanType(
                    name=pt.get('name'),
                    price=pt.get('price'),
                    period=pt.get('period'),
                    images_count= pt.get('images_count'),
                    plan_id=new_plan.id
                )
                db.session.add(plan_type)

        db.session.commit()
        # print(new_plan)
        # print(new_plan.as_dict())
        return new_plan
    except Exception as e:
        logger.error(f"Failed to create plan and types: {e}")
        db.session.rollback()
        abort(400, description=f"Plan creation with types failed. {e}")

def updatePlan(plan_id: int, update_data: PlanUpdate, db):
    plan = db.session.query(Plans).options(joinedload(Plans.plan_type)).get(plan_id)
    if not plan:
        abort(404, description="Plan not found.")
    try:
        for key, value in update_data.dict(exclude_unset=True).items():
            if key != "plan_type":
                setattr(plan, key, value)

        # Handle updating plan types
        if update_data.plan_type:
            # Clear existing plan types
            db.session.query(PlanType).filter_by(plan_id=plan.id).delete()
            # Add new plan types
            for pt in update_data.plan_type:
                plan_type = PlanType(
                    name=pt.get('name'),
                    price=pt.get('price'),
                    period=pt.get('period'),
                    images_count=pt.get('images_count'),
                    plan_id=plan.id
                )
                db.session.add(plan_type)

        db.session.commit()
        return plan
    except Exception as e:
        logger.error(f"Failed to update plan and types: {e}")
        db.session.rollback()
        abort(400, description="Plan update failed.")

def deletePlan(plan_id: int, db):
    plan = db.session.query(Plans).get(plan_id)
    if not plan:
        abort(404, description="Plan not found.")
    try:
        db.session.delete(plan)
        db.session.commit()
        return plan
    except Exception as e:
        logger.error(f"Failed to delete plan: {e}")
        db.session.rollback()
        abort(400, description="Plan deletion failed.")
