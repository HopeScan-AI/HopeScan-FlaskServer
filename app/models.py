from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey, Text, Double
from sqlalchemy.sql import func
from datetime import datetime, timedelta


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(10))
    verification_code = Column(String(10))
    is_verified = Column(Boolean, default=False)
    provider = Column(String(20))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, nullable=True)
    deleted_by = Column(Integer, nullable=True)
    owner_cases = relationship('Case', back_populates='owner', foreign_keys='Case.owner_id', cascade="all, delete-orphan")
    creator_cases = relationship('Case', back_populates='creator', foreign_keys='Case.creator_id', cascade="all, delete-orphan")
    doctore_diagnose = relationship('DoctorDiagnose', back_populates='user', cascade="all, delete-orphan")
    health_providers_user = relationship('HealthProvider', back_populates='user', foreign_keys='HealthProvider.user_id', cascade="all, delete-orphan")
    health_provider = relationship('HealthProvider', back_populates='user', foreign_keys='HealthProvider.provider_id', cascade="all, delete-orphan")
    notifications = relationship('Notification', back_populates='user', cascade="all, delete-orphan")
    payments = relationship('Payments', back_populates='user', cascade="all, delete-orphan")
    subscription = relationship('Subscription', back_populates='user', cascade="all, delete-orphan")

    def as_dict(self):
        user_dict =  {col.name: getattr(self, col.name) for col in self.__table__.columns}
        # print(self.health_provider)
        
        user_dict["providers"] =[
            {**provider.as_dict()}
            for provider in self.health_providers_user
        ]
        user_dict["owners"] =[
            {**owner.as_dict()}
            for owner in self.health_provider
        ]

        return user_dict


class Case(db.Model):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    create_date = Column(Date, nullable=False)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship('User', back_populates='owner_cases', foreign_keys=[owner_id])
    creator = relationship('User', back_populates='creator_cases', foreign_keys=[creator_id])
    images = relationship('Image', back_populates='case', cascade="all, delete-orphan") 

    def as_dict(self):
        case_dict = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        case_dict['create_date_without_time'] = self.create_date_without_time

        # Include creator details
        case_dict['creator'] = {
            "id": self.creator.id,
            "name": self.creator.name,
            "email": self.creator.email
        } if self.creator else None

        case_dict['owner'] = {
            "id": self.owner.id,
            "name": self.owner.name,
            "email": self.owner.email
        } if self.owner else None
        
        return case_dict

    
    @property
    def create_date_without_time(self):
        return self.create_date.strftime('%Y-%m-%d') if self.create_date else None

class Image(db.Model):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    diagnose = Column(String(500), nullable=True)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    case_id = Column(Integer, ForeignKey('cases.id'))
    case = relationship("Case", back_populates="images")

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class DriveImage(db.Model):
    __tablename__ = "drive_image"
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    old_diagnose = Column(String(20), nullable=True)
    folder_id = Column(String(20), nullable=True)
    folder_name = Column(String(20), nullable=True)
    doctore_diagnose = relationship('DoctorDiagnose', back_populates='image_drive')


    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
    
class DoctorDiagnose(db.Model):
    __tablename__ = "doctor_diagnose"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='doctore_diagnose')
    image_drive_id = Column(String(50), ForeignKey('drive_image.id'), nullable=False)
    image_drive  = relationship('DriveImage', back_populates='doctore_diagnose')
    diagnose = Column(String(20), nullable=True)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class HealthProvider(db.Model):
    __tablename__ = "health_provider"
    
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    provider = relationship('User', back_populates='health_provider', foreign_keys=[provider_id], overlaps="health_providers", lazy="joined")
    user = relationship('User', back_populates='health_provider', foreign_keys=[user_id])
    
    status = Column(String(20), nullable=False, default="pending")

    def as_dict(self):
        provider_dict = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        provider_dict['owner_name'] = self.user.name
        provider_dict['provider_name'] = self.provider.name
        provider_dict['owner_id'] = self.user.id

        return provider_dict
    

class Notification(db.Model):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='notifications')
    is_read = Column(Boolean, default= False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    action_url = Column(String(255))
    title = Column(String(255))
    message = Column(String(255))

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
    
class Payments(db.Model):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='payments')
    amount = Column(Integer, nullable=False)
    verification_code = Column(String(255), nullable=False)
    subscription_id =  Column(Integer, ForeignKey('subscription.id'), nullable=True)
    status=Column(String(50), default="approved")
    subscription = relationship('Subscription', back_populates='payments')
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
    

class Subscription(db.Model):
    __tablename__ = "subscription"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='subscription')
    authorization_code = Column(String(255), nullable=False)  # Lahza authorization code
    plans_id = Column(String(100), ForeignKey('plans.id'), nullable=False)
    plans = relationship('Plans', back_populates='subscription')
    plan_type_id = Column(String(100), ForeignKey('plan_type.id'), nullable=False)
    plan_type = relationship('PlanType', back_populates='subscription')
    currency = Column(String(10), default="USD")
    status = Column(String(50), default="active")  # active, canceled, expired
    start_date = Column(DateTime, default=datetime.utcnow)
    next_billing_date = Column(DateTime, default=datetime.utcnow() + timedelta(days=30))
    images_count = Column(Integer, default=0)
    num_of_providers = Column(Integer, default=0)
    image_cost = Column(Double, default=0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    used_images = Column(Integer, default=0)
    payments = relationship('Payments', back_populates='subscription')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


    

class Plans(db.Model):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    name_arabic = Column(String(50))
    image_cost = Column(Double, default=0)
    plan_type = relationship(
        'PlanType',
        back_populates='plans',
    )
    num_of_providers = Column(Integer, default=0)
    subscription = relationship('Subscription', back_populates='plans')
    icon = Column(Text)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    def as_dict(self):
        plans = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        plans["plan_type"] = [p.as_dict() for p in self.plan_type]
        return plans
    
class PlanType(db.Model):
    __tablename__ = "plan_type"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    period = Column(Integer, default=1)
    price = Column(Double, default=1)
    images_count = Column(Integer, default=0)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    plans = relationship(
        'Plans',
        back_populates='plan_type',
        foreign_keys=[plan_id]
    )
    subscription = db.relationship("Subscription", back_populates="plan_type")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
