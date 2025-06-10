"""Integration tests for refresh token endpoint."""

import pytest
from httpx import AsyncClient
from datetime import datetime, timezone, timedelta
from uuid import uuid4

from app.main import app
from app.domain.entities.refresh_token_entity import RefreshToken
from app.domain.entities.user_entity import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.document_number import DocumentNumber
from app.domain.value_objects.document_type import DocumentType
from app.domain.value_objects.user_role import UserRole


class TestRefreshTokenEndpoint:
    """Integration tests for refresh token endpoint."""
    
    @pytest.fixture
    async def client(self):
        """Create test client."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac
    
    @pytest.fixture
    def sample_user(self):
        """Create a sample user for testing."""
        return User(
            first_name="John",
            last_name="Doe",
            email=Email("john.doe@example.com"),
            document_number=DocumentNumber("12345678", DocumentType.CC),
            hashed_password="$2b$12$hashed_password",
            role=UserRole.APPRENTICE
        )
    
    @pytest.fixture
    def valid_refresh_token(self, sample_user):
        """Create a valid refresh token for testing."""
        return RefreshToken.create_for_user(
            user_id=sample_user.id,
            device_info="Test Device",
            expires_in_days=30
        )
    
    @pytest.mark.asyncio
    async def test_refresh_token_success(self, client, mocker, sample_user, valid_refresh_token):
        """Test successful token refresh."""
        # Mock dependencies
        mock_refresh_token_repo = mocker.patch(
            "app.dependencies.get_refresh_token_repository"
        )
        mock_user_repo = mocker.patch(
            "app.dependencies.get_user_repository"
        )
        mock_token_service = mocker.patch(
            "app.dependencies.get_token_service"
        )
        
        # Setup mocks
        refresh_repo_instance = mock_refresh_token_repo.return_value
        user_repo_instance = mock_user_repo.return_value
        token_service_instance = mock_token_service.return_value
        
        refresh_repo_instance.get_by_token.return_value = valid_refresh_token
        user_repo_instance.get_by_id.return_value = sample_user
        token_service_instance.create_access_token.return_value = "new_access_token_123"
        
        # Mock rotate method
        new_refresh_token = RefreshToken.create_for_user(sample_user.id)
        valid_refresh_token.rotate = mocker.Mock(return_value=new_refresh_token)
        
        # Request payload
        payload = {
            "refresh_token": valid_refresh_token.token
        }
        
        # Act
        response = await client.post("/api/v1/auth/refresh", json=payload)
        
        # Assert
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "token_type" in data
        assert "expires_in" in data
        
        assert data["access_token"] == "new_access_token_123"
        assert data["refresh_token"] == new_refresh_token.token
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 3600
        
        # Verify repository interactions
        refresh_repo_instance.get_by_token.assert_called_once_with(valid_refresh_token.token)
        user_repo_instance.get_by_id.assert_called_once_with(valid_refresh_token.user_id)
        token_service_instance.create_access_token.assert_called_once()
        refresh_repo_instance.save.assert_called_once()
        refresh_repo_instance.update.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_refresh_token_invalid_token(self, client, mocker):
        """Test refresh with invalid token returns 401."""
        # Mock dependencies
        mock_refresh_token_repo = mocker.patch(
            "app.dependencies.get_refresh_token_repository"
        )
        
        # Setup mocks
        refresh_repo_instance = mock_refresh_token_repo.return_value
        refresh_repo_instance.get_by_token.return_value = None
        
        # Request payload
        payload = {
            "refresh_token": "invalid_token_123"
        }
        
        # Act
        response = await client.post("/api/v1/auth/refresh", json=payload)
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "Invalid refresh token" in data["detail"]
        assert data.get("headers", {}).get("WWW-Authenticate") == "Bearer"
    
    @pytest.mark.asyncio
    async def test_refresh_token_expired_token(self, client, mocker, sample_user):
        """Test refresh with expired token returns 401."""
        # Create expired token
        expired_token = RefreshToken(
            token="expired_token_123",
            user_id=sample_user.id,
            expires_at=datetime.now(timezone.utc) - timedelta(minutes=1)
        )
        
        # Mock dependencies
        mock_refresh_token_repo = mocker.patch(
            "app.dependencies.get_refresh_token_repository"
        )
        
        # Setup mocks
        refresh_repo_instance = mock_refresh_token_repo.return_value
        refresh_repo_instance.get_by_token.return_value = expired_token
        
        # Request payload
        payload = {
            "refresh_token": expired_token.token
        }
        
        # Act
        response = await client.post("/api/v1/auth/refresh", json=payload)
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        
        # Verify cleanup was called
        refresh_repo_instance.delete.assert_called_once_with(expired_token.id)
    
    @pytest.mark.asyncio
    async def test_refresh_token_user_not_found(self, client, mocker, valid_refresh_token):
        """Test refresh with token for non-existent user returns 404."""
        # Mock dependencies
        mock_refresh_token_repo = mocker.patch(
            "app.dependencies.get_refresh_token_repository"
        )
        mock_user_repo = mocker.patch(
            "app.dependencies.get_user_repository"
        )
        
        # Setup mocks
        refresh_repo_instance = mock_refresh_token_repo.return_value
        user_repo_instance = mock_user_repo.return_value
        
        refresh_repo_instance.get_by_token.return_value = valid_refresh_token
        user_repo_instance.get_by_id.return_value = None
        
        # Request payload
        payload = {
            "refresh_token": valid_refresh_token.token
        }
        
        # Act
        response = await client.post("/api/v1/auth/refresh", json=payload)
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert str(valid_refresh_token.user_id) in data["detail"]
    
    @pytest.mark.asyncio
    async def test_refresh_token_inactive_user(self, client, mocker, sample_user, valid_refresh_token):
        """Test refresh with token for inactive user returns 403."""
        # Deactivate user
        sample_user.deactivate()
        
        # Mock dependencies
        mock_refresh_token_repo = mocker.patch(
            "app.dependencies.get_refresh_token_repository"
        )
        mock_user_repo = mocker.patch(
            "app.dependencies.get_user_repository"
        )
        
        # Setup mocks
        refresh_repo_instance = mock_refresh_token_repo.return_value
        user_repo_instance = mock_user_repo.return_value
        
        refresh_repo_instance.get_by_token.return_value = valid_refresh_token
        user_repo_instance.get_by_id.return_value = sample_user
        
        # Request payload
        payload = {
            "refresh_token": valid_refresh_token.token
        }
        
        # Act
        response = await client.post("/api/v1/auth/refresh", json=payload)
        
        # Assert
        assert response.status_code == 403
        data = response.json()
        assert "detail" in data
        assert "inactive" in data["detail"].lower()
        
        # Verify all user tokens were revoked
        refresh_repo_instance.revoke_all_user_tokens.assert_called_once_with(sample_user.id)
    
    @pytest.mark.asyncio
    async def test_refresh_token_missing_payload(self, client):
        """Test refresh without payload returns 422."""
        # Act
        response = await client.post("/api/v1/auth/refresh", json={})
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    @pytest.mark.asyncio
    async def test_refresh_token_invalid_payload_format(self, client):
        """Test refresh with invalid payload format returns 422."""
        # Request with wrong field name
        payload = {
            "token": "some_token"  # Should be "refresh_token"
        }
        
        # Act
        response = await client.post("/api/v1/auth/refresh", json=payload)
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    @pytest.mark.asyncio
    async def test_refresh_token_empty_token(self, client):
        """Test refresh with empty token returns 422."""
        # Request payload
        payload = {
            "refresh_token": ""
        }
        
        # Act
        response = await client.post("/api/v1/auth/refresh", json=payload)
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    @pytest.mark.asyncio
    async def test_refresh_token_content_type_json_required(self, client, valid_refresh_token):
        """Test refresh endpoint requires JSON content type."""
        # Act - Send form data instead of JSON
        response = await client.post(
            "/api/v1/auth/refresh",
            data={"refresh_token": valid_refresh_token.token}
        )
        
        # Assert
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_refresh_token_endpoint_documentation(self, client):
        """Test that refresh token endpoint is documented in OpenAPI."""
        # Act
        response = await client.get("/docs")
        
        # Assert
        assert response.status_code == 200
        # The endpoint should be documented in the OpenAPI spec
        # This is a basic check that the docs are accessible
    
    @pytest.mark.asyncio
    async def test_refresh_token_cors_headers(self, client, mocker, sample_user, valid_refresh_token):
        """Test that CORS headers are included in response."""
        # Mock dependencies for successful refresh
        mock_refresh_token_repo = mocker.patch(
            "app.dependencies.get_refresh_token_repository"
        )
        mock_user_repo = mocker.patch(
            "app.dependencies.get_user_repository"
        )
        mock_token_service = mocker.patch(
            "app.dependencies.get_token_service"
        )
        
        # Setup mocks
        refresh_repo_instance = mock_refresh_token_repo.return_value
        user_repo_instance = mock_user_repo.return_value
        token_service_instance = mock_token_service.return_value
        
        refresh_repo_instance.get_by_token.return_value = valid_refresh_token
        user_repo_instance.get_by_id.return_value = sample_user
        token_service_instance.create_access_token.return_value = "new_access_token"
        
        # Request payload
        payload = {
            "refresh_token": valid_refresh_token.token
        }
        
        # Act
        response = await client.post(
            "/api/v1/auth/refresh",
            json=payload,
            headers={"Origin": "http://localhost:3000"}
        )
        
        # Assert
        assert response.status_code == 200
        
        # Check CORS headers are present (configured in main.py)
        headers = response.headers
        assert "access-control-allow-origin" in headers or "Access-Control-Allow-Origin" in headers
