from datetime import date
from typing import Any, List, Optional

from pydantic import BaseModel


class PlanTypeCreate(BaseModel):
    name: str
    price: float
    period: int
    images_count: int

class PlanTypeUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    period: Optional[int] = None
    images_count: Optional[int] = None


class PlanCreate(BaseModel):
    name: str
    name_arabic: str
    image_cost: float
    num_of_providers: int
    plan_type: List[Any]
    icon: str


class PlanUpdate(BaseModel):
    name: Optional[str] = None
    num_of_providers: Optional[int] = None
    plan_type: Optional [List[Any]] = []
    name_arabic: Optional[str] = None
    image_cost: Optional[float] = None
    icon:  Optional[str] = None

