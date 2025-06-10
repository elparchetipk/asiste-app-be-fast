"""SQLAlchemy models for user service."""

from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

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
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)  # PASO 4: Soft delete support
    phone = Column(String(20), nullable=True)  # PASO 4: Additional user field
    # PASO 5: Password reset token support
    reset_password_token = Column(String(100), nullable=True, index=True)
    reset_password_token_expires_at = Column(DateTime, nullable=True)
    
    # PASO 6: Relationship with refresh tokens
    refresh_tokens = relationship("RefreshTokenModel", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<UserModel(id={self.id}, email={self.email}, role={self.role})>"
