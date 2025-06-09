"""Tests de integración comprehensivos para todos los endpoints de usuarios"""

import pytest
import random
from fastapi.testclient import TestClient
from main import app
from tests.utils.test_helpers import AuthTestHelper, TestDataFactory
from app.domain.value_objects.user_role import UserRole


class TestUserEndpoints:
    """Suite de tests para todos los endpoints de usuarios"""

    @pytest.fixture(autouse=True)
    async def setup_test_environment(self, test_client, db_tables_ready):
        """Setup que se ejecuta antes de cada test"""
        # Usar el cliente de test del fixture
        self.client = test_client
        
        # Inicializar helper de autenticación
        self.auth_helper = AuthTestHelper(self.client)
        
        # Crear admin usando el seeder
        await self.auth_helper.seed_admin_user()
        
        # Crear un usuario base para tests que lo requieran
        self.base_user_data = TestDataFactory.create_user_data(
            role=UserRole.APPRENTICE,
            prefix="testbase"
        )
        
        # Crear el usuario para usar en tests usando admin headers
        admin_headers = self.auth_helper.get_admin_headers()
        response = self.client.post("/users/", json=self.base_user_data, headers=admin_headers)
        if response.status_code == 201:
            self.created_user = response.json()
            self.user_id = self.created_user["id"]
        else:
            pytest.fail(f"Failed to create base user: {response.text}")

    def test_create_user_success(self):
        """Test crear usuario exitosamente"""
        user_data = {
            "email": f"newuser-{random.randint(100000, 999999)}@test.com",
            "password": "SecurePass123!",
            "first_name": "New",
            "last_name": "User",
            "document_number": f"{random.randint(10000000, 99999999)}",
            "document_type": "CC",
            "role": "instructor"
        }
        
        response = self.client.post("/users/", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["first_name"] == user_data["first_name"]
        assert data["last_name"] == user_data["last_name"]
        assert data["document_number"] == user_data["document_number"]
        assert data["document_type"] == user_data["document_type"]
        assert data["role"] == user_data["role"]
        assert data["is_active"] is True
        assert data["must_change_password"] is True
        assert "id" in data
        assert "created_at" in data

    def test_create_user_duplicate_email(self):
        """Test crear usuario con email duplicado"""
        response = self.client.post("/users/", json=self.base_user_data)
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    def test_create_user_invalid_password(self):
        """Test crear usuario con contraseña inválida"""
        invalid_user_data = self.base_user_data.copy()
        invalid_user_data["email"] = f"invalid-{random.randint(100000, 999999)}@test.com"
        invalid_user_data["password"] = "weak"
        
        response = self.client.post("/users/", json=invalid_user_data)
        
        assert response.status_code in [400, 422]  # Both are valid for validation errors
        detail = response.json()["detail"]
        # Handle both string and list response formats
        detail_text = detail if isinstance(detail, str) else str(detail)
        assert "password" in detail_text.lower() or "validation" in detail_text.lower()

    def test_get_user_by_id_success(self):
        """Test obtener usuario por ID exitosamente"""
        response = self.client.get(f"/users/{self.user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == self.user_id
        assert data["email"] == self.base_user_data["email"]
        assert data["first_name"] == self.base_user_data["first_name"]

    def test_get_user_by_id_not_found(self):
        """Test obtener usuario con ID inexistente"""
        fake_id = "550e8400-e29b-41d4-a716-446655440000"
        response = self.client.get(f"/users/{fake_id}")
        
        assert response.status_code == 404

    def test_get_user_by_id_invalid_uuid(self):
        """Test obtener usuario con UUID inválido"""
        response = self.client.get("/users/invalid-uuid")
        
        assert response.status_code == 422

    def test_list_users_success(self):
        """Test listar usuarios exitosamente"""
        response = self.client.get("/users/")
        
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert isinstance(data["users"], list)
        assert data["total"] >= 1  # Al menos nuestro usuario de test

    def test_list_users_with_pagination(self):
        """Test listar usuarios con paginación"""
        response = self.client.get("/users/?page=1&page_size=5")
        
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 5
        assert len(data["users"]) <= 5

    def test_list_users_with_filters(self):
        """Test listar usuarios con filtros"""
        response = self.client.get("/users/?role=apprentice&is_active=true")
        
        assert response.status_code == 200
        data = response.json()
        # Verificar que todos los usuarios devueltos cumplan los filtros
        for user in data["users"]:
            assert user["role"] == "apprentice"
            assert user["is_active"] is True

    def test_activate_user_success(self):
        """Test activar usuario exitosamente"""
        # Primero desactivar el usuario
        deactivate_response = self.client.patch(f"/users/{self.user_id}/deactivate")
        assert deactivate_response.status_code == 200
        
        # Ahora activarlo
        response = self.client.patch(f"/users/{self.user_id}/activate")
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is True
        assert data["id"] == self.user_id

    def test_activate_user_not_found(self):
        """Test activar usuario inexistente"""
        fake_id = "550e8400-e29b-41d4-a716-446655440000"
        response = self.client.patch(f"/users/{fake_id}/activate")
        
        assert response.status_code == 404

    def test_deactivate_user_success(self):
        """Test desactivar usuario exitosamente"""
        response = self.client.patch(f"/users/{self.user_id}/deactivate")
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is False
        assert data["id"] == self.user_id

    def test_deactivate_user_not_found(self):
        """Test desactivar usuario inexistente"""
        fake_id = "550e8400-e29b-41d4-a716-446655440000"
        response = self.client.patch(f"/users/{fake_id}/deactivate")
        
        assert response.status_code == 404

    def test_change_password_success(self):
        """Test cambiar contraseña exitosamente"""
        password_data = {
            "current_password": "SecurePass123!",
            "new_password": "NewSecurePass456!"
        }
        
        response = self.client.patch(f"/users/{self.user_id}/change-password", json=password_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "successfully" in data["message"].lower()

    def test_change_password_wrong_current_password(self):
        """Test cambiar contraseña con contraseña actual incorrecta"""
        password_data = {
            "current_password": "WrongPassword123!",
            "new_password": "NewSecurePass456!"
        }
        
        response = self.client.patch(f"/users/{self.user_id}/change-password", json=password_data)
        
        assert response.status_code == 400

    def test_change_password_weak_new_password(self):
        """Test cambiar contraseña con nueva contraseña débil"""
        password_data = {
            "current_password": "SecurePass123!",
            "new_password": "weak"
        }
        
        response = self.client.patch(f"/users/{self.user_id}/change-password", json=password_data)
        
        assert response.status_code in [400, 422]  # Both are valid for validation errors
        # The test passes if we get a validation error response

    def test_change_password_user_not_found(self):
        """Test cambiar contraseña de usuario inexistente"""
        fake_id = "550e8400-e29b-41d4-a716-446655440000"
        password_data = {
            "current_password": "SecurePass123!",
            "new_password": "NewSecurePass456!"
        }
        
        response = self.client.patch(f"/users/{fake_id}/change-password", json=password_data)
        
        assert response.status_code == 400

    def test_user_lifecycle_complete(self):
        """Test del ciclo de vida completo de un usuario"""
        # 1. Crear usuario
        user_data = {
            "email": f"lifecycle-{random.randint(100000, 999999)}@test.com",
            "password": "LifecyclePass123!",
            "first_name": "Lifecycle",
            "last_name": "Test",
            "document_number": f"{random.randint(10000000, 99999999)}",
            "document_type": "TI",
            "role": "administrative"
        }
        
        create_response = self.client.post("/users/", json=user_data)
        assert create_response.status_code == 201
        user = create_response.json()
        user_id = user["id"]
        
        # 2. Obtener usuario
        get_response = self.client.get(f"/users/{user_id}")
        assert get_response.status_code == 200
        assert get_response.json()["email"] == user_data["email"]
        
        # 3. Desactivar usuario
        deactivate_response = self.client.patch(f"/users/{user_id}/deactivate")
        assert deactivate_response.status_code == 200
        assert deactivate_response.json()["is_active"] is False
        
        # 4. Activar usuario
        activate_response = self.client.patch(f"/users/{user_id}/activate")
        assert activate_response.status_code == 200
        assert activate_response.json()["is_active"] is True
        
        # 5. Cambiar contraseña
        password_data = {
            "current_password": "LifecyclePass123!",
            "new_password": "NewLifecyclePass456!"
        }
        password_response = self.client.patch(f"/users/{user_id}/change-password", json=password_data)
        assert password_response.status_code == 200
        
        # 6. Verificar usuario final
        final_get_response = self.client.get(f"/users/{user_id}")
        assert final_get_response.status_code == 200
        final_user = final_get_response.json()
        assert final_user["is_active"] is True
        assert final_user["email"] == user_data["email"]
