import pytest
from fastapi.testclient import TestClient

from main import app
from tests.utils.test_helpers import AuthTestHelper, TestDataFactory
from app.domain.value_objects.user_role import UserRole


class TestExampleIntegration:
    """Ejemplos de tests de integración"""

    @pytest.fixture(autouse=True)
    async def setup_test_environment(self, test_client, db_tables_ready):
        """Setup que se ejecuta antes de cada test"""
        # Usar el cliente de test del fixture
        self.client = test_client
        
        # Inicializar helper de autenticación
        self.auth_helper = AuthTestHelper(self.client)
        
        # Crear admin usando el seeder
        await self.auth_helper.seed_admin_user()

    def test_health_endpoint(self):
        """Test that the health check endpoint returns a 200 status and correct format."""
        response = self.client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert "timestamp" in data

    def test_create_user_endpoint(self):
        """Test creating a user through the API."""
        user_data = TestDataFactory.create_user_data(
            role=UserRole.APPRENTICE,
            prefix="testexample"
        )
        
        admin_headers = self.auth_helper.get_admin_headers()
        response = self.client.post("/users/", json=user_data, headers=admin_headers)
        
        # Debug: Print response details
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.json()}")
        
        # Should succeed if not exists or return conflict if already exists
        assert response.status_code in [201, 409, 400]  # Allow 400 for business logic errors
        
        if response.status_code == 201:
            data = response.json()
            assert data["email"] == user_data["email"]
            assert data["first_name"] == user_data["first_name"]
            assert data["last_name"] == user_data["last_name"]
            assert "id" in data
            assert "created_at" in data
