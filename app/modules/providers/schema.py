from typing import Optional

from pydantic import BaseModel


class ProviderCreate(BaseModel):
    user_email: str
