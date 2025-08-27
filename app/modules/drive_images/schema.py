from pydantic import BaseModel
from typing import Optional



class DoctorDiagnoseCreate(BaseModel):
    image_drive_id: str
    diagnose: str
    user_id: Optional[int] = None