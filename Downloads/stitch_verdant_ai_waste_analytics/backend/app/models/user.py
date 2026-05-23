"""
User model for authentication and authorization
"""
from sqlalchemy import Column, String, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    ADMIN = "admin"
    OPERATOR = "operator"
    ANALYST = "analyst"
    VIEWER = "viewer"


class User(Base):
    """User model for authentication and profile management"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.VIEWER)
    
    # Profile information stored as JSON
    profile = Column(JSON, nullable=True)
    preferences = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"