from pydantic import BaseModel, EmailStr, Field

from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, strip_whitespace=True, description="Name cannot be empty")
    email: EmailStr = Field(..., description="Invalid email format")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")
    role: Optional[str] = Field(default="user", min_length=1, description="Role cannot be empty")
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
