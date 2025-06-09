"""Refresh token repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.refresh_token_entity import RefreshToken


class RefreshTokenRepositoryInterface(ABC):
    """Interface for refresh token repository operations."""
    
    @abstractmethod
    async def save(self, refresh_token: RefreshToken) -> RefreshToken:
        """Save a refresh token."""
        pass
    
    @abstractmethod
    async def get_by_token(self, token: str) -> Optional[RefreshToken]:
        """Get refresh token by token value."""
        pass
    
    @abstractmethod
    async def get_by_id(self, token_id: UUID) -> Optional[RefreshToken]:
        """Get refresh token by ID."""
        pass
    
    @abstractmethod
    async def get_active_tokens_for_user(self, user_id: UUID) -> List[RefreshToken]:
        """Get all active refresh tokens for a user."""
        pass
    
    @abstractmethod
    async def revoke_token(self, token: str) -> bool:
        """Revoke a specific refresh token."""
        pass
    
    @abstractmethod
    async def revoke_all_user_tokens(self, user_id: UUID) -> int:
        """Revoke all refresh tokens for a user. Returns count of revoked tokens."""
        pass
    
    @abstractmethod
    async def delete_expired_tokens(self) -> int:
        """Delete all expired tokens. Returns count of deleted tokens."""
        pass
    
    @abstractmethod
    async def update(self, refresh_token: RefreshToken) -> RefreshToken:
        """Update an existing refresh token."""
        pass
    
    @abstractmethod
    async def delete(self, token_id: UUID) -> bool:
        """Delete a refresh token by ID."""
        pass
    
    @abstractmethod
    async def count_active_tokens_for_user(self, user_id: UUID) -> int:
        """Count active tokens for a user."""
        pass
