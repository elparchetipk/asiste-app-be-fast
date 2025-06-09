"""
Pruebas comprehensivas para todos los endpoints de usuarios con autenticación JWT.
Incluye casos positivos y negativos para validar el comportamiento completo.
"""

import pytest
import asyncio
import random
from fastapi.testclient import TestClient

from main import app
from tests.utils.test_helpers import AuthTestHelper, TestDataFactory
from app.domain.value_objects.user_role import UserRole


class TestUserEndpointsWithAuth:
    """Suite de tests para todos los endpoints de usuarios con autenticación JWT"""

    @pytest.fixture(autouse=True)
    async def setup_test_environment(self, test_client, db_tables_ready):
        """Setup que se ejecuta antes de cada test"""
        # Usar el cliente de test del fixture
        self.client = test_client
        
        # Inicializar helper de autenticación
        self.auth_helper = AuthTestHelper(self.client)
        
        # Crear admin usando el seeder antes de seed_database
        await self.auth_helper.seed_admin_user()
        
        # Sembrar la base de datos con usuarios de test
        self.seeded_users = self.auth_helper.seed_database()
        
        # Verificar que tenemos admin disponible
        if not self.auth_helper.get_admin_headers():
            pytest.fail("No se pudo crear usuario admin para tests")
        
        # Crear un usuario base para tests usando admin
        self.base_user_data = TestDataFactory.create_user_data(
            role=UserRole.APPRENTICE,
            prefix="testbase"
        )
        
        admin_headers = self.auth_helper.get_admin_headers()
        response = self.client.post("/users/", json=self.base_user_data, headers=admin_headers)
        
        if response.status_code == 201:
            self.created_user = response.json()
            self.user_id = self.created_user["id"]
            
            # Obtener token del usuario creado
            self.base_user_token = self.auth_helper.get_auth_token(
                self.base_user_data["email"],
                self.base_user_data["password"]
            )
        else:
            pytest.fail(f"Failed to create base user: {response.text}")

    def test_create_user_success_as_admin(self):
        """Test crear usuario exitosamente como ADMIN"""
        user_data = TestDataFactory.create_user_data(
            role=UserRole.INSTRUCTOR,
            prefix="newuser"
        )
        
        admin_headers = self.auth_helper.get_admin_headers()
        response = self.client.post("/users/", json=user_data, headers=admin_headers)
        
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

    def test_create_user_success_as_administrative(self):
        """Test crear usuario exitosamente como ADMINISTRATIVE"""
        user_data = TestDataFactory.create_user_data(
            role=UserRole.APPRENTICE,
            prefix="adminuser"
        )
        
        admin_headers = self.auth_helper.get_administrative_headers()
        response = self.client.post("/users/", json=user_data, headers=admin_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["role"] == user_data["role"]

    def test_create_user_forbidden_as_instructor(self):
        """Test crear usuario prohibido como INSTRUCTOR"""
        user_data = TestDataFactory.create_user_data(
            role=UserRole.APPRENTICE,
            prefix="forbidden"
        )
        
        instructor_headers = self.auth_helper.get_instructor_headers()
        response = self.client.post("/users/", json=user_data, headers=instructor_headers)
        
        assert response.status_code == 403

    def test_create_user_forbidden_as_apprentice(self):
        """Test crear usuario prohibido como APPRENTICE"""
        user_data = TestDataFactory.create_user_data(
            role=UserRole.APPRENTICE,
            prefix="forbidden"
        )
        
        apprentice_headers = self.auth_helper.get_apprentice_headers()
        response = self.client.post("/users/", json=user_data, headers=apprentice_headers)
        
        assert response.status_code == 403

    def test_create_user_unauthorized_without_token(self):
        """Test crear usuario sin autenticación"""
        user_data = TestDataFactory.create_user_data()
        
        response = self.client.post("/users/", json=user_data)
        
        assert response.status_code == 401

    def test_create_user_duplicate_email(self):
        """Test crear usuario con email duplicado"""
        admin_headers = self.auth_helper.get_admin_headers()
        response = self.client.post("/users/", json=self.base_user_data, headers=admin_headers)
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    def test_create_user_invalid_password(self):
        """Test crear usuario con contraseña inválida"""
        invalid_user_data = TestDataFactory.create_user_data()
        invalid_user_data["password"] = "weak"
        
        admin_headers = self.auth_helper.get_admin_headers()
        response = self.client.post("/users/", json=invalid_user_data, headers=admin_headers)
        
        assert response.status_code in [400, 422]
        detail = response.json()["detail"]
        detail_text = detail if isinstance(detail, str) else str(detail)
        assert "password" in detail_text.lower() or "validation" in detail_text.lower()

    def test_get_user_by_id_success_as_admin(self):
        """Test obtener usuario por ID exitosamente como ADMIN"""
        admin_headers = self.auth_helper.get_admin_headers()
        response = self.client.get(f"/users/{self.user_id}", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == self.user_id
        assert data["email"] == self.base_user_data["email"]
        assert data["first_name"] == self.base_user_data["first_name"]

    def test_get_user_by_id_success_as_instructor(self):
        """Test obtener usuario por ID exitosamente como INSTRUCTOR"""
        instructor_headers = self.auth_helper.get_instructor_headers()
        response = self.client.get(f"/users/{self.user_id}", headers=instructor_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == self.user_id

    def test_get_user_by_id_forbidden_as_apprentice(self):
        """Test obtener usuario por ID prohibido como APPRENTICE"""
        apprentice_headers = self.auth_helper.get_apprentice_headers()
        response = self.client.get(f"/users/{self.user_id}", headers=apprentice_headers)
        
        assert response.status_code == 403

    def test_get_user_by_id_not_found(self):
        """Test obtener usuario con ID inexistente"""
        fake_id = "550e8400-e29b-41d4-a716-446655440000"
        admin_headers = self.auth_helper.get_admin_headers()
        response = self.client.get(f"/users/{fake_id}", headers=admin_headers)
        
        assert response.status_code == 404

    def test_get_user_by_id_unauthorized(self):
        """Test obtener usuario sin autenticación"""
        response = self.client.get(f"/users/{self.user_id}")
        
        assert response.status_code == 401

    def test_list_users_success_as_admin(self):
        """Test listar usuarios exitosamente como ADMIN"""
        admin_headers = self.auth_helper.get_admin_headers()
        response = self.client.get("/users/", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert isinstance(data["users"], list)
        assert data["total"] >= 1

    def test_list_users_success_as_instructor(self):
        """Test listar usuarios exitosamente como INSTRUCTOR"""
        instructor_headers = self.auth_helper.get_instructor_headers()
        response = self.client.get("/users/", headers=instructor_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "users" in data

    def test_list_users_forbidden_as_apprentice(self):
        """Test listar usuarios prohibido como APPRENTICE"""
        apprentice_headers = self.auth_helper.get_apprentice_headers()
        response = self.client.get("/users/", headers=apprentice_headers)
        
        assert response.status_code == 403

    def test_list_users_with_pagination(self):
        """Test listar usuarios con paginación"""
        admin_headers = self.auth_helper.get_admin_headers()
        response = self.client.get("/users/?page=1&page_size=5", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 5
        assert len(data["users"]) <= 5

    def test_list_users_with_filters(self):
        """Test listar usuarios con filtros"""
        admin_headers = self.auth_helper.get_admin_headers()
        response = self.client.get("/users/?role=apprentice&is_active=true", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        for user in data["users"]:
            assert user["role"] == "apprentice"
            assert user["is_active"] is True

    def test_activate_user_success_as_admin(self):
        """Test activar usuario exitosamente como ADMIN"""
        admin_headers = self.auth_helper.get_admin_headers()
        
        # Primero desactivar el usuario
        deactivate_response = self.client.patch(f"/users/{self.user_id}/deactivate", headers=admin_headers)
        assert deactivate_response.status_code == 200
        
        # Ahora activarlo
        response = self.client.patch(f"/users/{self.user_id}/activate", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is True
        assert data["id"] == self.user_id

    def test_activate_user_forbidden_as_instructor(self):
        """Test activar usuario prohibido como INSTRUCTOR"""
        instructor_headers = self.auth_helper.get_instructor_headers()
        response = self.client.patch(f"/users/{self.user_id}/activate", headers=instructor_headers)
        
        assert response.status_code == 403

    def test_deactivate_user_success_as_admin(self):
        """Test desactivar usuario exitosamente como ADMIN"""
        admin_headers = self.auth_helper.get_admin_headers()
        response = self.client.patch(f"/users/{self.user_id}/deactivate", headers=admin_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is False
        assert data["id"] == self.user_id

    def test_deactivate_user_forbidden_as_instructor(self):
        """Test desactivar usuario prohibido como INSTRUCTOR"""
        instructor_headers = self.auth_helper.get_instructor_headers()
        response = self.client.patch(f"/users/{self.user_id}/deactivate", headers=instructor_headers)
        
        assert response.status_code == 403

    def test_change_password_success_own_user(self):
        """Test cambiar contraseña exitosamente del propio usuario"""
        password_data = TestDataFactory.create_password_change_data(
            current_password=self.base_user_data["password"],
            new_password="NewSecurePass456!"
        )
        
        # Usar token del usuario base (apprentice)
        base_user_headers = self.auth_helper.get_auth_headers(self.base_user_token)
        response = self.client.patch(f"/users/{self.user_id}/change-password", 
                              json=password_data, headers=base_user_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "successfully" in data["message"].lower()

    def test_change_password_success_as_admin(self):
        """Test cambiar contraseña exitosamente como ADMIN"""
        password_data = TestDataFactory.create_password_change_data(
            current_password=self.base_user_data["password"],
            new_password="ChiefChangedSecure123!"  # Evitar "admin" y "pass"
        )
        
        admin_headers = self.auth_helper.get_admin_headers()
        response = self.client.patch(f"/users/{self.user_id}/change-password", 
                              json=password_data, headers=admin_headers)
        
        assert response.status_code == 200

    def test_change_password_forbidden_other_user(self):
        """Test cambiar contraseña prohibido de otro usuario"""
        # Crear otro usuario para el test
        admin_headers = self.auth_helper.get_admin_headers()
        other_user_data = TestDataFactory.create_user_data(prefix="other")
        other_response = self.client.post("/users/", json=other_user_data, headers=admin_headers)
        other_user_id = other_response.json()["id"]
        
        password_data = TestDataFactory.create_password_change_data()
        
        # Intentar cambiar contraseña de otro usuario como apprentice
        base_user_headers = self.auth_helper.get_auth_headers(self.base_user_token)
        response = self.client.patch(f"/users/{other_user_id}/change-password", 
                              json=password_data, headers=base_user_headers)
        
        assert response.status_code == 403

    def test_change_password_wrong_current_password(self):
        """Test cambiar contraseña con contraseña actual incorrecta"""
        password_data = TestDataFactory.create_password_change_data(
            current_password="WrongPassword123!",
            new_password="NewSecurePass456!"
        )
        
        base_user_headers = self.auth_helper.get_auth_headers(self.base_user_token)
        response = self.client.patch(f"/users/{self.user_id}/change-password", 
                              json=password_data, headers=base_user_headers)
        
        assert response.status_code == 400

    def test_change_password_weak_new_password(self):
        """Test cambiar contraseña con nueva contraseña débil"""
        password_data = TestDataFactory.create_password_change_data(
            current_password=self.base_user_data["password"],
            new_password="weak"
        )
        
        base_user_headers = self.auth_helper.get_auth_headers(self.base_user_token)
        response = self.client.patch(f"/users/{self.user_id}/change-password", 
                              json=password_data, headers=base_user_headers)
        
        assert response.status_code in [400, 422]

    def test_user_lifecycle_complete_with_auth(self):
        """Test del ciclo de vida completo de un usuario con autenticación"""
        admin_headers = self.auth_helper.get_admin_headers()
        
        # 1. Crear usuario
        user_data = TestDataFactory.create_user_data(
            role=UserRole.ADMINISTRATIVE,
            prefix="lifecycle"
        )
        
        create_response = self.client.post("/users/", json=user_data, headers=admin_headers)
        assert create_response.status_code == 201
        user = create_response.json()
        user_id = user["id"]
        
        # 2. Obtener usuario
        get_response = self.client.get(f"/users/{user_id}", headers=admin_headers)
        assert get_response.status_code == 200
        assert get_response.json()["email"] == user_data["email"]
        
        # 3. Desactivar usuario
        deactivate_response = self.client.patch(f"/users/{user_id}/deactivate", headers=admin_headers)
        assert deactivate_response.status_code == 200
        assert deactivate_response.json()["is_active"] is False
        
        # 4. Activar usuario
        activate_response = self.client.patch(f"/users/{user_id}/activate", headers=admin_headers)
        assert activate_response.status_code == 200
        assert activate_response.json()["is_active"] is True
        
        # 5. Cambiar contraseña como admin
        password_data = TestDataFactory.create_password_change_data(
            current_password=user_data["password"],
            new_password="NewLifecyclePass456!"
        )
        password_response = self.client.patch(f"/users/{user_id}/change-password", 
                                       json=password_data, headers=admin_headers)
        assert password_response.status_code == 200
        
        # 6. Verificar usuario final
        final_get_response = self.client.get(f"/users/{user_id}", headers=admin_headers)
        assert final_get_response.status_code == 200
        final_user = final_get_response.json()
        assert final_user["is_active"] is True
        assert final_user["email"] == user_data["email"]

    def test_unauthorized_access_all_endpoints(self):
        """Test que todos los endpoints requieren autenticación"""
        test_user_id = self.user_id
        
        # Endpoints que deben requerir autenticación
        endpoints = [
            ("GET", "/users/"),
            ("GET", f"/users/{test_user_id}"),
            ("POST", "/users/", TestDataFactory.create_user_data()),
            ("PATCH", f"/users/{test_user_id}/activate"),
            ("PATCH", f"/users/{test_user_id}/deactivate"),
            ("PATCH", f"/users/{test_user_id}/change-password", 
             TestDataFactory.create_password_change_data())
        ]
        
        for method, endpoint, *payload in endpoints:
            json_data = payload[0] if payload else {}
            
            if method == "GET":
                response = self.client.get(endpoint)
            elif method == "POST":
                response = self.client.post(endpoint, json=json_data)
            elif method == "PATCH":
                response = self.client.patch(endpoint, json=json_data)
            
            assert response.status_code == 401, f"Endpoint {method} {endpoint} debe requerir autenticación"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
