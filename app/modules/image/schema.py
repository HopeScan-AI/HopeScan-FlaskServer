from pydantic import BaseModel
from typing import Optional

class ImageCreate(BaseModel):
    file_name: str
    file_path: str
    diagnose: str
    comments: Optional[str]
