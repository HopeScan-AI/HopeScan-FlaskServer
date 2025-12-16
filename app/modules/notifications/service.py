from flask import abort

from app.models import Notification
from app.modules.notifications.schema import NotificationCreate


def create(notification: NotificationCreate, db):
    db_notification = Notification(
        user_id = notification.user_id,
        title = notification.title,
        message = notification.message,
        action_url = notification.action_url
    )
    db.session.add(db_notification)
    db.session.commit()
    db.session.refresh(db_notification)
    return db_notification

def get_notifications(user_id, db):
    return db.session.query(Notification).filter(Notification.user_id == user_id).all()
     

def mark_as_read(user_id, notification_id, db):
    notification = db.session.query(Notification)\
    .filter(Notification.user_id == user_id).filter(Notification.id == notification_id).first()
    if notification:
        notification.is_read = True
        db.session.commit()
        db.session.refresh(notification)
    return notification
