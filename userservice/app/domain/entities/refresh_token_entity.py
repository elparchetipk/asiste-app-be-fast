"""Refresh Token domain entity."""

from datetime import datetime, timezone, timedelta
from typing import Optional
from uuid import UUID, uuid4
import secrets

from ..exceptions.user_exceptions import InvalidTokenError


class RefreshToken:
    """Refresh token domain entity for JWT token management."""
    
    def __init__(
        self,
        token: str,
        user_id: UUID,
        expires_at: datetime,
        device_info: Optional[str] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        is_active: bool = True,
        last_used_at: Optional[datetime] = None
    ):
        self._id = id or uuid4()
        self._token = token
        self._user_id = user_id
        self._expires_at = expires_at
        self._device_info = device_info
        self._created_at = created_at or datetime.now(timezone.utc)
        self._is_active = is_active
        self._last_used_at = last_used_at
    
    @property
    def id(self) -> UUID:
        """Get refresh token ID."""
        return self._id
    
    @property
    def token(self) -> str:
        """Get refresh token value."""
        return self._token
    
    @property
    def user_id(self) -> UUID:
        """Get associated user ID."""
        return self._user_id
    
    @property
    def expires_at(self) -> datetime:
        """Get expiration datetime."""
        return self._expires_at
    
    @property
    def device_info(self) -> Optional[str]:
        """Get device information."""
        return self._device_info
    
    @property
    def created_at(self) -> datetime:
        """Get creation datetime."""
        return self._created_at
    
    @property
    def is_active(self) -> bool:
        """Check if token is active."""
        return self._is_active
    
    @property
    def last_used_at(self) -> Optional[datetime]:
        """Get last usage datetime."""
        return self._last_used_at
    
    def is_valid(self) -> bool:
        """Check if refresh token is valid and not expired."""
        now = datetime.now(timezone.utc)
        return (
            self._is_active and 
            self._expires_at > now
        )
    
    def is_expired(self) -> bool:
        """Check if refresh token is expired."""
        return datetime.now(timezone.utc) >= self._expires_at
    
    def revoke(self) -> None:
        """Revoke the refresh token."""
        self._is_active = False
    
    def mark_as_used(self) -> None:
        """Mark token as recently used."""
        self._last_used_at = datetime.now(timezone.utc)
    
    def validate_for_refresh(self) -> None:
        """Validate token can be used for refresh operation."""
        if not self._is_active:
            raise InvalidTokenError("Refresh token has been revoked")
        
        if self.is_expired():
            raise InvalidTokenError("Refresh token has expired")
    
    @classmethod
    def create_for_user(
        cls,
        user_id: UUID,
        device_info: Optional[str] = None,
        expires_in_days: int = 30
    ) -> "RefreshToken":
        """Create a new refresh token for a user."""
        token = secrets.token_urlsafe(64)  # 512-bit token
        expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)
        
        return cls(
            token=token,
            user_id=user_id,
            expires_at=expires_at,
            device_info=device_info
        )
    
    def rotate(self, device_info: Optional[str] = None) -> "RefreshToken":
        """Create a new refresh token and revoke current one."""
        self.revoke()
        return self.create_for_user(
            user_id=self._user_id,
            device_info=device_info or self._device_info
        )
    
    def __eq__(self, other) -> bool:
        """Check equality based on token value."""
        if not isinstance(other, RefreshToken):
            return False
        return self._token == other._token
    
    def __hash__(self) -> int:
        """Hash based on token value."""
        return hash(self._token)
    
    def __str__(self) -> str:
        """String representation."""
        return f"RefreshToken(id={self._id}, user_id={self._user_id}, expires_at={self._expires_at})"
