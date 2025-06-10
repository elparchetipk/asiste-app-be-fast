"""Refresh token SQLAlchemy model."""

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from ..config.database import Base


class RefreshTokenModel(Base):
    """SQLAlchemy model for refresh tokens."""
    
    __tablename__ = "refresh_tokens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String(128), unique=True, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    device_info = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationship
    user = relationship("UserModel", back_populates="refresh_tokens")
    
    def __repr__(self) -> str:
        return f"<RefreshTokenModel(id={self.id}, user_id={self.user_id}, expires_at={self.expires_at})>"
