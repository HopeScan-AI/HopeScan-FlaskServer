from flask import abort
from .schema import SubscriptionCreate
from app.models import Subscription, Payments
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from app.modules.plans.service import getPlan, getPlanType

from app import logger

def subscriptionPayment(payment_data, db):
    authorization_code= payment_data.get("authorization").get("authorization_code")
    reference= payment_data.get("reference")
    plan_id= payment_data.get("metadata").get("plan_id")
    plan_type_id= payment_data.get("metadata").get("plan_type_id")
    user_id= payment_data.get("metadata").get("user_id")
    amount= payment_data.get("amount")
    payment_status=payment_data.get("status")
    status = "active"
    currency = payment_data.get("currency")
    subscription_plan_type = getPlanType(plan_type_id, db)

    db_payment = Payments(
        user_id= user_id,
        amount=amount,
        verification_code=reference,
        status=payment_status,
    )
    db.session.add(db_payment)
    db.session.commit()
    db.session.refresh(db_payment)
    
    if subscription_plan_type.price != amount:
        logger.warning(f"User with id {user_id} is trying to subscripe to plan id \
                       {plan_id} with non equivalent price")
        status = "invalid"
    period = subscription_plan_type.period
    subscription = SubscriptionCreate(
        currency = currency,
        authorization_code = authorization_code,
        plan_id = plan_id,
        plan_type_id = plan_type_id,
        status = status,
        next_billing_date = datetime.utcnow() + timedelta(days= 30 * period)
    )
    return createSubscription(subscription, db, user_id)



def createSubscription(subscription: SubscriptionCreate, db, user_id):
    old_active_subscription = getActiveSubscriptionByUserId(user_id, db)
    if old_active_subscription:
        old_active_subscription.status = 'inactive'
        db.session.add(old_active_subscription)
        db.session.commit()
        db.session.refresh(old_active_subscription)

    subscription_plan = getPlan(subscription.plan_id, db)
    subscription_plan_type = getPlanType(subscription.plan_type_id, db)

    db_subscription = Subscription(
        user_id = user_id,
        authorization_code = subscription.authorization_code,
        plans_id = subscription.plan_id,
        plan_type_id = subscription.plan_type_id,
        status = subscription.status,
        currency = subscription.currency,
        next_billing_date = subscription.next_billing_date,
        used_images=0,
        images_count=subscription_plan_type.get('images_count'),
        num_of_providers=subscription_plan.get('num_of_providers'),
        image_cost=subscription_plan.get('image_cost'),
    )
    db.session.add(db_subscription)
    db.session.commit()
    db.session.refresh(db_subscription)
    return db_subscription


def getSubscriptions(db):
    subscriptions = db.session.query(Subscription).all()
    subscriptions_dicts = [
        s.as_dict() for s in subscriptions
    ]
    return subscriptions_dicts


def getSubscription(subscription_id, db):
    subscription = db.session.query(Subscription).filter(Subscription.id == subscription_id).first()
    return subscription.as_dict() if subscription else None

def getActiveSubscriptionByUserId(user_id, db):
    subscription = db.session.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.status == 'active'
        ).first()
    return subscription

def substractImagesCount(subscription_id, db):
    db_subscription = db.session.query(Subscription).filter(Subscription.id == subscription_id).first()
    db_subscription.images_count = db_subscription.images_count - 1
    db.session.add(db_subscription)
    db.session.commit()
    db.session.refresh(db_subscription)

def updateSubscription(subscription_id, sub_data, db):
    db_subscription = db.session.query(Subscription).filter(Subscription.id == subscription_id).first()

    if db_subscription:
        if sub_data.authorization_code:
            db_subscription.authorization_code = sub_data.authorization_code
        if sub_data.status:
            db_subscription.status = sub_data.status
        if sub_data.currency:
            db_subscription.currency = sub_data.currency
        if sub_data.used_images:
            db_subscription.used_images = sub_data.used_images
        if sub_data.next_billing_date:
            db_subscription.next_billing_date = sub_data.next_billing_date
        if sub_data.plans_id:
            db_subscription.plans_id = sub_data.plans_id
            subscription_plan = getPlanType(sub_data.plan_id, db)
            db_subscription.num_of_providers=subscription_plan.get('num_of_providers')
            db_subscription.image_cost=subscription_plan.get('image_cost')
        if sub_data.plan_type_id:
            db_subscription.plan_type_id = sub_data.plan_type_id
            subscription_plan_type = getPlanType(sub_data.plan_type_id, db)
            db_subscription.images_count=subscription_plan_type.get('images_count')
        if sub_data.images_count:
            db_subscription.images_count=sub_data.images_count

        db.session.commit()
        db.session.refresh(db_subscription)
    else:
        abort(404, description="Subscription not found")
    return db_subscription


def deleteSubscription(subscription_id, db):
    db_subscription = db.session.query(Subscription).filter(Subscription.id == subscription_id).first()
    if db_subscription:
        db.session.delete(db_subscription)
        db.session.commit()
        return db_subscription
    else:
       abort(404, description="subscription not found")
