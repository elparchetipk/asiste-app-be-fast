"""
Tests simples para verificar que los endpoints críticos de autenticación funcionan.
HU-BE-005, HU-BE-006, HU-BE-007: Password reset y force change functionality.
"""

import pytest
from fastapi.testclient import TestClient
from main import app


class TestCriticalAuthEndpointsSimple:
    """Tests simples para endpoints críticos de autenticación."""

    @pytest.fixture(autouse=True)
    def setup(self, test_client):
        """Setup simple usando el test_client disponible."""
        self.client = test_client

    def test_forgot_password_endpoint_exists(self):
        """Test que el endpoint de forgot password existe."""
        response = self.client.post("/api/v1/auth/forgot-password", json={
            "email": "test@example.com"
        })
        
        # Debería responder (aunque sea error de validación o éxito)
        assert response.status_code in [200, 400, 422, 500]

    def test_reset_password_endpoint_exists(self):
        """Test que el endpoint de reset password existe."""
        response = self.client.post("/api/v1/auth/reset-password", json={
            "token": "test_token",
            "new_password": "TestPassword123!"
        })
        
        # Debería responder (aunque sea error de validación o éxito)
        assert response.status_code in [200, 400, 422, 500]

    def test_force_change_password_endpoint_exists(self):
        """Test que el endpoint de force change password existe."""
        response = self.client.post("/api/v1/auth/force-change-password", json={
            "new_password": "TestPassword123!"
        })
        
        # Debería responder (aunque sea error de autorización)
        assert response.status_code in [200, 401, 403, 422, 500]

    def test_forgot_password_email_validation(self):
        """Test validación de email en forgot password."""
        response = self.client.post("/api/v1/auth/forgot-password", json={
            "email": "invalid-email"
        })
        
        # Debería fallar validación de email
        assert response.status_code == 422

    def test_reset_password_validation(self):
        """Test validación de campos en reset password."""
        # Sin token
        response = self.client.post("/api/v1/auth/reset-password", json={
            "new_password": "TestPassword123!"
        })
        assert response.status_code == 422
        
        # Sin password
        response = self.client.post("/api/v1/auth/reset-password", json={
            "token": "test_token"
        })
        assert response.status_code == 422

    def test_force_change_password_requires_auth(self):
        """Test que force change password requiere autenticación."""
        response = self.client.post("/api/v1/auth/force-change-password", json={
            "new_password": "TestPassword123!"
        })
        
        # Debería requerir autenticación (401 o 403)
        assert response.status_code in [401, 403]

    def test_openapi_includes_new_endpoints(self):
        """Test que los nuevos endpoints aparecen en la documentación OpenAPI."""
        response = self.client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_data = response.json()
        paths = openapi_data.get("paths", {})
        
        # Verificar que los endpoints existen en la documentación
        assert "/api/v1/auth/forgot-password" in paths
        assert "/api/v1/auth/reset-password" in paths
        assert "/api/v1/auth/force-change-password" in paths
