from pydantic import BaseModel
from typing import Optional

class ProviderCreate(BaseModel):
    user_email: str
