"""SQLAlchemy implementation of UserRepository."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain import (
    UserRepositoryInterface, 
    User, 
    UserRole,
    Email,
    DocumentNumber,
    DocumentType,
    UserNotFoundError,
)
from ..models import UserModel


class SQLAlchemyUserRepository(UserRepositoryInterface):
    """SQLAlchemy implementation of UserRepositoryInterface."""
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    def _model_to_entity(self, model: UserModel) -> User:
        """Convert UserModel to User entity."""
        return User(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            email=Email(model.email),
            document_number=DocumentNumber(model.document_number, DocumentType(model.document_type)),
            hashed_password=model.hashed_password,
            role=model.role,
            is_active=model.is_active,
            must_change_password=model.must_change_password,
            phone=model.phone,
            created_at=model.created_at,
            updated_at=model.updated_at,
            last_login_at=model.last_login_at,
            deleted_at=model.deleted_at,
        )
    
    def _entity_to_model(self, entity: User) -> UserModel:
        """Convert User entity to UserModel."""
        return UserModel(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email.value,
            document_number=entity.document_number.value,
            document_type=entity.document_number.document_type.value,
            hashed_password=entity.hashed_password,
            role=entity.role,
            is_active=entity.is_active,
            must_change_password=entity.must_change_password,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            last_login_at=entity.last_login_at,
        )
    
    async def create(self, user: User) -> User:
        """Create a new user."""
        model = self._entity_to_model(user)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._model_to_entity(model)
    
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email.lower())
        )
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def get_by_document_number(self, document_number: str) -> Optional[User]:
        """Get user by document number."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.document_number == document_number.upper())
        )
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
    
    async def update(self, user: User) -> User:
        """Update user."""
        # Get existing model
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            raise UserNotFoundError(str(user.id))
        
        # Update fields
        model.first_name = user.first_name
        model.last_name = user.last_name
        model.email = user.email.value
        model.document_number = user.document_number.value
        model.document_type = user.document_number.document_type.value
        model.hashed_password = user.hashed_password
        model.role = user.role
        model.is_active = user.is_active
        model.must_change_password = user.must_change_password
        model.updated_at = user.updated_at
        model.last_login_at = user.last_login_at
        model.deleted_at = user.deleted_at  # PASO 4: Soft delete support
        model.phone = user.phone  # PASO 4: Additional user field
        
        await self._session.flush()
        await self._session.refresh(model)
        return self._model_to_entity(model)
    
    async def delete(self, user_id: UUID) -> bool:
        """Delete user by ID."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        await self._session.delete(model)
        return True
    
    async def list_users(
        self,
        offset: int = 0,
        limit: int = 10,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
        search_term: Optional[str] = None,
    ) -> List[User]:
        """List users with filtering and pagination."""
        query = select(UserModel)
        
        # Apply filters
        if role:
            query = query.where(UserModel.role == role)
        
        if is_active is not None:
            query = query.where(UserModel.is_active == is_active)
        
        if search_term:
            search_pattern = f"%{search_term.lower()}%"
            query = query.where(
                or_(
                    func.lower(UserModel.first_name).contains(search_pattern),
                    func.lower(UserModel.last_name).contains(search_pattern),
                    func.lower(UserModel.email).contains(search_pattern),
                    UserModel.document_number.contains(search_term.upper()),
                )
            )
        
        # Apply pagination and ordering
        query = query.order_by(UserModel.created_at.desc()).offset(offset).limit(limit)
        
        result = await self._session.execute(query)
        models = result.scalars().all()
        
        return [self._model_to_entity(model) for model in models]
    
    async def count_users(
        self,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
        search_term: Optional[str] = None,
    ) -> int:
        """Count users with filtering."""
        query = select(func.count(UserModel.id))
        
        # Apply same filters as list_users
        if role:
            query = query.where(UserModel.role == role)
        
        if is_active is not None:
            query = query.where(UserModel.is_active == is_active)
        
        if search_term:
            search_pattern = f"%{search_term.lower()}%"
            query = query.where(
                or_(
                    func.lower(UserModel.first_name).contains(search_pattern),
                    func.lower(UserModel.last_name).contains(search_pattern),
                    func.lower(UserModel.email).contains(search_pattern),
                    UserModel.document_number.contains(search_term.upper()),
                )
            )
        
        result = await self._session.execute(query)
        return result.scalar()
    
    async def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email."""
        result = await self._session.execute(
            select(func.count(UserModel.id)).where(UserModel.email == email.lower())
        )
        count = result.scalar()
        return count > 0
    
    async def exists_by_document_number(self, document_number: str) -> bool:
        """Check if user exists by document number."""
        result = await self._session.execute(
            select(func.count(UserModel.id)).where(UserModel.document_number == document_number.upper())
        )
        count = result.scalar()
        return count > 0

    # PASO 5: Métodos adicionales para funcionalidades de autenticación críticas
    
    async def get_by_reset_token(self, reset_token: str) -> Optional[User]:
        """Get user by password reset token."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.password_reset_token == reset_token)
        )
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
