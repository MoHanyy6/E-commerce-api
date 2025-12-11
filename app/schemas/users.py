from pydantic import BaseModel, EmailStr,constr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    customer = "customer"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[UserRole] = UserRole.customer

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_verified: bool

    class Config:
        orm_mode = True
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
