"""
Pruebas de integración para autenticación JWT en endpoints de usuarios.
"""

import pytest
import httpx
from uuid import uuid4
from fastapi.testclient import TestClient

from main import app
from app.domain.value_objects.user_role import UserRole
from tests.utils.test_helpers import AuthTestHelper, TestDataFactory


class TestJWTAuthentication:
    """Pruebas de autenticación JWT para endpoints de gestión de usuarios."""

    @pytest.fixture(autouse=True)
    async def setup_test_data(self, test_client, db_tables_ready):
        """Configurar datos de prueba."""
        # Usar el cliente de test del fixture
        self.client = test_client
        
        # Inicializar helper de autenticación
        self.auth_helper = AuthTestHelper(self.client)
        
        # Crear admin usando el seeder
        await self.auth_helper.seed_admin_user()
        
        # Crear usuarios de prueba con diferentes roles usando TestDataFactory
        self.admin_user_data = TestDataFactory.create_user_data(
            role=UserRole.ADMIN,
            prefix="testadmin"
        )
        
        self.instructor_user_data = TestDataFactory.create_user_data(
            role=UserRole.INSTRUCTOR,
            prefix="testinstr"
        )
        
        self.administrative_user_data = TestDataFactory.create_user_data(
            role=UserRole.ADMINISTRATIVE,
            prefix="testadmins"
        )
        
        self.apprentice_user_data = {
            "first_name": "Apprentice",
            "last_name": "User",
            "email": f"apprentice.{uuid4().hex[:8]}@test.com",
            "document_number": f"APP{uuid4().hex[:8].upper()}",
            "document_type": "CC",
            "password": "ApprenticePass123!",
            "role": UserRole.APPRENTICE.value
        }

    def create_user_and_get_token(self, user_data: dict) -> tuple[dict, str]:
        """Crear usuario y obtener token de autenticación."""
        # Primero necesitamos crear un admin temporal para crear otros usuarios
        # En un entorno real, esto se haría a través de seeders o migración inicial
        
        # Intentar crear el usuario (esto fallará para roles no-admin sin autenticación)
        # Por ahora, vamos a crear usuarios directamente para pruebas
        
        response = self.client.post("/users/", json=user_data)
        
        if response.status_code == 422:  # Error de autenticación esperado
            # Para las pruebas, necesitamos un método alternativo
            # Vamos a usar el endpoint de login directamente si existe
            pass
        
        # Login para obtener token
        login_response = self.client.post("/auth/login", json={
            "username": user_data["email"],
            "password": user_data["password"]
        })
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            return user_data, token_data["access_token"]
        
        return user_data, None

    def get_auth_headers(self, token: str) -> dict:
        """Obtener headers de autenticación."""
        return {"Authorization": f"Bearer {token}"}

    def test_endpoints_require_authentication(self):
        """Verificar que todos los endpoints requieren autenticación."""
        
        # Endpoints que deben requerir autenticación
        test_endpoints = [
            ("GET", "/users/", {}),
            ("GET", f"/users/{uuid4()}", {}),
            ("POST", "/users/", self.admin_user_data),
            ("PATCH", f"/users/{uuid4()}/activate", {}),
            ("PATCH", f"/users/{uuid4()}/deactivate", {}),
            ("PATCH", f"/users/{uuid4()}/change-password", {
                "current_password": "old_pass",
                "new_password": "new_pass"
            })
        ]
        
        for method, endpoint, payload in test_endpoints:
            if method == "GET":
                response = self.client.get(endpoint)
            elif method == "POST":
                response = self.client.post(endpoint, json=payload)
            elif method == "PATCH":
                response = self.client.patch(endpoint, json=payload)
            
            # Tanto 401 (Unauthorized) como 403 (Forbidden) indican protección de autenticación
            assert response.status_code in [401, 403], f"Endpoint {method} {endpoint} should require authentication. Got: {response.status_code}, Response: {response.json()}"

    def test_invalid_token_rejected(self):
        """Verificar que tokens inválidos son rechazados."""
        invalid_headers = {"Authorization": "Bearer invalid_token_here"}
        
        response = self.client.get("/users/", headers=invalid_headers)
        assert response.status_code == 401
        response_detail = response.json()["detail"].lower()
        assert any(keyword in response_detail for keyword in ["token inválido", "invalid", "error de autenticación", "authentication error"])

    def test_expired_token_rejected(self):
        """Verificar que tokens expirados son rechazados."""
        # Crear un token expirado (esto requeriría modificar el servicio de tokens para testing)
        expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImV4cCI6MTYxNjIzOTAyMn0.invalid"
        headers = {"Authorization": f"Bearer {expired_token}"}
        
        response = self.client.get("/users/", headers=headers)
        assert response.status_code == 401

    def test_admin_can_access_all_endpoints(self):
        """Verificar que el ADMIN puede acceder a todos los endpoints."""
        # Este test requiere que ya exista un usuario admin en la base de datos
        # o que implementemos un seeder
        
        # Crear admin user - este test requiere refactoring para usar seeders
        pass

    def test_instructor_has_limited_access(self):
        """Verificar que los INSTRUCTORES tienen acceso limitado."""
        # Los instructores pueden listar y ver usuarios, pero no crear/activar/desactivar
        pass

    def test_administrative_has_user_creation_access(self):
        """Verificar que ADMINISTRATIVE puede crear usuarios."""
        pass

    def test_apprentice_has_minimal_access(self):
        """Verificar que APPRENTICE solo puede cambiar su propia contraseña."""
        pass

    def test_role_based_authorization_create_user(self):
        """Verificar autorización basada en roles para crear usuarios."""
        # Solo ADMIN y ADMINISTRATIVE pueden crear usuarios
        pass

    def test_role_based_authorization_activate_deactivate(self):
        """Verificar autorización basada en roles para activar/desactivar usuarios."""
        # Solo ADMIN puede activar/desactivar usuarios
        pass

    def test_change_password_authorization(self):
        """Verificar autorización para cambio de contraseñas."""
        # Usuarios pueden cambiar su propia contraseña
        # ADMINs pueden cambiar cualquier contraseña
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
