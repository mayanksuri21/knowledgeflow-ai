from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    profile_image: Optional[str] = None


class UserCreate(UserBase):
    clerk_id: str


class UserUpdate(UserBase):
    pass


class UserResponse(UserBase):
    id: str
    clerk_id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
