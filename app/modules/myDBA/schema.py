from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[str] = "user"
    is_verified: Optional[bool] = False

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_verified: Optional[bool] = None

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    password: str
    role: str
    is_verified: bool
