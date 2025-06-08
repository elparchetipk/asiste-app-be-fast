"""
Test helpers y utilidades para testing con autenticación JWT.
"""

import uuid
import random
from typing import Dict, Optional, Tuple
from fastapi.testclient import TestClient

from app.domain.value_objects.user_role import UserRole


class AuthTestHelper:
    """Helper para manejo de autenticación en tests."""

    def __init__(self, client: TestClient):
        self.client = client
        self._seed_users: Dict[str, Dict] = {}
        self._user_tokens: Dict[str, str] = {}

    def create_seed_users(self) -> Dict[str, Dict]:
        """Crear usuarios de seed para testing."""
        seed_users = {
            "admin": {
                "email": f"admin.seed.{uuid.uuid4().hex[:8]}@test.com",
                "password": "AdminSeedPass123!",
                "data": {
                    "first_name": "Admin",
                    "last_name": "Seed", 
                    "email": f"admin.seed.{uuid.uuid4().hex[:8]}@test.com",
                    "document_number": f"ADMSEED{random.randint(10000, 99999)}",
                    "document_type": "CC",
                    "password": "AdminSeedPass123!",
                    "role": UserRole.ADMIN.value
                }
            },
            "administrative": {
                "email": f"admin.staff.{uuid.uuid4().hex[:8]}@test.com",
                "password": "AdminStaffPass123!",
                "data": {
                    "first_name": "Administrative",
                    "last_name": "Staff",
                    "email": f"admin.staff.{uuid.uuid4().hex[:8]}@test.com",
                    "document_number": f"ADMSTAFF{random.randint(10000, 99999)}",
                    "document_type": "CC",
                    "password": "AdminStaffPass123!",
                    "role": UserRole.ADMINISTRATIVE.value
                }
            },
            "instructor": {
                "email": f"instructor.seed.{uuid.uuid4().hex[:8]}@test.com",
                "password": "InstructorSeedPass123!",
                "data": {
                    "first_name": "Instructor",
                    "last_name": "Seed",
                    "email": f"instructor.seed.{uuid.uuid4().hex[:8]}@test.com",
                    "document_number": f"INSSEED{random.randint(10000, 99999)}",
                    "document_type": "CC",
                    "password": "InstructorSeedPass123!",
                    "role": UserRole.INSTRUCTOR.value
                }
            },
            "apprentice": {
                "email": f"apprentice.seed.{uuid.uuid4().hex[:8]}@test.com",
                "password": "ApprenticeSeedPass123!",
                "data": {
                    "first_name": "Apprentice",
                    "last_name": "Seed",
                    "email": f"apprentice.seed.{uuid.uuid4().hex[:8]}@test.com",
                    "document_number": f"APPSEED{random.randint(10000, 99999)}",
                    "document_type": "CC",
                    "password": "ApprenticeSeedPass123!",
                    "role": UserRole.APPRENTICE.value
                }
            }
        }
        
        self._seed_users = seed_users
        return seed_users

    def seed_database(self) -> Dict[str, Dict]:
        """Sembrar la base de datos con usuarios para testing."""
        if not self._seed_users:
            self.create_seed_users()

        seeded_users = {}

        # Crear admin primero (necesario para crear otros usuarios)
        admin_data = self._seed_users["admin"]["data"]
        
        # Crear admin directamente usando el endpoint público o método directo
        # (El primer admin podría necesitar un método especial)
        response = self.client.post("/users/", json=admin_data)
        
        if response.status_code == 201:
            seeded_users["admin"] = response.json()
            admin_token = self.get_auth_token(
                self._seed_users["admin"]["email"], 
                self._seed_users["admin"]["password"]
            )
            if admin_token:
                self._user_tokens["admin"] = admin_token
                
                # Usar admin token para crear otros usuarios
                admin_headers = self.get_auth_headers(admin_token)
                
                for role in ["administrative", "instructor", "apprentice"]:
                    user_data = self._seed_users[role]["data"]
                    response = self.client.post("/users/", json=user_data, headers=admin_headers)
                    
                    if response.status_code == 201:
                        seeded_users[role] = response.json()
                        
                        # Obtener token para cada usuario
                        token = self.get_auth_token(
                            self._seed_users[role]["email"],
                            self._seed_users[role]["password"]
                        )
                        if token:
                            self._user_tokens[role] = token

        return seeded_users

    def get_auth_token(self, email: str, password: str) -> Optional[str]:
        """Obtener token de autenticación."""
        try:
            response = self.client.post("/auth/login", json={
                "username": email,
                "password": password
            })
            
            if response.status_code == 200:
                return response.json()["access_token"]
        except Exception as e:
            print(f"Error getting auth token: {e}")
        
        return None

    def get_auth_headers(self, token: str) -> Dict[str, str]:
        """Obtener headers de autenticación."""
        return {"Authorization": f"Bearer {token}"}

    def get_user_token(self, role: str) -> Optional[str]:
        """Obtener token para un rol específico."""
        return self._user_tokens.get(role)

    def get_user_headers(self, role: str) -> Optional[Dict[str, str]]:
        """Obtener headers de autenticación para un rol específico."""
        token = self.get_user_token(role)
        if token:
            return self.get_auth_headers(token)
        return None

    def get_admin_headers(self) -> Optional[Dict[str, str]]:
        """Obtener headers de admin."""
        return self.get_user_headers("admin")

    def get_instructor_headers(self) -> Optional[Dict[str, str]]:
        """Obtener headers de instructor."""
        return self.get_user_headers("instructor")

    def get_administrative_headers(self) -> Optional[Dict[str, str]]:
        """Obtener headers de administrative."""
        return self.get_user_headers("administrative")

    def get_apprentice_headers(self) -> Optional[Dict[str, str]]:
        """Obtener headers de apprentice."""
        return self.get_user_headers("apprentice")

    def create_test_user(self, role: UserRole = UserRole.APPRENTICE, 
                        prefix: str = "test") -> Tuple[Dict, Optional[str]]:
        """Crear un usuario temporal para testing."""
        user_data = {
            "first_name": f"{prefix.title()}",
            "last_name": "User",
            "email": f"{prefix}.{uuid.uuid4().hex[:8]}@test.com",
            "document_number": f"{prefix.upper()}{random.randint(10000, 99999)}",
            "document_type": "CC",
            "password": f"{prefix.title()}Pass123!",
            "role": role.value
        }

        # Necesitamos headers de admin para crear usuarios
        admin_headers = self.get_admin_headers()
        if not admin_headers:
            return user_data, None

        response = self.client.post("/users/", json=user_data, headers=admin_headers)
        
        if response.status_code == 201:
            created_user = response.json()
            token = self.get_auth_token(user_data["email"], user_data["password"])
            return created_user, token
        
        return user_data, None

    def cleanup_test_data(self):
        """Limpiar datos de test (si es necesario)."""
        # Para SQLite en memoria, no es necesario limpiar
        # Para bases de datos persistentes, aquí se implementaría la limpieza
        self._seed_users = {}
        self._user_tokens = {}


class TestDataFactory:
    """Factory para crear datos de test."""

    @staticmethod
    def create_user_data(role: UserRole = UserRole.APPRENTICE, 
                        prefix: str = "test") -> Dict:
        """Crear datos de usuario para testing."""
        return {
            "first_name": f"{prefix.title()}",
            "last_name": "User",
            "email": f"{prefix}.{uuid.uuid4().hex[:8]}@test.com",
            "document_number": f"{prefix.upper()}{random.randint(10000000, 99999999)}",
            "document_type": "CC",
            "password": f"{prefix.title()}Pass123!",
            "role": role.value
        }

    @staticmethod
    def create_password_change_data(current_password: str = "OldPass123!", 
                                   new_password: str = "NewPass123!") -> Dict:
        """Crear datos para cambio de contraseña."""
        return {
            "current_password": current_password,
            "new_password": new_password
        }

    @staticmethod
    def create_invalid_user_data() -> Dict:
        """Crear datos de usuario inválidos para testing."""
        return {
            "first_name": "",  # Inválido: vacío
            "last_name": "Test",
            "email": "invalid-email",  # Inválido: formato email
            "document_number": "123",  # Inválido: muy corto
            "document_type": "XX",  # Inválido: tipo no válido
            "password": "weak",  # Inválido: contraseña débil
            "role": "invalid_role"  # Inválido: rol no existe
        }
