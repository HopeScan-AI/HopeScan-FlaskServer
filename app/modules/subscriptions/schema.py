from pydantic import BaseModel
from typing import Optional
from datetime import date


class PaymentCreate(BaseModel):
    amount: int
    verification_code: str
    plan_id: int
    plan_type_id: int

class SubscriptionCreate(BaseModel):
    user_id: int
    authorization_code: str
    plans_id: int
    plan_type_id: int
    status: str
    currency:  str
    next_billing_date: Optional[date]

class SubscriptionUpdate(BaseModel):
    user_id: Optional[int] = None
    authorization_code: Optional[str] = None
    plans_id: Optional[int] = None
    plan_type_id: Optional[int] = None
    status: Optional[str] = None
    currency:  Optional[str] = None
    next_billing_date: Optional[date] = None
    used_images: Optional[int] = None
    images_count: Optional[int] = None
