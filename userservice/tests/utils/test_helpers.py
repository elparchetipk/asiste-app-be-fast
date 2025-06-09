"""
Test helpers y utilidades para testing con autenticación JWT.
"""

import uuid
import random
from typing import Dict, Optional, Tuple
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.value_objects.user_role import UserRole
from app.infrastructure.config.database import get_db_session
from app.infrastructure.seeders.admin_seeder import AdminSeeder


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
                "password": "ChiefSecure123!",  # Evitar "admin" y "pass"
                "data": {
                    "first_name": "Admin",
                    "last_name": "Seed", 
                    "email": f"admin.seed.{uuid.uuid4().hex[:8]}@test.com",
                    "document_number": f"{random.randint(10000000, 99999999)}",
                    "document_type": "CC",
                    "password": "ChiefSecure123!",
                    "role": UserRole.ADMIN.value
                }
            },
            "administrative": {
                "email": f"admin.staff.{uuid.uuid4().hex[:8]}@test.com",
                "password": "StaffSecure123!",  # Evitar "admin" y "pass"
                "data": {
                    "first_name": "Administrative",
                    "last_name": "Staff",
                    "email": f"admin.staff.{uuid.uuid4().hex[:8]}@test.com",
                    "document_number": f"{random.randint(20000000, 29999999)}",
                    "document_type": "CC",
                    "password": "StaffSecure123!",
                    "role": UserRole.ADMINISTRATIVE.value
                }
            },
            "instructor": {
                "email": f"instructor.seed.{uuid.uuid4().hex[:8]}@test.com",
                "password": "TeacherSecure123!",  # Evitar "pass"
                "data": {
                    "first_name": "Instructor",
                    "last_name": "Seed",
                    "email": f"instructor.seed.{uuid.uuid4().hex[:8]}@test.com",
                    "document_number": f"{random.randint(30000000, 39999999)}",
                    "document_type": "CC",
                    "password": "TeacherSecure123!",
                    "role": UserRole.INSTRUCTOR.value
                }
            },
            "apprentice": {
                "email": f"apprentice.seed.{uuid.uuid4().hex[:8]}@test.com",
                "password": "StudentSecure123!",  # Evitar "pass"
                "data": {
                    "first_name": "Apprentice",
                    "last_name": "Seed",
                    "email": f"apprentice.seed.{uuid.uuid4().hex[:8]}@test.com",
                    "document_number": f"{random.randint(40000000, 49999999)}",
                    "document_type": "CC",
                    "password": "StudentSecure123!",
                    "role": UserRole.APPRENTICE.value
                }
            }
        }
        
        self._seed_users = seed_users
        return seed_users

    def seed_database(self) -> Dict[str, Dict]:
        """Sembrar la base de datos con usuarios para testing (versión síncrona)."""
        if not self._seed_users:
            self.create_seed_users()

        seeded_users = {}

        # Para usar en tests síncronos, crear admin directamente con credenciales conocidas
        # Intentar login para verificar si el admin ya existe
        admin_data = self._seed_users["admin"]["data"]
        admin_token = self.get_auth_token(
            admin_data["email"], 
            admin_data["password"]
        )
        
        if admin_token:
            # El admin ya existe, obtener sus datos
            self._user_tokens["admin"] = admin_token
            admin_headers = self.get_auth_headers(admin_token)
            
            # Simular datos del admin existente para compatibilidad
            seeded_users["admin"] = {
                "email": admin_data["email"],
                "first_name": admin_data["first_name"],
                "last_name": admin_data["last_name"],
                "document_number": admin_data["document_number"],
                "role": admin_data["role"],
                "is_active": True
            }
            
            # Crear otros usuarios usando el admin token
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
                else:
                    print(f"❌ Error al crear usuario {role}: {response.status_code} - {response.text}")
        else:
            print("❌ No se pudo obtener token de admin. Asegúrate de que el admin inicial existe.")
            print("💡 Ejecuta seed_admin_user() primero para crear el usuario admin inicial.")

        return seeded_users

    async def seed_admin_user(self) -> bool:
        """Crear el usuario admin inicial usando AdminSeeder."""
        try:
            admin_data = self._seed_users["admin"]["data"] if self._seed_users else {}
            
            if not admin_data:
                self.create_seed_users()
                admin_data = self._seed_users["admin"]["data"]
            
            async for session in get_db_session():
                seeder = AdminSeeder(session)
                
                admin_user = await seeder.seed_test_admin(
                    email=admin_data["email"],
                    password=admin_data["password"],
                    first_name=admin_data["first_name"],
                    last_name=admin_data["last_name"],
                    document_number=admin_data["document_number"]
                )
                
                if admin_user:
                    print(f"✅ Usuario admin creado para testing: {admin_data['email']}")
                    
                    # Obtener token de autenticación para el admin recién creado
                    admin_token = self.get_auth_token(
                        admin_data["email"], 
                        admin_data["password"]
                    )
                    
                    if admin_token:
                        self._user_tokens["admin"] = admin_token
                        print(f"✅ Token de admin obtenido y guardado")
                        return True
                    else:
                        print(f"❌ No se pudo obtener token para admin: {admin_data['email']}")
                        return False
                break
                
        except Exception as e:
            print(f"❌ Error al crear admin user: {e}")
            
        return False

    def get_auth_token(self, email: str, password: str) -> Optional[str]:
        """Obtener token de autenticación."""
        try:
            response = self.client.post("/api/v1/auth/login", json={
                "email": email,
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

    def get_admin_token(self) -> Optional[str]:
        """Obtener token de admin."""
        return self.get_user_token("admin")

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
        # Mapear prefijos a palabras seguras para evitar patrones débiles
        safe_prefix_map = {
            "test": "Test",
            "admin": "Chief",
            "user": "Person",
            "password": "Secret",
            "instructor": "Teacher",
            "apprentice": "Student",
            "administrative": "Staff"
        }
        
        safe_prefix = safe_prefix_map.get(prefix.lower(), prefix.title())
        
        user_data = {
            "first_name": f"{prefix.title()}",
            "last_name": "User",
            "email": f"{prefix}.{uuid.uuid4().hex[:8]}@test.com",
            "document_number": f"{random.randint(50000000, 59999999)}",
            "document_type": "CC",
            "password": f"{safe_prefix}Secure{random.randint(100, 999)}!",
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
        # Generar número de documento válido para CC (7-10 dígitos)
        base_document = random.randint(10000000, 99999999)  # 8 dígitos
        
        # Mapear prefijos a palabras seguras para evitar patrones débiles (admin, user, password)
        safe_prefix_map = {
            "test": "Test",
            "admin": "Chief",      # Evitar "admin"
            "user": "Person",      # Evitar "user" 
            "password": "Secret",  # Evitar "password"
            "instructor": "Teacher",
            "apprentice": "Student",
            "administrative": "Staff"
        }
        
        safe_prefix = safe_prefix_map.get(prefix.lower(), prefix.title())
        
        # Generar contraseña que cumpla todos los requisitos de seguridad
        # Mínimo 8 chars, 1 mayúscula, 1 minúscula, 1 dígito, 1 especial
        password_suffix = random.randint(100, 999)
        secure_password = f"{safe_prefix}Secure{password_suffix}!"
        
        return {
            "first_name": f"{prefix.title()}",
            "last_name": "User", 
            "email": f"{prefix}.{uuid.uuid4().hex[:8]}@test.com",
            "document_number": str(base_document),  # Solo dígitos para CC
            "document_type": "CC",
            "password": secure_password,
            "role": role.value
        }

    @staticmethod
    def create_password_change_data(current_password: str = "OldSecure123!", 
                                   new_password: str = "NewSecure456!") -> Dict:
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
