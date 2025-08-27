from pydantic import BaseModel

class ImageResponse(BaseModel):
    filename: str
    classification: str