"""
User-related Pydantic schemas for API request/response validation
"""
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.user import UserRole


class UserProfile(BaseModel):
    """User profile information"""
    first_name: Optional[str] = Field(None, max_length=50, description="User's first name")
    last_name: Optional[str] = Field(None, max_length=50, description="User's last name")
    department: Optional[str] = Field(None, max_length=100, description="User's department")
    phone: Optional[str] = Field(None, max_length=20, description="User's phone number")
    avatar_url: Optional[str] = Field(None, description="URL to user's avatar image")


class UserPreferences(BaseModel):
    """User preferences and settings"""
    theme: str = Field("dark", description="UI theme preference")
    language: str = Field("en", description="Language preference")
    timezone: str = Field("UTC", description="User's timezone")
    notifications_enabled: bool = Field(True, description="Whether notifications are enabled")
    dashboard_layout: Optional[Dict[str, Any]] = Field(None, description="Custom dashboard layout")
    default_module: str = Field("dashboard", description="Default module to load")


class UserBase(BaseModel):
    """Base user schema with common fields"""
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="User's email address")
    role: UserRole = Field(UserRole.VIEWER, description="User's role in the system")
    profile: Optional[UserProfile] = Field(None, description="User profile information")
    preferences: Optional[UserPreferences] = Field(None, description="User preferences")

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """Validate username format"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username must contain only letters, numbers, hyphens, and underscores')
        return v.lower()


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8, max_length=128, description="User's password")
    confirm_password: str = Field(..., description="Password confirmation")

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        """Validate that passwords match"""
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = Field(None, description="User's email address")
    role: Optional[UserRole] = Field(None, description="User's role in the system")
    profile: Optional[UserProfile] = Field(None, description="User profile information")
    preferences: Optional[UserPreferences] = Field(None, description="User preferences")
    password: Optional[str] = Field(None, min_length=8, max_length=128, description="New password")

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength if provided"""
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserResponse(UserBase):
    """Schema for user response data"""
    id: UUID = Field(..., description="User's unique identifier")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    last_login_at: Optional[datetime] = Field(None, description="Last login timestamp")

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login request"""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="User's password")
    remember_me: bool = Field(False, description="Whether to remember the login")


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class UserLoginResponse(BaseModel):
    """Schema for login response"""
    user: UserResponse = Field(..., description="User information")
    tokens: TokenResponse = Field(..., description="Authentication tokens")
    message: str = Field("Login successful", description="Response message")


class PasswordReset(BaseModel):
    """Schema for password reset request"""
    email: EmailStr = Field(..., description="User's email address")


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation"""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password")
    confirm_password: str = Field(..., description="Password confirmation")

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        """Validate that passwords match"""
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError('Passwords do not match')
        return v

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserList(BaseModel):
    """Schema for paginated user list response"""
    users: list[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Number of users per page")
    pages: int = Field(..., description="Total number of pages")