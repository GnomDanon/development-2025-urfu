from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    description: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID4
    username: str
    email: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
