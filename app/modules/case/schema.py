from datetime import date
from typing import Optional

from pydantic import BaseModel


class CaseCreate(BaseModel):
    name: str
    create_date: date
    comments: str
    owner_id: Optional[int] = None
    provider_id: Optional[int] = None

class CaseUpdate(BaseModel):
    name: Optional[str] = None
    create_date: Optional[date] = None
    comments: Optional[str] = None
    owner: Optional[str] = None
    provider: Optional[str] = None

class ChangeOwner(BaseModel):
    email: str
    case_id: str