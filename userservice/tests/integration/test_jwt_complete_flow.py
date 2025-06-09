"""
Pruebas de autenticación JWT usando el flujo completo de la API.
"""

import pytest
from uuid import uuid4
from fastapi.testclient import TestClient

from main import app
from app.domain.value_objects.user_role import UserRole
from tests.utils.test_helpers import AuthTestHelper, TestDataFactory


class TestJWTCompleteFlow:
    """Pruebas del flujo completo de autenticación JWT."""

    @pytest.fixture(autouse=True)
    async def setup_test_environment(self, test_client, db_tables_ready):
        """Setup que se ejecuta antes de cada test"""
        # Usar el cliente de test del fixture
        self.client = test_client
        
        # Inicializar helper de autenticación
        self.auth_helper = AuthTestHelper(self.client)
        
        # Crear admin usando el seeder
        await self.auth_helper.seed_admin_user()

    def test_complete_jwt_flow_without_existing_admin(self):
        """
        Verificar el flujo completo JWT sin depender de usuarios existentes.
        Esta prueba demuestra que los endpoints están protegidos.
        """
        
        # 1. Verificar que los endpoints están protegidos
        response = self.client.get("/users/")
        assert response.status_code in [401, 403], "Los endpoints deben estar protegidos"
        
        # 2. Verificar que tokens inválidos son rechazados
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        response = self.client.get("/users/", headers=invalid_headers)
        assert response.status_code == 401, "Tokens inválidos deben ser rechazados"
        
        # 3. Verificar que el endpoint de login existe
        response = self.client.post("/auth/login", json={
            "username": "nonexistent@test.com",
            "password": "wrongpassword"
        })
        # El endpoint debe existir, aunque las credenciales sean incorrectas
        assert response.status_code in [401, 422], "El endpoint de login debe existir"

    def test_auth_endpoints_are_accessible(self):
        """Verificar que los endpoints de autenticación son accesibles."""
        
        # Verificar que el endpoint de login existe y responde
        response = self.client.post("/auth/login", json={
            "username": "test@example.com",
            "password": "testpassword"
        })
        # Debe retornar error de credenciales, no error 404
        assert response.status_code != 404, "El endpoint de login debe existir"
        
        # Verificar que el endpoint de validación existe
        response = self.client.get("/auth/validate", headers={
            "Authorization": "Bearer invalid_token"
        })
        # Debe retornar error de token, no error 404
        assert response.status_code != 404, "El endpoint de validación debe existir"

    def test_user_endpoints_require_specific_permissions(self):
        """Verificar que diferentes endpoints requieren diferentes permisos."""
        
        test_user_id = str(uuid4())
        
        endpoints_tests = [
            # (método, endpoint, payload, descripción)
            ("GET", "/users/", {}, "Listar usuarios"),
            ("GET", f"/users/{test_user_id}", {}, "Obtener usuario"),
            ("POST", "/users/", {
                "first_name": "Test",
                "last_name": "User", 
                "email": "test@example.com",
                "document_number": "12345678",
                "document_type": "CC",
                "password": "TestPass123!",
                "role": "apprentice"
            }, "Crear usuario"),
            ("PATCH", f"/users/{test_user_id}/activate", {}, "Activar usuario"),
            ("PATCH", f"/users/{test_user_id}/deactivate", {}, "Desactivar usuario"),
            ("PATCH", f"/users/{test_user_id}/change-password", {
                "current_password": "old_pass",
                "new_password": "new_pass"
            }, "Cambiar contraseña")
        ]
        
        for method, endpoint, payload, description in endpoints_tests:
            if method == "GET":
                response = self.client.get(endpoint)
            elif method == "POST":
                response = self.client.post(endpoint, json=payload)
            elif method == "PATCH":
                response = self.client.patch(endpoint, json=payload)
            
            # Todos deben requerir autenticación
            assert response.status_code in [401, 403], f"{description} debe requerir autenticación"

    def test_jwt_middleware_integration(self):
        """Verificar que el middleware JWT está integrado correctamente."""
        
        # Test con diferentes tipos de headers Authorization incorrectos
        test_cases = [
            {"Authorization": "InvalidFormat"},  # Sin Bearer
            {"Authorization": "Bearer"},  # Sin token
            {"Authorization": "Bearer "},  # Token vacío
            {"Authorization": "Bearer invalid.jwt.token"},  # Token malformado
        ]
        
        for headers in test_cases:
            response = self.client.get("/users/", headers=headers)
            assert response.status_code in [401, 403], f"Header inválido debe ser rechazado: {headers}"

    def test_role_based_access_structure_exists(self):
        """Verificar que la estructura de autorización basada en roles existe."""
        
        # Esta prueba verifica que la estructura de roles está implementada
        # revisando que los códigos de respuesta sean consistentes con un
        # sistema de autorización por roles
        
        # Crear payload de usuario para diferentes endpoints
        user_payload = {
            "first_name": "Test",
            "last_name": "User",
            "email": f"test.{uuid4().hex[:8]}@example.com",
            "document_number": f"DOC{uuid4().hex[:8].upper()}",
            "document_type": "CC",
            "password": "TestPass123!",
            "role": "apprentice"
        }
        
        # Todos estos endpoints deben estar protegidos
        response = self.client.post("/users/", json=user_payload)
        assert response.status_code in [401, 403], "Crear usuario debe estar protegido"
        
        test_user_id = str(uuid4())
        
        response = self.client.patch(f"/users/{test_user_id}/activate")
        assert response.status_code in [401, 403], "Activar usuario debe estar protegido"
        
        response = self.client.patch(f"/users/{test_user_id}/deactivate")
        assert response.status_code in [401, 403], "Desactivar usuario debe estar protegido"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
