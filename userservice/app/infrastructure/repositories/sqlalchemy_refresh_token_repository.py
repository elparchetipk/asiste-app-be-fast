"""SQLAlchemy implementation of refresh token repository."""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_

from ...domain.entities.refresh_token_entity import RefreshToken
from ...domain.repositories.refresh_token_repository_interface import RefreshTokenRepositoryInterface
from ..models.refresh_token_model import RefreshTokenModel


class SQLAlchemyRefreshTokenRepository(RefreshTokenRepositoryInterface):
    """SQLAlchemy implementation of refresh token repository."""
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def save(self, refresh_token: RefreshToken) -> RefreshToken:
        """Save a refresh token."""
        model = RefreshTokenModel(
            id=refresh_token.id,
            token=refresh_token.token,
            user_id=refresh_token.user_id,
            expires_at=refresh_token.expires_at,
            device_info=refresh_token.device_info,
            created_at=refresh_token.created_at,
            is_active=refresh_token.is_active,
            last_used_at=refresh_token.last_used_at,
        )
        
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        
        return self._model_to_entity(model)
    
    async def get_by_token(self, token: str) -> Optional[RefreshToken]:
        """Get refresh token by token value."""
        stmt = select(RefreshTokenModel).where(RefreshTokenModel.token == token)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model is None:
            return None
        
        return self._model_to_entity(model)
    
    async def get_by_id(self, token_id: UUID) -> Optional[RefreshToken]:
        """Get refresh token by ID."""
        model = await self._session.get(RefreshTokenModel, token_id)
        
        if model is None:
            return None
        
        return self._model_to_entity(model)
    
    async def get_active_tokens_for_user(self, user_id: UUID) -> List[RefreshToken]:
        """Get all active refresh tokens for a user."""
        stmt = select(RefreshTokenModel).where(
            and_(
                RefreshTokenModel.user_id == user_id,
                RefreshTokenModel.is_active == True,
                RefreshTokenModel.expires_at > datetime.now(timezone.utc)
            )
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        
        return [self._model_to_entity(model) for model in models]
    
    async def revoke_token(self, token: str) -> bool:
        """Revoke a specific refresh token."""
        stmt = (
            update(RefreshTokenModel)
            .where(RefreshTokenModel.token == token)
            .values(is_active=False)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        
        return result.rowcount > 0
    
    async def revoke_all_user_tokens(self, user_id: UUID) -> int:
        """Revoke all refresh tokens for a user. Returns count of revoked tokens."""
        stmt = (
            update(RefreshTokenModel)
            .where(
                and_(
                    RefreshTokenModel.user_id == user_id,
                    RefreshTokenModel.is_active == True
                )
            )
            .values(is_active=False)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        
        return result.rowcount
    
    async def delete_expired_tokens(self) -> int:
        """Delete all expired tokens. Returns count of deleted tokens."""
        now = datetime.now(timezone.utc)
        stmt = delete(RefreshTokenModel).where(RefreshTokenModel.expires_at <= now)
        
        result = await self._session.execute(stmt)
        await self._session.commit()
        
        return result.rowcount
    
    async def update(self, refresh_token: RefreshToken) -> RefreshToken:
        """Update an existing refresh token."""
        stmt = (
            update(RefreshTokenModel)
            .where(RefreshTokenModel.id == refresh_token.id)
            .values(
                token=refresh_token.token,
                expires_at=refresh_token.expires_at,
                device_info=refresh_token.device_info,
                is_active=refresh_token.is_active,
                last_used_at=refresh_token.last_used_at,
            )
        )
        await self._session.execute(stmt)
        await self._session.commit()
        
        # Get updated model to return
        model = await self._session.get(RefreshTokenModel, refresh_token.id)
        return self._model_to_entity(model)
    
    async def delete(self, token_id: UUID) -> bool:
        """Delete a refresh token by ID."""
        stmt = delete(RefreshTokenModel).where(RefreshTokenModel.id == token_id)
        result = await self._session.execute(stmt)
        await self._session.commit()
        
        return result.rowcount > 0
    
    async def count_active_tokens_for_user(self, user_id: UUID) -> int:
        """Count active tokens for a user."""
        stmt = select(RefreshTokenModel).where(
            and_(
                RefreshTokenModel.user_id == user_id,
                RefreshTokenModel.is_active == True,
                RefreshTokenModel.expires_at > datetime.now(timezone.utc)
            )
        )
        result = await self._session.execute(stmt)
        return len(result.scalars().all())
    
    def _model_to_entity(self, model: RefreshTokenModel) -> RefreshToken:
        """Convert SQLAlchemy model to domain entity."""
        return RefreshToken(
            token=model.token,
            user_id=model.user_id,
            expires_at=model.expires_at,
            device_info=model.device_info,
            id=model.id,
            created_at=model.created_at,
            is_active=model.is_active,
            last_used_at=model.last_used_at,
        )
