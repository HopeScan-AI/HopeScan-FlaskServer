from pydantic import BaseModel
from typing import Optional

class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    action_url:  str