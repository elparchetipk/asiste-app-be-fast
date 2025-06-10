"""Unit tests for SQLAlchemy RefreshToken Repository."""

import pytest
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from unittest.mock import AsyncMock, Mock

from app.infrastructure.repositories.sqlalchemy_refresh_token_repository import SQLAlchemyRefreshTokenRepository
from app.infrastructure.models.refresh_token_model import RefreshTokenModel
from app.domain.entities.refresh_token_entity import RefreshToken


class TestSQLAlchemyRefreshTokenRepository:
    """Test cases for SQLAlchemy RefreshToken Repository."""
    
    @pytest.fixture
    def mock_session(self):
        """Mock SQLAlchemy async session."""
        session = AsyncMock()
        return session
    
    @pytest.fixture
    def repository(self, mock_session):
        """Create repository instance with mocked session."""
        return SQLAlchemyRefreshTokenRepository(mock_session)
    
    @pytest.fixture
    def sample_refresh_token(self):
        """Create a sample refresh token entity."""
        return RefreshToken.create_for_user(
            user_id=uuid4(),
            device_info="Test Device",
            expires_in_days=30
        )
    
    @pytest.fixture
    def sample_refresh_token_model(self, sample_refresh_token):
        """Create a sample refresh token model."""
        return RefreshTokenModel(
            id=sample_refresh_token.id,
            token=sample_refresh_token.token,
            user_id=sample_refresh_token.user_id,
            expires_at=sample_refresh_token.expires_at,
            device_info=sample_refresh_token.device_info,
            created_at=sample_refresh_token.created_at,
            is_active=sample_refresh_token.is_active,
            last_used_at=sample_refresh_token.last_used_at,
        )
    
    @pytest.mark.asyncio
    async def test_save_refresh_token(self, repository, mock_session, sample_refresh_token):
        """Test saving a refresh token."""
        # Arrange
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()
        
        # Act
        result = await repository.save(sample_refresh_token)
        
        # Assert
        assert isinstance(result, RefreshToken)
        assert result.token == sample_refresh_token.token
        assert result.user_id == sample_refresh_token.user_id
        
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_by_token_found(self, repository, mock_session, sample_refresh_token_model):
        """Test getting refresh token by token value when found."""
        # Arrange
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_refresh_token_model
        mock_session.execute.return_value = mock_result
        
        # Act
        result = await repository.get_by_token(sample_refresh_token_model.token)
        
        # Assert
        assert result is not None
        assert isinstance(result, RefreshToken)
        assert result.token == sample_refresh_token_model.token
        assert result.user_id == sample_refresh_token_model.user_id
        
        mock_session.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_by_token_not_found(self, repository, mock_session):
        """Test getting refresh token by token value when not found."""
        # Arrange
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result
        
        # Act
        result = await repository.get_by_token("nonexistent_token")
        
        # Assert
        assert result is None
        mock_session.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repository, mock_session, sample_refresh_token_model):
        """Test getting refresh token by ID when found."""
        # Arrange
        mock_session.get.return_value = sample_refresh_token_model
        
        # Act
        result = await repository.get_by_id(sample_refresh_token_model.id)
        
        # Assert
        assert result is not None
        assert isinstance(result, RefreshToken)
        assert result.id == sample_refresh_token_model.id
        
        mock_session.get.assert_called_once_with(RefreshTokenModel, sample_refresh_token_model.id)
    
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repository, mock_session):
        """Test getting refresh token by ID when not found."""
        # Arrange
        token_id = uuid4()
        mock_session.get.return_value = None
        
        # Act
        result = await repository.get_by_id(token_id)
        
        # Assert
        assert result is None
        mock_session.get.assert_called_once_with(RefreshTokenModel, token_id)
    
    @pytest.mark.asyncio
    async def test_get_active_tokens_for_user(self, repository, mock_session, sample_refresh_token_model):
        """Test getting active tokens for a user."""
        # Arrange
        user_id = sample_refresh_token_model.user_id
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = [sample_refresh_token_model]
        mock_session.execute.return_value = mock_result
        
        # Act
        result = await repository.get_active_tokens_for_user(user_id)
        
        # Assert
        assert len(result) == 1
        assert isinstance(result[0], RefreshToken)
        assert result[0].user_id == user_id
        
        mock_session.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_revoke_token_success(self, repository, mock_session):
        """Test revoking a token successfully."""
        # Arrange
        token = "test_token"
        mock_result = Mock()
        mock_result.rowcount = 1
        mock_session.execute.return_value = mock_result
        mock_session.commit = AsyncMock()
        
        # Act
        result = await repository.revoke_token(token)
        
        # Assert
        assert result is True
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_revoke_token_not_found(self, repository, mock_session):
        """Test revoking a token that doesn't exist."""
        # Arrange
        token = "nonexistent_token"
        mock_result = Mock()
        mock_result.rowcount = 0
        mock_session.execute.return_value = mock_result
        mock_session.commit = AsyncMock()
        
        # Act
        result = await repository.revoke_token(token)
        
        # Assert
        assert result is False
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_revoke_all_user_tokens(self, repository, mock_session):
        """Test revoking all tokens for a user."""
        # Arrange
        user_id = uuid4()
        mock_result = Mock()
        mock_result.rowcount = 3  # 3 tokens revoked
        mock_session.execute.return_value = mock_result
        mock_session.commit = AsyncMock()
        
        # Act
        result = await repository.revoke_all_user_tokens(user_id)
        
        # Assert
        assert result == 3
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_expired_tokens(self, repository, mock_session):
        """Test deleting expired tokens."""
        # Arrange
        mock_result = Mock()
        mock_result.rowcount = 5  # 5 expired tokens deleted
        mock_session.execute.return_value = mock_result
        mock_session.commit = AsyncMock()
        
        # Act
        result = await repository.delete_expired_tokens()
        
        # Assert
        assert result == 5
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_refresh_token(self, repository, mock_session, sample_refresh_token, sample_refresh_token_model):
        """Test updating a refresh token."""
        # Arrange
        mock_session.execute = AsyncMock()
        mock_session.commit = AsyncMock()
        mock_session.get.return_value = sample_refresh_token_model
        
        # Modify the token
        sample_refresh_token.mark_as_used()
        
        # Act
        result = await repository.update(sample_refresh_token)
        
        # Assert
        assert isinstance(result, RefreshToken)
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.get.assert_called_once_with(RefreshTokenModel, sample_refresh_token.id)
    
    @pytest.mark.asyncio
    async def test_delete_refresh_token_success(self, repository, mock_session):
        """Test deleting a refresh token successfully."""
        # Arrange
        token_id = uuid4()
        mock_result = Mock()
        mock_result.rowcount = 1
        mock_session.execute.return_value = mock_result
        mock_session.commit = AsyncMock()
        
        # Act
        result = await repository.delete(token_id)
        
        # Assert
        assert result is True
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_refresh_token_not_found(self, repository, mock_session):
        """Test deleting a refresh token that doesn't exist."""
        # Arrange
        token_id = uuid4()
        mock_result = Mock()
        mock_result.rowcount = 0
        mock_session.execute.return_value = mock_result
        mock_session.commit = AsyncMock()
        
        # Act
        result = await repository.delete(token_id)
        
        # Assert
        assert result is False
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_count_active_tokens_for_user(self, repository, mock_session):
        """Test counting active tokens for a user."""
        # Arrange
        user_id = uuid4()
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = ["token1", "token2", "token3"]
        mock_session.execute.return_value = mock_result
        
        # Act
        result = await repository.count_active_tokens_for_user(user_id)
        
        # Assert
        assert result == 3
        mock_session.execute.assert_called_once()
    
    def test_model_to_entity_conversion(self, repository, sample_refresh_token_model):
        """Test converting SQLAlchemy model to domain entity."""
        # Act
        result = repository._model_to_entity(sample_refresh_token_model)
        
        # Assert
        assert isinstance(result, RefreshToken)
        assert result.token == sample_refresh_token_model.token
        assert result.user_id == sample_refresh_token_model.user_id
        assert result.expires_at == sample_refresh_token_model.expires_at
        assert result.device_info == sample_refresh_token_model.device_info
        assert result.id == sample_refresh_token_model.id
        assert result.created_at == sample_refresh_token_model.created_at
        assert result.is_active == sample_refresh_token_model.is_active
        assert result.last_used_at == sample_refresh_token_model.last_used_at
