"""User management use cases."""

from uuid import UUID
from typing import Optional

from ...domain import (
    UserRepositoryInterface,
    User,
    UserRole,
    Email,
    DocumentNumber,
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidPasswordError,
    UserInactiveError,
)
from ..interfaces import PasswordServiceInterface, EmailServiceInterface
from ..dtos import (
    CreateUserDTO,
    UpdateUserDTO,
    ChangePasswordDTO,
    UserResponseDTO,
    UserListDTO,
    UserFilterDTO,
)


class CreateUserUseCase:
    """Use case for creating a new user."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        password_service: PasswordServiceInterface,
        email_service: EmailServiceInterface,
    ):
        self._user_repository = user_repository
        self._password_service = password_service
        self._email_service = email_service
    
    async def execute(self, user_data: CreateUserDTO) -> UserResponseDTO:
        """Create a new user."""
        # Validate password strength
        if not self._password_service.validate_password_strength(user_data.password):
            raise InvalidPasswordError("Password does not meet security requirements")
        
        # Create value objects
        email = Email(user_data.email)
        document_number = DocumentNumber(user_data.document_number, user_data.document_type)
        
        # Check if user already exists
        if await self._user_repository.exists_by_email(email.value):
            raise UserAlreadyExistsError("email", email.value)
        
        if await self._user_repository.exists_by_document_number(document_number.value):
            raise UserAlreadyExistsError("document_number", document_number.value)
        
        # Hash password
        hashed_password = self._password_service.hash_password(user_data.password)
        
        # Create user entity
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=email,
            document_number=document_number,
            hashed_password=hashed_password,
            role=user_data.role,
        )
        
        # Save user
        created_user = await self._user_repository.create(user)
        
        # Send welcome email
        try:
            await self._email_service.send_welcome_email(
                to_email=created_user.email.value,
                user_name=created_user.full_name(),
                temporary_password=user_data.password,
            )
        except Exception:
            # Log error but don't fail user creation
            pass
        
        return UserResponseDTO(
            id=created_user.id,
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            email=created_user.email.value,
            document_number=created_user.document_number.value,
            document_type=created_user.document_number.document_type.value,
            role=created_user.role.value,
            is_active=created_user.is_active,
            must_change_password=created_user.must_change_password,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at,
            last_login_at=created_user.last_login_at,
        )


class GetUserByIdUseCase:
    """Use case for getting a user by ID."""
    
    def __init__(self, user_repository: UserRepositoryInterface):
        self._user_repository = user_repository
    
    async def execute(self, user_id: UUID) -> UserResponseDTO:
        """Get user by ID."""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(str(user_id))
        
        return UserResponseDTO(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email.value,
            document_number=user.document_number.value,
            document_type=user.document_number.document_type.value,
            role=user.role.value,
            is_active=user.is_active,
            must_change_password=user.must_change_password,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login_at=user.last_login_at,
        )


class UpdateUserUseCase:
    """Use case for updating user information."""
    
    def __init__(self, user_repository: UserRepositoryInterface):
        self._user_repository = user_repository
    
    async def execute(self, user_id: UUID, update_data: UpdateUserDTO) -> UserResponseDTO:
        """Update user information."""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(str(user_id))
        
        # Check if email is being changed and doesn't already exist
        if update_data.email:
            email = Email(update_data.email)
            if email.value != user.email.value:
                if await self._user_repository.exists_by_email(email.value):
                    raise UserAlreadyExistsError("email", email.value)
        
        # Update user profile
        user.update_profile(
            first_name=update_data.first_name,
            last_name=update_data.last_name,
            email=update_data.email,
        )
        
        # Save changes
        updated_user = await self._user_repository.update(user)
        
        return UserResponseDTO(
            id=updated_user.id,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            email=updated_user.email.value,
            document_number=updated_user.document_number.value,
            document_type=updated_user.document_number.document_type.value,
            role=updated_user.role.value,
            is_active=updated_user.is_active,
            must_change_password=updated_user.must_change_password,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            last_login_at=updated_user.last_login_at,
        )


class ChangePasswordUseCase:
    """Use case for changing user password."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        password_service: PasswordServiceInterface,
        email_service: EmailServiceInterface,
    ):
        self._user_repository = user_repository
        self._password_service = password_service
        self._email_service = email_service
    
    async def execute(self, user_id: UUID, password_data: ChangePasswordDTO) -> None:
        """Change user password."""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(str(user_id))
        
        if not user.is_active:
            raise UserInactiveError(str(user_id))
        
        # Verify current password
        if not self._password_service.verify_password(password_data.current_password, user.hashed_password):
            raise InvalidPasswordError("Current password is incorrect")
        
        # Validate new password strength
        if not self._password_service.validate_password_strength(password_data.new_password):
            raise InvalidPasswordError("New password does not meet security requirements")
        
        # Hash new password
        new_hashed_password = self._password_service.hash_password(password_data.new_password)
        
        # Change password
        user.change_password(new_hashed_password)
        
        # Save changes
        await self._user_repository.update(user)
        
        # Send notification email
        try:
            await self._email_service.send_password_changed_notification(
                to_email=user.email.value,
                user_name=user.full_name(),
            )
        except Exception:
            # Log error but don't fail password change
            pass


class ActivateUserUseCase:
    """Use case for activating a user."""
    
    def __init__(self, user_repository: UserRepositoryInterface):
        self._user_repository = user_repository
    
    async def execute(self, user_id: UUID) -> UserResponseDTO:
        """Activate a user."""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(str(user_id))
        
        user.activate()
        updated_user = await self._user_repository.update(user)
        
        return UserResponseDTO(
            id=updated_user.id,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            email=updated_user.email.value,
            document_number=updated_user.document_number.value,
            document_type=updated_user.document_number.document_type.value,
            role=updated_user.role.value,
            is_active=updated_user.is_active,
            must_change_password=updated_user.must_change_password,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            last_login_at=updated_user.last_login_at,
        )


class DeactivateUserUseCase:
    """Use case for deactivating a user."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        email_service: EmailServiceInterface,
    ):
        self._user_repository = user_repository
        self._email_service = email_service
    
    async def execute(self, user_id: UUID) -> UserResponseDTO:
        """Deactivate a user."""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(str(user_id))
        
        user.deactivate()
        updated_user = await self._user_repository.update(user)
        
        # Send notification email
        try:
            await self._email_service.send_account_deactivation_notification(
                to_email=updated_user.email.value,
                user_name=updated_user.full_name(),
            )
        except Exception:
            # Log error but don't fail deactivation
            pass
        
        return UserResponseDTO(
            id=updated_user.id,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            email=updated_user.email.value,
            document_number=updated_user.document_number.value,
            document_type=updated_user.document_number.document_type.value,
            role=updated_user.role.value,
            is_active=updated_user.is_active,
            must_change_password=updated_user.must_change_password,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            last_login_at=updated_user.last_login_at,
        )


class ListUsersUseCase:
    """Use case for listing users with pagination and filtering."""
    
    def __init__(self, user_repository: UserRepositoryInterface):
        self._user_repository = user_repository
    
    async def execute(
        self,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[UserFilterDTO] = None,
    ) -> UserListDTO:
        """List users with pagination and filtering."""
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10
        if page_size > 100:
            page_size = 100
        
        # Convert filters for repository
        role = filters.role if filters else None
        is_active = filters.is_active if filters else None
        search_term = filters.search_term if filters else None
        
        # Get users and total count
        users = await self._user_repository.list_users(
            offset=(page - 1) * page_size,
            limit=page_size,
            role=role,
            is_active=is_active,
            search_term=search_term,
        )
        
        total = await self._user_repository.count_users(
            role=role,
            is_active=is_active,
            search_term=search_term,
        )
        
        # Convert to DTOs
        user_dtos = [
            UserResponseDTO(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email.value,
                document_number=user.document_number.value,
                document_type=user.document_number.document_type.value,
                role=user.role.value,
                is_active=user.is_active,
                must_change_password=user.must_change_password,
                created_at=user.created_at,
                updated_at=user.updated_at,
                last_login_at=user.last_login_at,
            )
            for user in users
        ]
        
        total_pages = (total + page_size - 1) // page_size
        
        return UserListDTO(
            users=user_dtos,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
