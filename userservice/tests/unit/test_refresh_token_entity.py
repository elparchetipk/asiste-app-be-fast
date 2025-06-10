"""Unit tests for RefreshToken entity."""

import pytest
from datetime import datetime, timezone, timedelta
from uuid import uuid4

from app.domain.entities.refresh_token_entity import RefreshToken
from app.domain.exceptions.user_exceptions import InvalidTokenError


class TestRefreshTokenEntity:
    """Test cases for RefreshToken domain entity."""
    
    def test_create_refresh_token_with_all_params(self):
        """Test creating a refresh token with all parameters."""
        # Arrange
        token_id = uuid4()
        token = "test_token_123"
        user_id = uuid4()
        expires_at = datetime.now(timezone.utc) + timedelta(days=30)
        device_info = "Mozilla/5.0..."
        created_at = datetime.now(timezone.utc)
        
        # Act
        refresh_token = RefreshToken(
            id=token_id,
            token=token,
            user_id=user_id,
            expires_at=expires_at,
            device_info=device_info,
            created_at=created_at,
            is_active=True,
            last_used_at=None
        )
        
        # Assert
        assert refresh_token.id == token_id
        assert refresh_token.token == token
        assert refresh_token.user_id == user_id
        assert refresh_token.expires_at == expires_at
        assert refresh_token.device_info == device_info
        assert refresh_token.created_at == created_at
        assert refresh_token.is_active is True
        assert refresh_token.last_used_at is None
    
    def test_create_refresh_token_with_defaults(self):
        """Test creating a refresh token with default values."""
        # Arrange
        token = "test_token_123"
        user_id = uuid4()
        expires_at = datetime.now(timezone.utc) + timedelta(days=30)
        
        # Act
        refresh_token = RefreshToken(
            token=token,
            user_id=user_id,
            expires_at=expires_at
        )
        
        # Assert
        assert refresh_token.token == token
        assert refresh_token.user_id == user_id
        assert refresh_token.expires_at == expires_at
        assert refresh_token.device_info is None
        assert refresh_token.is_active is True
        assert refresh_token.last_used_at is None
        assert isinstance(refresh_token.id, type(uuid4()))
        assert isinstance(refresh_token.created_at, datetime)
    
    def test_create_for_user_factory_method(self):
        """Test creating refresh token using factory method."""
        # Arrange
        user_id = uuid4()
        device_info = "iOS App"
        
        # Act
        refresh_token = RefreshToken.create_for_user(
            user_id=user_id,
            device_info=device_info,
            expires_in_days=7
        )
        
        # Assert
        assert refresh_token.user_id == user_id
        assert refresh_token.device_info == device_info
        assert refresh_token.is_active is True
        assert len(refresh_token.token) == 86  # URL-safe base64 length for 64 bytes
        assert refresh_token.expires_at > datetime.now(timezone.utc) + timedelta(days=6)
        assert refresh_token.expires_at < datetime.now(timezone.utc) + timedelta(days=8)
    
    def test_is_valid_with_active_non_expired_token(self):
        """Test is_valid returns True for active, non-expired token."""
        # Arrange
        refresh_token = RefreshToken.create_for_user(
            user_id=uuid4(),
            expires_in_days=1
        )
        
        # Act & Assert
        assert refresh_token.is_valid() is True
    
    def test_is_valid_with_expired_token(self):
        """Test is_valid returns False for expired token."""
        # Arrange
        expired_time = datetime.now(timezone.utc) - timedelta(minutes=1)
        refresh_token = RefreshToken(
            token="expired_token",
            user_id=uuid4(),
            expires_at=expired_time
        )
        
        # Act & Assert
        assert refresh_token.is_valid() is False
    
    def test_is_valid_with_revoked_token(self):
        """Test is_valid returns False for revoked token."""
        # Arrange
        refresh_token = RefreshToken.create_for_user(
            user_id=uuid4(),
            expires_in_days=1
        )
        refresh_token.revoke()
        
        # Act & Assert
        assert refresh_token.is_valid() is False
    
    def test_is_expired_with_expired_token(self):
        """Test is_expired returns True for expired token."""
        # Arrange
        expired_time = datetime.now(timezone.utc) - timedelta(minutes=1)
        refresh_token = RefreshToken(
            token="expired_token",
            user_id=uuid4(),
            expires_at=expired_time
        )
        
        # Act & Assert
        assert refresh_token.is_expired() is True
    
    def test_is_expired_with_valid_token(self):
        """Test is_expired returns False for valid token."""
        # Arrange
        refresh_token = RefreshToken.create_for_user(
            user_id=uuid4(),
            expires_in_days=1
        )
        
        # Act & Assert
        assert refresh_token.is_expired() is False
    
    def test_revoke_token(self):
        """Test revoking a token."""
        # Arrange
        refresh_token = RefreshToken.create_for_user(user_id=uuid4())
        assert refresh_token.is_active is True
        
        # Act
        refresh_token.revoke()
        
        # Assert
        assert refresh_token.is_active is False
    
    def test_mark_as_used(self):
        """Test marking token as used updates last_used_at."""
        # Arrange
        refresh_token = RefreshToken.create_for_user(user_id=uuid4())
        assert refresh_token.last_used_at is None
        
        # Act
        refresh_token.mark_as_used()
        
        # Assert
        assert refresh_token.last_used_at is not None
        assert isinstance(refresh_token.last_used_at, datetime)
        assert refresh_token.last_used_at.tzinfo == timezone.utc
    
    def test_validate_for_refresh_with_valid_token(self):
        """Test validate_for_refresh passes for valid token."""
        # Arrange
        refresh_token = RefreshToken.create_for_user(user_id=uuid4())
        
        # Act & Assert - Should not raise exception
        refresh_token.validate_for_refresh()
    
    def test_validate_for_refresh_with_revoked_token(self):
        """Test validate_for_refresh raises exception for revoked token."""
        # Arrange
        refresh_token = RefreshToken.create_for_user(user_id=uuid4())
        refresh_token.revoke()
        
        # Act & Assert
        with pytest.raises(InvalidTokenError, match="Refresh token has been revoked"):
            refresh_token.validate_for_refresh()
    
    def test_validate_for_refresh_with_expired_token(self):
        """Test validate_for_refresh raises exception for expired token."""
        # Arrange
        expired_time = datetime.now(timezone.utc) - timedelta(minutes=1)
        refresh_token = RefreshToken(
            token="expired_token",
            user_id=uuid4(),
            expires_at=expired_time
        )
        
        # Act & Assert
        with pytest.raises(InvalidTokenError, match="Refresh token has expired"):
            refresh_token.validate_for_refresh()
    
    def test_rotate_token(self):
        """Test rotating a token creates new token and revokes old one."""
        # Arrange
        original_user_id = uuid4()
        original_device = "Original Device"
        original_token = RefreshToken.create_for_user(
            user_id=original_user_id,
            device_info=original_device
        )
        original_token_value = original_token.token
        
        # Act
        new_token = original_token.rotate(device_info="New Device")
        
        # Assert
        # Original token should be revoked
        assert original_token.is_active is False
        
        # New token should be different and active
        assert new_token.token != original_token_value
        assert new_token.user_id == original_user_id
        assert new_token.device_info == "New Device"
        assert new_token.is_active is True
        assert new_token.is_valid() is True
    
    def test_rotate_token_preserves_device_info_when_not_provided(self):
        """Test rotating token preserves original device info when not provided."""
        # Arrange
        original_device = "Original Device"
        original_token = RefreshToken.create_for_user(
            user_id=uuid4(),
            device_info=original_device
        )
        
        # Act
        new_token = original_token.rotate()
        
        # Assert
        assert new_token.device_info == original_device
    
    def test_equality_based_on_token_value(self):
        """Test equality comparison based on token value."""
        # Arrange
        user_id = uuid4()
        token_value = "same_token_value"
        
        token1 = RefreshToken(
            token=token_value,
            user_id=user_id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=1)
        )
        
        token2 = RefreshToken(
            token=token_value,
            user_id=uuid4(),  # Different user
            expires_at=datetime.now(timezone.utc) + timedelta(days=2)  # Different expiry
        )
        
        token3 = RefreshToken(
            token="different_token",
            user_id=user_id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=1)
        )
        
        # Act & Assert
        assert token1 == token2  # Same token value
        assert token1 != token3  # Different token value
        assert token2 != token3  # Different token value
    
    def test_hash_based_on_token_value(self):
        """Test hash function based on token value."""
        # Arrange
        token_value = "test_token"
        token1 = RefreshToken(
            token=token_value,
            user_id=uuid4(),
            expires_at=datetime.now(timezone.utc) + timedelta(days=1)
        )
        
        token2 = RefreshToken(
            token=token_value,
            user_id=uuid4(),
            expires_at=datetime.now(timezone.utc) + timedelta(days=1)
        )
        
        # Act & Assert
        assert hash(token1) == hash(token2)
        assert hash(token1) == hash(token_value)
    
    def test_string_representation(self):
        """Test string representation of refresh token."""
        # Arrange
        token_id = uuid4()
        user_id = uuid4()
        expires_at = datetime.now(timezone.utc) + timedelta(days=1)
        
        refresh_token = RefreshToken(
            id=token_id,
            token="test_token",
            user_id=user_id,
            expires_at=expires_at
        )
        
        # Act
        str_repr = str(refresh_token)
        
        # Assert
        assert "RefreshToken" in str_repr
        assert str(token_id) in str_repr
        assert str(user_id) in str_repr
        assert str(expires_at) in str_repr
