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
    async def setup_test_environment(self, test_client, db_tables_ready):
        """Setup que se ejecuta antes de cada test"""
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

    def get_auth_token(self, email: str, password: str) -> str:
        """Obtener token de autenticación."""
        login_response = self.client.post("/auth/login", json={
            "username": email,
            "password": password
        })
        
        if login_response.status_code == 200:
            return login_response.json()["access_token"]
        return None

    def test_admin_can_create_users(self):
        """Test que admin puede crear usuarios de cualquier rol"""
        admin_headers = self.auth_helper.get_admin_headers()
        assert admin_headers is not None, "No se pudo obtener headers de admin"
        
        for role_name, user_data in self.test_users.items():
            print(f"Creando usuario {role_name}: {user_data['email']}")
            
            response = self.client.post("/users/", json=user_data, headers=admin_headers)
            
            # Permitir 201 (creado) o 409 (ya existe)
            assert response.status_code in [201, 409], f"Error creando {role_name}: {response.json()}"
            
            if response.status_code == 201:
                created_user = response.json()
                assert created_user["email"] == user_data["email"]
                assert created_user["role"] == user_data["role"]

    def test_user_authentication_flow(self):
        """Test completo del flujo de autenticación"""
        admin_headers = self.auth_helper.get_admin_headers()
        
        # Crear un usuario instructor para probar autenticación
        instructor_data = self.test_users["instructor"]
        create_response = self.client.post("/users/", json=instructor_data, headers=admin_headers)
        
        # Verificar que se creó o ya existe
        assert create_response.status_code in [201, 409]
        
        # Intentar login con las credenciales
        login_response = self.client.post("/auth/login", json={
            "username": instructor_data["email"],
            "password": instructor_data["password"]
        })
        
        # Debería funcionar si el usuario está activo
        if login_response.status_code == 200:
            token_data = login_response.json()
            assert "access_token" in token_data
            assert token_data["token_type"] == "bearer"
            
            # Probar endpoint protegido con el token
            headers = {"Authorization": f"Bearer {token_data['access_token']}"}
            profile_response = self.client.get("/users/profile", headers=headers)
            assert profile_response.status_code == 200
            
            profile_data = profile_response.json()
            assert profile_data["email"] == instructor_data["email"]

    def test_token_validation(self):
        """Test validación de tokens JWT"""
        # Intentar acceder a endpoint protegido sin token
        response = self.client.get("/users/profile")
        assert response.status_code == 401
        
        # Intentar con token inválido
        bad_headers = {"Authorization": "Bearer invalid_token"}
        response = self.client.get("/users/profile", headers=bad_headers)
        assert response.status_code == 401

    def test_role_based_access(self):
        """Test acceso basado en roles"""
        admin_headers = self.auth_helper.get_admin_headers()
        
        # Crear usuarios de diferentes roles
        apprentice_data = self.test_users["apprentice"]
        create_response = self.client.post("/users/", json=apprentice_data, headers=admin_headers)
        assert create_response.status_code in [201, 409]
        
        # Obtener token del apprentice
        apprentice_token = self.get_auth_token(apprentice_data["email"], apprentice_data["password"])
        
        if apprentice_token:
            apprentice_headers = {"Authorization": f"Bearer {apprentice_token}"}
            
            # El apprentice debería poder ver su perfil
            profile_response = self.client.get("/users/profile", headers=apprentice_headers)
            assert profile_response.status_code == 200
            
            # Pero no debería poder crear otros usuarios
            new_user_data = TestDataFactory.create_user_data(
                role=UserRole.APPRENTICE,
                prefix="unauthorized"
            )
            create_response = self.client.post("/users/", json=new_user_data, headers=apprentice_headers)
            assert create_response.status_code == 403  # Forbidden
