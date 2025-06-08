"""Admin user seeder for database initialization."""

import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.entities.user_entity import User
from app.domain.value_objects.user_role import UserRole
from app.domain.value_objects.email import Email
from app.domain.value_objects.document_number import DocumentNumber
from app.domain.value_objects.document_type import DocumentType
from app.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.infrastructure.adapters.bcrypt_password_service import BcryptPasswordService


class AdminSeeder:
    """Seeder for creating the first admin user."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = SQLAlchemyUserRepository(session)
        self.password_service = BcryptPasswordService()

    async def seed_first_admin(
        self,
        email: str = "admin@sicora.sena.edu.co",
        password: str = "AdminSicora123!",
        first_name: str = "Admin",
        last_name: str = "SICORA",
        document_number: str = "1000000001",
    ) -> Optional[User]:
        """
        Crear el primer usuario admin si no existe ningún usuario en el sistema.
        
        Args:
            email: Email del admin (default: admin@sicora.sena.edu.co)
            password: Contraseña del admin (default: AdminSicora123!)
            first_name: Nombre del admin (default: Admin)
            last_name: Apellido del admin (default: SICORA)
            document_number: Número de documento (default: 1000000001)
            
        Returns:
            User: El usuario admin creado o None si ya existen usuarios
        """
        # Verificar si ya existen usuarios en el sistema
        try:
            existing_users = await self.user_repository.list(
                filters={"limit": 1, "offset": 0}
            )
            if existing_users.users:
                print("❌ Ya existen usuarios en el sistema. No se creará admin inicial.")
                return None
        except Exception:
            # Si hay error al consultar, procedemos con la creación
            pass

        # Verificar si el admin ya existe por email
        try:
            existing_admin = await self.user_repository.get_by_email(email)
            if existing_admin:
                print(f"❌ Usuario admin con email {email} ya existe.")
                return existing_admin
        except Exception:
            # Si no existe, procedemos con la creación
            pass

        # Crear el usuario admin
        try:
            # Crear value objects
            admin_email = Email(email)
            admin_document = DocumentNumber(document_number, DocumentType.CC)
            
            # Hash de la contraseña
            hashed_password = self.password_service.hash_password(password)
            
            # Crear entidad User
            admin_user = User(
                id=uuid.uuid4(),
                first_name=first_name,
                last_name=last_name,
                email=admin_email,
                document_number=admin_document,
                hashed_password=hashed_password,
                role=UserRole.ADMIN,
                is_active=True,
                must_change_password=False,  # Admin inicial no necesita cambiar contraseña
            )
            
            # Guardar en base de datos
            created_admin = await self.user_repository.create(admin_user)
            await self.session.commit()  # Asegurar commit para persistir datos
            
            print(f"✅ Usuario admin inicial creado exitosamente:")
            print(f"   Email: {email}")
            print(f"   Contraseña: {password}")
            print(f"   ID: {created_admin.id}")
            
            return created_admin
            
        except Exception as e:
            print(f"❌ Error al crear usuario admin inicial: {e}")
            raise

    async def seed_test_admin(
        self,
        email: str,
        password: str,
        first_name: str = "Test",
        last_name: str = "Admin",
        document_number: str = "1000000002",
        force_recreate: bool = False,
    ) -> User:
        """
        Crear un usuario admin específico para testing.
        
        Args:
            email: Email del admin
            password: Contraseña del admin
            first_name: Nombre del admin
            last_name: Apellido del admin
            document_number: Número de documento
            force_recreate: Si True, elimina y recrea el usuario si ya existe
            
        Returns:
            User: El usuario admin creado o existente
            
        Raises:
            Exception: Si hay error en la creación
        """
        try:
            # Verificar si el admin ya existe
            existing_admin = None
            try:
                existing_admin = await self.user_repository.get_by_email(email)
            except Exception:
                pass  # El usuario no existe
            
            if existing_admin and not force_recreate:
                print(f"ℹ️  Usuario admin de testing ya existe: {email}")
                return existing_admin
            
            if existing_admin and force_recreate:
                # Eliminar el usuario existente
                await self.user_repository.delete(existing_admin.id)
                await self.session.commit()  # Commit para asegurar eliminación
                print(f"🗑️  Usuario admin existente eliminado: {email}")
            
            # Crear value objects
            admin_email = Email(email)
            admin_document = DocumentNumber(document_number, DocumentType.CC)
            
            # Hash de la contraseña
            hashed_password = self.password_service.hash_password(password)
            
            # Crear entidad User
            admin_user = User(
                id=uuid.uuid4(),
                first_name=first_name,
                last_name=last_name,
                email=admin_email,
                document_number=admin_document,
                hashed_password=hashed_password,
                role=UserRole.ADMIN,
                is_active=True,
                must_change_password=False,
            )
            
            # Guardar en base de datos
            created_admin = await self.user_repository.create(admin_user)
            await self.session.commit()  # Asegurar commit para persistir datos
            
            print(f"✅ Usuario admin de testing creado: {email}")
            
            return created_admin
            
        except Exception as e:
            print(f"❌ Error al crear usuario admin de testing: {e}")
            raise
