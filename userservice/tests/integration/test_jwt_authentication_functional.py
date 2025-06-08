"""
Pruebas funcionales completas de autenticación JWT con usuarios reales.
"""

import pytest
import asyncio
from uuid import uuid4
from fastapi.testclient import TestClient

from main import app
from app.domain.value_objects.user_role import UserRole
from app.infrastructure.config.database import get_db_session
from app.domain.entities.user_entity import User
from app.infrastructure.adapters.password_service import PasswordService
from app.infrastructure.adapters.sqlalchemy_user_repository import SQLAlchemyUserRepository


client = TestClient(app)


class TestJWTAuthenticationFunctional:
    """Pruebas funcionales completas de autenticación JWT."""

    @pytest.fixture(autouse=True)
    async def setup_test_users(self):
        """Configurar usuarios de prueba directamente en la base de datos."""
        async for session in get_db_session():
            try:
                # Crear instancias de servicios
                password_service = PasswordService()
                user_repository = SQLAlchemyUserRepository(session)
                
                # Crear usuario ADMIN de prueba
                self.admin_email = f"admin.{uuid4().hex[:8]}@test.com"
                self.admin_password = "AdminPass123!"
                
                admin_user = User(
                    first_name="Admin",
                    last_name="Test",
                    email=self.admin_email,
                    document_number=f"ADM{uuid4().hex[:8].upper()}",
                    document_type="CC",
                    password_hash=password_service.hash_password(self.admin_password),
                    role=UserRole.ADMIN,
                    is_active=True
                )
                
                await user_repository.create(admin_user)
                self.admin_user_id = admin_user.id
                
                # Crear usuario INSTRUCTOR de prueba
                self.instructor_email = f"instructor.{uuid4().hex[:8]}@test.com"
                self.instructor_password = "InstructorPass123!"
                
                instructor_user = User(
                    first_name="Instructor",
                    last_name="Test",
                    email=self.instructor_email,
                    document_number=f"INS{uuid4().hex[:8].upper()}",
                    document_type="CC",
                    password_hash=password_service.hash_password(self.instructor_password),
                    role=UserRole.INSTRUCTOR,
                    is_active=True
                )
                
                await user_repository.create(instructor_user)
                self.instructor_user_id = instructor_user.id
                
                # Crear usuario APPRENTICE de prueba
                self.apprentice_email = f"apprentice.{uuid4().hex[:8]}@test.com"
                self.apprentice_password = "ApprenticePass123!"
                
                apprentice_user = User(
                    first_name="Apprentice",
                    last_name="Test",
                    email=self.apprentice_email,
                    document_number=f"APP{uuid4().hex[:8].upper()}",
                    document_type="CC",
                    password_hash=password_service.hash_password(self.apprentice_password),
                    role=UserRole.APPRENTICE,
                    is_active=True
                )
                
                await user_repository.create(apprentice_user)
                self.apprentice_user_id = apprentice_user.id
                
                break
            except Exception as e:
                await session.rollback()
                raise e

    def get_auth_token(self, email: str, password: str) -> str:
        """Obtener token de autenticación."""
        login_response = client.post("/auth/login", json={
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
        
        response = client.post("/users/", json=new_user_data, headers=headers)
        assert response.status_code == 201
        
        created_user = response.json()
        assert created_user["email"] == new_user_data["email"]
        assert created_user["role"] == new_user_data["role"]

    def test_admin_can_list_users(self):
        """Verificar que ADMIN puede listar usuarios."""
        admin_token = self.get_auth_token(self.admin_email, self.admin_password)
        headers = self.get_auth_headers(admin_token)
        
        response = client.get("/users/", headers=headers)
        assert response.status_code == 200
        
        users_data = response.json()
        assert "users" in users_data
        assert "total" in users_data
        assert len(users_data["users"]) >= 3  # Al menos los 3 usuarios creados en setup

    def test_admin_can_get_user_by_id(self):
        """Verificar que ADMIN puede obtener usuarios por ID."""
        admin_token = self.get_auth_token(self.admin_email, self.admin_password)
        headers = self.get_auth_headers(admin_token)
        
        response = client.get(f"/users/{self.instructor_user_id}", headers=headers)
        assert response.status_code == 200
        
        user_data = response.json()
        assert user_data["email"] == self.instructor_email

    def test_admin_can_activate_deactivate_users(self):
        """Verificar que ADMIN puede activar/desactivar usuarios."""
        admin_token = self.get_auth_token(self.admin_email, self.admin_password)
        headers = self.get_auth_headers(admin_token)
        
        # Desactivar usuario
        response = client.patch(f"/users/{self.apprentice_user_id}/deactivate", headers=headers)
        assert response.status_code == 200
        assert not response.json()["is_active"]
        
        # Activar usuario
        response = client.patch(f"/users/{self.apprentice_user_id}/activate", headers=headers)
        assert response.status_code == 200
        assert response.json()["is_active"]

    def test_instructor_can_list_and_view_users(self):
        """Verificar que INSTRUCTOR puede listar y ver usuarios."""
        instructor_token = self.get_auth_token(self.instructor_email, self.instructor_password)
        headers = self.get_auth_headers(instructor_token)
        
        # Listar usuarios
        response = client.get("/users/", headers=headers)
        assert response.status_code == 200
        
        # Ver usuario específico
        response = client.get(f"/users/{self.apprentice_user_id}", headers=headers)
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
        
        response = client.post("/users/", json=new_user_data, headers=headers)
        assert response.status_code == 403

    def test_instructor_cannot_activate_deactivate_users(self):
        """Verificar que INSTRUCTOR no puede activar/desactivar usuarios."""
        instructor_token = self.get_auth_token(self.instructor_email, self.instructor_password)
        headers = self.get_auth_headers(instructor_token)
        
        # Intentar desactivar usuario
        response = client.patch(f"/users/{self.apprentice_user_id}/deactivate", headers=headers)
        assert response.status_code == 403
        
        # Intentar activar usuario
        response = client.patch(f"/users/{self.apprentice_user_id}/activate", headers=headers)
        assert response.status_code == 403

    def test_apprentice_cannot_access_user_management(self):
        """Verificar que APPRENTICE no puede acceder a gestión de usuarios."""
        apprentice_token = self.get_auth_token(self.apprentice_email, self.apprentice_password)
        headers = self.get_auth_headers(apprentice_token)
        
        # No puede listar usuarios
        response = client.get("/users/", headers=headers)
        assert response.status_code == 403
        
        # No puede ver usuarios específicos
        response = client.get(f"/users/{self.admin_user_id}", headers=headers)
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
        
        response = client.post("/users/", json=new_user_data, headers=headers)
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
        
        response = client.patch(f"/users/{self.apprentice_user_id}/change-password", 
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
        response = client.patch(f"/users/{self.instructor_user_id}/change-password", 
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
        
        response = client.patch(f"/users/{self.instructor_user_id}/change-password", 
                              json=password_data, headers=headers)
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
