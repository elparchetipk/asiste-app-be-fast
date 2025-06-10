"""Unit tests for RefreshTokenUseCase."""

import pytest
from unittest.mock import AsyncMock, Mock
from datetime import datetime, timezone, timedelta
from uuid import uuid4

from app.application.use_cases.auth_use_cases import RefreshTokenUseCase
from app.application.dtos.user_dtos import RefreshTokenDTO, RefreshTokenResponseDTO
from app.domain.entities.refresh_token_entity import RefreshToken
from app.domain.entities.user_entity import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.document_number import DocumentNumber
from app.domain.value_objects.document_type import DocumentType
from app.domain.value_objects.user_role import UserRole
from app.domain.exceptions.user_exceptions import (
    InvalidTokenError,
    UserNotFoundError,
    UserInactiveError,
)


class TestRefreshTokenUseCase:
    """Test cases for RefreshTokenUseCase."""
    
    @pytest.fixture
    def mock_user_repository(self):
        """Mock user repository."""
        return AsyncMock()
    
    @pytest.fixture
    def mock_refresh_token_repository(self):
        """Mock refresh token repository."""
        return AsyncMock()
    
    @pytest.fixture
    def mock_token_service(self):
        """Mock token service."""
        return Mock()
    
    @pytest.fixture
    def use_case(self, mock_user_repository, mock_refresh_token_repository, mock_token_service):
        """Create RefreshTokenUseCase instance with mocked dependencies."""
        return RefreshTokenUseCase(
            user_repository=mock_user_repository,
            refresh_token_repository=mock_refresh_token_repository,
            token_service=mock_token_service
        )
    
    @pytest.fixture
    def sample_user(self):
        """Create a sample user for testing."""
        return User(
            first_name="John",
            last_name="Doe",
            email=Email("john.doe@example.com"),
            document_number=DocumentNumber("12345678", DocumentType.CC),
            hashed_password="hashed_password",
            role=UserRole.APPRENTICE
        )
    
    @pytest.fixture
    def sample_refresh_token(self, sample_user):
        """Create a sample refresh token for testing."""
        return RefreshToken.create_for_user(
            user_id=sample_user.id,
            device_info="Test Device"
        )
    
    @pytest.mark.asyncio
    async def test_execute_with_valid_token_success(
        self,
        use_case,
        mock_user_repository,
        mock_refresh_token_repository,
        mock_token_service,
        sample_user,
        sample_refresh_token
    ):
        """Test successful token refresh with valid token."""
        # Arrange
        refresh_dto = RefreshTokenDTO(refresh_token=sample_refresh_token.token)
        new_access_token = "new_access_token_123"
        new_refresh_token = sample_refresh_token.rotate()
        
        mock_refresh_token_repository.get_by_token.return_value = sample_refresh_token
        mock_user_repository.get_by_id.return_value = sample_user
        mock_token_service.create_access_token.return_value = new_access_token
        mock_refresh_token_repository.save.return_value = new_refresh_token
        mock_refresh_token_repository.update.return_value = sample_refresh_token
        
        # Act
        result = await use_case.execute(refresh_dto)
        
        # Assert
        assert isinstance(result, RefreshTokenResponseDTO)
        assert result.access_token == new_access_token
        assert result.refresh_token == new_refresh_token.token
        assert result.token_type == "bearer"
        assert result.expires_in == 3600
        
        # Verify repository calls
        mock_refresh_token_repository.get_by_token.assert_called_once_with(sample_refresh_token.token)
        mock_user_repository.get_by_id.assert_called_once_with(sample_refresh_token.user_id)
        mock_token_service.create_access_token.assert_called_once_with(
            user_id=sample_user.id,
            role=sample_user.role.value,
            expires_delta=3600
        )
        mock_refresh_token_repository.save.assert_called_once()
        mock_refresh_token_repository.update.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_with_nonexistent_token(
        self,
        use_case,
        mock_refresh_token_repository
    ):
        """Test refresh with non-existent token raises InvalidTokenError."""
        # Arrange
        refresh_dto = RefreshTokenDTO(refresh_token="nonexistent_token")
        mock_refresh_token_repository.get_by_token.return_value = None
        
        # Act & Assert
        with pytest.raises(InvalidTokenError, match="Invalid refresh token"):
            await use_case.execute(refresh_dto)
        
        mock_refresh_token_repository.get_by_token.assert_called_once_with("nonexistent_token")
    
    @pytest.mark.asyncio
    async def test_execute_with_revoked_token(
        self,
        use_case,
        mock_refresh_token_repository,
        sample_refresh_token
    ):
        """Test refresh with revoked token raises InvalidTokenError and cleans up."""
        # Arrange
        sample_refresh_token.revoke()  # Revoke the token
        refresh_dto = RefreshTokenDTO(refresh_token=sample_refresh_token.token)
        
        mock_refresh_token_repository.get_by_token.return_value = sample_refresh_token
        
        # Act & Assert
        with pytest.raises(InvalidTokenError):
            await use_case.execute(refresh_dto)
        
        # Verify cleanup was called
        mock_refresh_token_repository.delete.assert_called_once_with(sample_refresh_token.id)
    
    @pytest.mark.asyncio
    async def test_execute_with_expired_token(
        self,
        use_case,
        mock_refresh_token_repository,
        sample_user
    ):
        """Test refresh with expired token raises InvalidTokenError and cleans up."""
        # Arrange
        expired_token = RefreshToken(
            token="expired_token",
            user_id=sample_user.id,
            expires_at=datetime.now(timezone.utc) - timedelta(minutes=1)
        )
        refresh_dto = RefreshTokenDTO(refresh_token=expired_token.token)
        
        mock_refresh_token_repository.get_by_token.return_value = expired_token
        
        # Act & Assert
        with pytest.raises(InvalidTokenError):
            await use_case.execute(refresh_dto)
        
        # Verify cleanup was called
        mock_refresh_token_repository.delete.assert_called_once_with(expired_token.id)
    
    @pytest.mark.asyncio
    async def test_execute_with_nonexistent_user(
        self,
        use_case,
        mock_user_repository,
        mock_refresh_token_repository,
        sample_refresh_token
    ):
        """Test refresh with token for non-existent user raises UserNotFoundError."""
        # Arrange
        refresh_dto = RefreshTokenDTO(refresh_token=sample_refresh_token.token)
        
        mock_refresh_token_repository.get_by_token.return_value = sample_refresh_token
        mock_user_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(UserNotFoundError, match=f"User not found: {sample_refresh_token.user_id}"):
            await use_case.execute(refresh_dto)
    
    @pytest.mark.asyncio
    async def test_execute_with_inactive_user(
        self,
        use_case,
        mock_user_repository,
        mock_refresh_token_repository,
        mock_token_service,
        sample_user,
        sample_refresh_token
    ):
        """Test refresh with token for inactive user raises UserInactiveError and revokes tokens."""
        # Arrange
        sample_user.deactivate()  # Deactivate the user
        refresh_dto = RefreshTokenDTO(refresh_token=sample_refresh_token.token)
        
        mock_refresh_token_repository.get_by_token.return_value = sample_refresh_token
        mock_user_repository.get_by_id.return_value = sample_user
        
        # Act & Assert
        with pytest.raises(UserInactiveError, match=f"User account is inactive: {sample_user.id}"):
            await use_case.execute(refresh_dto)
        
        # Verify all user tokens were revoked
        mock_refresh_token_repository.revoke_all_user_tokens.assert_called_once_with(sample_user.id)
    
    @pytest.mark.asyncio
    async def test_execute_marks_token_as_used(
        self,
        use_case,
        mock_user_repository,
        mock_refresh_token_repository,
        mock_token_service,
        sample_user,
        sample_refresh_token
    ):
        """Test that token is marked as used during refresh process."""
        # Arrange
        refresh_dto = RefreshTokenDTO(refresh_token=sample_refresh_token.token)
        original_last_used = sample_refresh_token.last_used_at
        
        mock_refresh_token_repository.get_by_token.return_value = sample_refresh_token
        mock_user_repository.get_by_id.return_value = sample_user
        mock_token_service.create_access_token.return_value = "new_token"
        
        # Act
        await use_case.execute(refresh_dto)
        
        # Assert
        assert sample_refresh_token.last_used_at != original_last_used
        assert sample_refresh_token.last_used_at is not None
    
    @pytest.mark.asyncio
    async def test_execute_creates_rotated_token(
        self,
        use_case,
        mock_user_repository,
        mock_refresh_token_repository,
        mock_token_service,
        sample_user,
        sample_refresh_token
    ):
        """Test that a new rotated token is created and saved."""
        # Arrange
        refresh_dto = RefreshTokenDTO(refresh_token=sample_refresh_token.token)
        original_token_value = sample_refresh_token.token
        
        mock_refresh_token_repository.get_by_token.return_value = sample_refresh_token
        mock_user_repository.get_by_id.return_value = sample_user
        mock_token_service.create_access_token.return_value = "new_access_token"
        
        # Mock the rotate method to return a new token
        new_refresh_token = RefreshToken.create_for_user(sample_user.id)
        sample_refresh_token.rotate = Mock(return_value=new_refresh_token)
        
        # Act
        result = await use_case.execute(refresh_dto)
        
        # Assert
        assert result.refresh_token == new_refresh_token.token
        assert result.refresh_token != original_token_value
        
        # Verify new token was saved
        mock_refresh_token_repository.save.assert_called_once()
        
        # Verify old token was updated (marked as used)
        mock_refresh_token_repository.update.assert_called_once_with(sample_refresh_token)
    
    @pytest.mark.asyncio
    async def test_execute_with_correct_token_service_parameters(
        self,
        use_case,
        mock_user_repository,
        mock_refresh_token_repository,
        mock_token_service,
        sample_user,
        sample_refresh_token
    ):
        """Test that token service is called with correct parameters."""
        # Arrange
        refresh_dto = RefreshTokenDTO(refresh_token=sample_refresh_token.token)
        
        mock_refresh_token_repository.get_by_token.return_value = sample_refresh_token
        mock_user_repository.get_by_id.return_value = sample_user
        mock_token_service.create_access_token.return_value = "new_access_token"
        
        # Act
        await use_case.execute(refresh_dto)
        
        # Assert
        mock_token_service.create_access_token.assert_called_once_with(
            user_id=sample_user.id,
            role=sample_user.role.value,
            expires_delta=3600
        )
