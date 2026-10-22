"""Pydantic schemas for Authentication"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15, description="Phone number with country code")
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)
    preferred_language: str = Field(default="en", pattern="^(en|hi|mr)$")

    @validator('phone')
    def validate_phone(cls, v):
        # Remove spaces and dashes
        v = v.replace(' ', '').replace('-', '')
        if not v.replace('+', '').isdigit():
            raise ValueError('Phone must contain only digits and optional + prefix')
        return v


class UserLogin(BaseModel):
    phone: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    phone: str
    full_name: str
    preferred_language: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class FarmerProfileUpdate(BaseModel):
    state: Optional[str] = None
    district: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    land_size_acres: Optional[float] = Field(None, ge=0, le=10000)
    primary_crops: Optional[list] = None
    farmer_category: Optional[str] = Field(None, pattern="^(small|marginal|medium|large)$")
    soil_type: Optional[str] = None
