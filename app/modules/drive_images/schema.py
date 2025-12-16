from typing import Optional

from pydantic import BaseModel


class DoctorDiagnoseCreate(BaseModel):
    image_drive_id: str
    diagnose: str
    user_id: Optional[int] = None