from typing import Optional

from pydantic import BaseModel


class ImageCreate(BaseModel):
    file_name: str
    file_path: str
    diagnose: str
    comments: Optional[str]
