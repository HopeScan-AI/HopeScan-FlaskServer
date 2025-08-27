from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class VerificationRequest(BaseModel):
    email: str
    code: str
