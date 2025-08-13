"""
Authentication Models for Cyra Enhanced
======================================
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any

class UserRegistration(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = ""

class UserLogin(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
    username: str
    email: str
    full_name: str
    preferences: Dict[str, Any]

class SessionResponse(BaseModel):
    success: bool
    message: str
    session_token: Optional[str] = None
    user: Optional[UserProfile] = None

class AuthResponse(BaseModel):
    success: bool
    message: str
    username: Optional[str] = None

class PreferencesUpdate(BaseModel):
    theme: Optional[str] = None
    voice_enabled: Optional[bool] = None
    notifications: Optional[bool] = None
