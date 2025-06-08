"""SQLAlchemy models for user service."""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from ...domain import UserRole

Base = declarative_base()


class UserModel(Base):
    """SQLAlchemy model for User entity."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(254), nullable=False, unique=True, index=True)
    document_number = Column(String(15), nullable=False, unique=True, index=True)
    document_type = Column(String(2), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    must_change_password = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<UserModel(id={self.id}, email={self.email}, role={self.role})>"
