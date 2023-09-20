from pydantic import BaseModel
from datetime import datetime

class ProfileRequest(BaseModel):
    address: str
    phone_number: str
    profile_picture: str

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    address: str
    phone_number: str
    profile_picture: str
    created_at: datetime
    updated_at: datetime