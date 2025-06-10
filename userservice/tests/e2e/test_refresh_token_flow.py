"""End-to-end tests for refresh token functionality."""

import pytest
from httpx import AsyncClient
from datetime import datetime, timezone, timedelta

from app.main import app


class TestRefreshTokenE2E:
    """End-to-end tests for refresh token flow."""
    
    @pytest.fixture
    async def client(self):
        """Create test client."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac
    
    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for testing."""
        return {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@test.com",
            "document_number": "12345678",
            "document_type": "CC",
            "password": "SecurePassword123!",
            "role": "APPRENTICE"
        }
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Requires full database setup and user registration endpoint")
    async def test_complete_refresh_token_flow(self, client, sample_user_data):
        """Test complete flow: register → login → refresh → use new token."""
        # Step 1: Register user (when endpoint is implemented)
        register_response = await client.post("/api/v1/auth/register", json=sample_user_data)
        assert register_response.status_code == 201
        
        # Step 2: Login to get initial tokens
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = await client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        login_result = login_response.json()
        assert "access_token" in login_result
        assert "refresh_token" in login_result
        
        original_access_token = login_result["access_token"]
        original_refresh_token = login_result["refresh_token"]
        
        # Step 3: Use refresh token to get new tokens
        refresh_data = {
            "refresh_token": original_refresh_token
        }
        refresh_response = await client.post("/api/v1/auth/refresh", json=refresh_data)
        assert refresh_response.status_code == 200
        
        refresh_result = refresh_response.json()
        assert "access_token" in refresh_result
        assert "refresh_token" in refresh_result
        
        new_access_token = refresh_result["access_token"]
        new_refresh_token = refresh_result["refresh_token"]
        
        # Verify tokens are different
        assert new_access_token != original_access_token
        assert new_refresh_token != original_refresh_token
        
        # Step 4: Verify old refresh token is now invalid
        old_refresh_data = {
            "refresh_token": original_refresh_token
        }
        old_refresh_response = await client.post("/api/v1/auth/refresh", json=old_refresh_data)
        assert old_refresh_response.status_code == 401
        
        # Step 5: Verify new access token works (when protected endpoint is available)
        headers = {"Authorization": f"Bearer {new_access_token}"}
        profile_response = await client.get("/api/v1/users/profile", headers=headers)
        # This will work when profile endpoint is implemented
        # assert profile_response.status_code == 200
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Requires database setup")
    async def test_refresh_token_expiration_behavior(self, client, sample_user_data):
        """Test behavior when refresh token expires."""
        # This test would require:
        # 1. Creating a user with a refresh token
        # 2. Manually setting the token to be expired in the database
        # 3. Attempting to refresh and verifying it fails
        # 4. Verifying the expired token is cleaned up
        pass
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Requires database setup")
    async def test_multiple_device_token_management(self, client, sample_user_data):
        """Test managing refresh tokens across multiple devices."""
        # This test would simulate:
        # 1. Login from device 1 (get refresh token 1)
        # 2. Login from device 2 (get refresh token 2)
        # 3. Refresh from device 1 (should work)
        # 4. Refresh from device 2 (should work)
        # 5. Revoke all tokens for user
        # 6. Verify both tokens are invalid
        pass
    
    @pytest.mark.asyncio
    async def test_refresh_endpoint_openapi_documentation(self, client):
        """Test that refresh endpoint is properly documented in OpenAPI spec."""
        # Get OpenAPI spec
        response = await client.get("/openapi.json")
        assert response.status_code == 200
        
        spec = response.json()
        
        # Verify refresh endpoint is documented
        paths = spec.get("paths", {})
        refresh_path = paths.get("/api/v1/auth/refresh", {})
        
        assert "post" in refresh_path
        
        post_spec = refresh_path["post"]
        assert "summary" in post_spec or "description" in post_spec
        assert "requestBody" in post_spec
        assert "responses" in post_spec
        
        # Verify request schema
        request_body = post_spec["requestBody"]
        assert "content" in request_body
        assert "application/json" in request_body["content"]
        
        # Verify response schemas
        responses = post_spec["responses"]
        assert "200" in responses  # Success response
        assert "401" in responses  # Unauthorized response
    
    @pytest.mark.asyncio
    async def test_refresh_endpoint_rate_limiting(self, client):
        """Test rate limiting on refresh endpoint (if implemented)."""
        # This would test rate limiting by making many requests
        # Currently skipped as rate limiting may not be implemented
        refresh_data = {
            "refresh_token": "dummy_token"
        }
        
        # Make multiple requests rapidly
        responses = []
        for _ in range(10):
            response = await client.post("/api/v1/auth/refresh", json=refresh_data)
            responses.append(response)
        
        # All should return 401 (invalid token) rather than rate limit errors
        # If rate limiting is implemented, some might return 429
        for response in responses:
            assert response.status_code in [401, 429]
    
    @pytest.mark.asyncio
    async def test_refresh_endpoint_cors_headers(self, client):
        """Test CORS headers on refresh endpoint."""
        refresh_data = {
            "refresh_token": "dummy_token"
        }
        
        # Make request with Origin header
        response = await client.post(
            "/api/v1/auth/refresh",
            json=refresh_data,
            headers={"Origin": "http://localhost:3000"}
        )
        
        # Should have CORS headers (configured in main.py)
        headers = response.headers
        assert any(
            header.lower() in ["access-control-allow-origin", "Access-Control-Allow-Origin"]
            for header in headers.keys()
        )
    
    @pytest.mark.asyncio
    async def test_refresh_endpoint_request_validation(self, client):
        """Test request validation for refresh endpoint."""
        # Test various invalid request formats
        test_cases = [
            ({}, 422),  # Empty body
            ({"wrong_field": "value"}, 422),  # Wrong field name
            ({"refresh_token": ""}, 422),  # Empty token
            ({"refresh_token": None}, 422),  # Null token
            ({"refresh_token": 123}, 422),  # Wrong type
        ]
        
        for payload, expected_status in test_cases:
            response = await client.post("/api/v1/auth/refresh", json=payload)
            assert response.status_code == expected_status
            
            if expected_status == 422:
                error_data = response.json()
                assert "detail" in error_data
    
    @pytest.mark.asyncio
    async def test_refresh_endpoint_content_type_validation(self, client):
        """Test content type validation for refresh endpoint."""
        # Test form data instead of JSON
        response = await client.post(
            "/api/v1/auth/refresh",
            data={"refresh_token": "dummy_token"}
        )
        assert response.status_code == 422
        
        # Test plain text
        response = await client.post(
            "/api/v1/auth/refresh",
            content="dummy_token",
            headers={"Content-Type": "text/plain"}
        )
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_refresh_endpoint_response_format(self, client):
        """Test response format consistency."""
        refresh_data = {
            "refresh_token": "invalid_token"
        }
        
        response = await client.post("/api/v1/auth/refresh", json=refresh_data)
        
        # Should return JSON even for errors
        assert response.headers.get("content-type", "").startswith("application/json")
        
        # Should have proper error format
        if response.status_code >= 400:
            error_data = response.json()
            assert "detail" in error_data
            
            # For 401 errors, should have WWW-Authenticate header
            if response.status_code == 401:
                assert "WWW-Authenticate" in response.headers
