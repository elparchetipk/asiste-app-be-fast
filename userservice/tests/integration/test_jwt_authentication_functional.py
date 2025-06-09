"""
Pruebas funcionales completas de autenticación JWT con usuarios reales.
"""

import pytest
from uuid import uuid4
from fastapi.testclient import TestClient

from main import app
from app.domain.value_objects.user_role import UserRole
from tests.utils.test_helpers import AuthTestHelper, TestDataFactory


class TestJWTAuthenticationFunctional:
    """Pruebas funcionales completas de autenticación JWT."""
    
    @pytest.fixture(autouse=True)
    async def setup_test_data(self, test_client, db_tables_ready):
        """Configurar datos de prueba usando la API existente."""
        # Usar el cliente de test del fixture
        self.client = test_client
        
        # Inicializar helper de autenticación
        self.auth_helper = AuthTestHelper(self.client)
        
        # Crear admin usando el seeder
        await self.auth_helper.seed_admin_user()
        
        # Datos de usuarios que intentaremos crear a través de la API
        self.test_users = {
            "admin": TestDataFactory.create_user_data(
                role=UserRole.ADMIN,
                prefix="testadmin"
            ),
            "instructor": TestDataFactory.create_user_data(
                role=UserRole.INSTRUCTOR,
                prefix="testinstr"
            ),
            "apprentice": TestDataFactory.create_user_data(
                role=UserRole.APPRENTICE,
                prefix="testapprent"
            )
        }
                    "last_name": "Test",
                    "email": f"apprentice.{uuid4().hex[:8]}@test.com",
                    "document_number": f"APP{uuid4().hex[:8].upper()}",
                    "document_type": "CC",
                    "password": "ApprenticePass123!",
                    "role": UserRole.APPRENTICE.value
                }
            }
        }

    def get_auth_token(self, email: str, password: str) -> str:
        """Obtener token de autenticación."""
        login_response = self.client.post("/auth/login", json={
            "username": email,
            "password": password
        })
        
        if login_response.status_code == 200:
            return login_response.json()["access_token"]
        else:
            raise Exception(f"Login failed: {login_response.status_code} - {login_response.text}")

    def get_auth_headers(self, token: str) -> dict:
        """Obtener headers de autenticación."""
        return {"Authorization": f"Bearer {token}"}

    def test_admin_can_create_users(self):
        """Verificar que ADMIN puede crear usuarios."""
        admin_token = self.get_auth_token(self.admin_email, self.admin_password)
        headers = self.get_auth_headers(admin_token)
        
        new_user_data = {
            "first_name": "New",
            "last_name": "User",
            "email": f"new.{uuid4().hex[:8]}@test.com",
            "document_number": f"NEW{uuid4().hex[:8].upper()}",
            "document_type": "CC",
            "password": "NewUserPass123!",
            "role": UserRole.APPRENTICE.value
        }
        
        response = self.client.post("/users/", json=new_user_data, headers=headers)
        assert response.status_code == 201
        
        created_user = response.json()
        assert created_user["email"] == new_user_data["email"]
        assert created_user["role"] == new_user_data["role"]

    def test_admin_can_list_users(self):
        """Verificar que ADMIN puede listar usuarios."""
        admin_token = self.get_auth_token(self.admin_email, self.admin_password)
        headers = self.get_auth_headers(admin_token)
        
        response = self.client.get("/users/", headers=headers)
        assert response.status_code == 200
        
        users_data = response.json()
        assert "users" in users_data
        assert "total" in users_data
        assert len(users_data["users"]) >= 3  # Al menos los 3 usuarios creados en setup

    def test_admin_can_get_user_by_id(self):
        """Verificar que ADMIN puede obtener usuarios por ID."""
        admin_token = self.get_auth_token(self.admin_email, self.admin_password)
        headers = self.get_auth_headers(admin_token)
        
        response = self.client.get(f"/users/{self.instructor_user_id}", headers=headers)
        assert response.status_code == 200
        
        user_data = response.json()
        assert user_data["email"] == self.instructor_email

    def test_admin_can_activate_deactivate_users(self):
        """Verificar que ADMIN puede activar/desactivar usuarios."""
        admin_token = self.get_auth_token(self.admin_email, self.admin_password)
        headers = self.get_auth_headers(admin_token)
        
        # Desactivar usuario
        response = self.client.patch(f"/users/{self.apprentice_user_id}/deactivate", headers=headers)
        assert response.status_code == 200
        assert not response.json()["is_active"]
        
        # Activar usuario
        response = self.client.patch(f"/users/{self.apprentice_user_id}/activate", headers=headers)
        assert response.status_code == 200
        assert response.json()["is_active"]

    def test_instructor_can_list_and_view_users(self):
        """Verificar que INSTRUCTOR puede listar y ver usuarios."""
        instructor_token = self.get_auth_token(self.instructor_email, self.instructor_password)
        headers = self.get_auth_headers(instructor_token)
        
        # Listar usuarios
        response = self.client.get("/users/", headers=headers)
        assert response.status_code == 200
        
        # Ver usuario específico
        response = self.client.get(f"/users/{self.apprentice_user_id}", headers=headers)
        assert response.status_code == 200

    def test_instructor_cannot_create_users(self):
        """Verificar que INSTRUCTOR no puede crear usuarios."""
        instructor_token = self.get_auth_token(self.instructor_email, self.instructor_password)
        headers = self.get_auth_headers(instructor_token)
        
        new_user_data = {
            "first_name": "Forbidden",
            "last_name": "User",
            "email": f"forbidden.{uuid4().hex[:8]}@test.com",
            "document_number": f"FOR{uuid4().hex[:8].upper()}",
            "document_type": "CC",
            "password": "ForbiddenPass123!",
            "role": UserRole.APPRENTICE.value
        }
        
        response = self.client.post("/users/", json=new_user_data, headers=headers)
        assert response.status_code == 403

    def test_instructor_cannot_activate_deactivate_users(self):
        """Verificar que INSTRUCTOR no puede activar/desactivar usuarios."""
        instructor_token = self.get_auth_token(self.instructor_email, self.instructor_password)
        headers = self.get_auth_headers(instructor_token)
        
        # Intentar desactivar usuario
        response = self.client.patch(f"/users/{self.apprentice_user_id}/deactivate", headers=headers)
        assert response.status_code == 403
        
        # Intentar activar usuario
        response = self.client.patch(f"/users/{self.apprentice_user_id}/activate", headers=headers)
        assert response.status_code == 403

    def test_apprentice_cannot_access_user_management(self):
        """Verificar que APPRENTICE no puede acceder a gestión de usuarios."""
        apprentice_token = self.get_auth_token(self.apprentice_email, self.apprentice_password)
        headers = self.get_auth_headers(apprentice_token)
        
        # No puede listar usuarios
        response = self.client.get("/users/", headers=headers)
        assert response.status_code == 403
        
        # No puede ver usuarios específicos
        response = self.client.get(f"/users/{self.admin_user_id}", headers=headers)
        assert response.status_code == 403
        
        # No puede crear usuarios
        new_user_data = {
            "first_name": "Forbidden",
            "last_name": "User",
            "email": f"forbidden.{uuid4().hex[:8]}@test.com",
            "document_number": f"FOR{uuid4().hex[:8].upper()}",
            "document_type": "CC",
            "password": "ForbiddenPass123!",
            "role": UserRole.APPRENTICE.value
        }
        
        response = self.client.post("/users/", json=new_user_data, headers=headers)
        assert response.status_code == 403

    def test_users_can_change_own_password(self):
        """Verificar que los usuarios pueden cambiar su propia contraseña."""
        # Apprentice cambiando su propia contraseña
        apprentice_token = self.get_auth_token(self.apprentice_email, self.apprentice_password)
        headers = self.get_auth_headers(apprentice_token)
        
        password_data = {
            "current_password": self.apprentice_password,
            "new_password": "NewApprenticePass123!"
        }
        
        response = self.client.patch(f"/users/{self.apprentice_user_id}/change-password", 
                              json=password_data, headers=headers)
        assert response.status_code == 200
        
        # Verificar que puede hacer login con la nueva contraseña
        new_token = self.get_auth_token(self.apprentice_email, "NewApprenticePass123!")
        assert new_token is not None

    def test_users_cannot_change_others_password(self):
        """Verificar que los usuarios no pueden cambiar contraseñas de otros."""
        apprentice_token = self.get_auth_token(self.apprentice_email, self.apprentice_password)
        headers = self.get_auth_headers(apprentice_token)
        
        password_data = {
            "current_password": "some_password",
            "new_password": "new_password"
        }
        
        # Intentar cambiar contraseña de otro usuario
        response = self.client.patch(f"/users/{self.instructor_user_id}/change-password", 
                              json=password_data, headers=headers)
        assert response.status_code == 403

    def test_admin_can_change_any_password(self):
        """Verificar que ADMIN puede cambiar cualquier contraseña."""
        admin_token = self.get_auth_token(self.admin_email, self.admin_password)
        headers = self.get_auth_headers(admin_token)
        
        password_data = {
            "current_password": self.instructor_password,
            "new_password": "NewInstructorPass123!"
        }
        
        response = self.client.patch(f"/users/{self.instructor_user_id}/change-password", 
                              json=password_data, headers=headers)
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
