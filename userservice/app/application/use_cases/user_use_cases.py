"""User management use cases."""

from uuid import UUID
from typing import Optional

from ...domain import (
    UserRepositoryInterface,
    User,
    UserRole,
    Email,
    DocumentNumber,
    DocumentType,
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
    # PASO 4: Admin DTOs
    AdminUpdateUserDTO,
    UserDetailDTO,
    BulkUploadUserDTO,
    BulkUploadResultDTO,
    DeleteUserResultDTO,
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


# PASO 4: Casos de uso para administración avanzada de usuarios

class GetUserDetailUseCase:
    """Use case for getting detailed user information (admin view)."""
    
    def __init__(self, user_repository: UserRepositoryInterface):
        self._user_repository = user_repository
    
    async def execute(self, user_id: UUID) -> "UserDetailDTO":
        """Get detailed user information."""
        from ..dtos import UserDetailDTO
        
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(str(user_id))
        
        return UserDetailDTO(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email.value,
            document_number=user.document_number.value,
            document_type=user.document_number.document_type.value,
            phone=user.phone,
            role=user.role.value,
            is_active=user.is_active,
            must_change_password=user.must_change_password,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login_at=user.last_login_at,
            deleted_at=user.deleted_at,
        )


class AdminUpdateUserUseCase:
    """Use case for admin user update with all possible fields."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        password_service: PasswordServiceInterface,
        email_service: EmailServiceInterface,
    ):
        self._user_repository = user_repository
        self._password_service = password_service
        self._email_service = email_service
    
    async def execute(self, user_id: UUID, update_data: "AdminUpdateUserDTO") -> "UserDetailDTO":
        """Update user with admin privileges."""
        from ..dtos import AdminUpdateUserDTO, UserDetailDTO
        
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(str(user_id))
        
        # Check for email conflicts if email is being changed
        if update_data.email and update_data.email != user.email.value:
            email = Email(update_data.email)
            if await self._user_repository.exists_by_email(email.value):
                raise UserAlreadyExistsError("email", email.value)
        
        # Check for document number conflicts if being changed
        if update_data.document_number and update_data.document_number != user.document_number.value:
            if update_data.document_type:
                document_number = DocumentNumber(update_data.document_number, update_data.document_type)
            else:
                document_number = DocumentNumber(update_data.document_number, user.document_number.document_type)
            
            if await self._user_repository.exists_by_document_number(document_number.value):
                raise UserAlreadyExistsError("document_number", document_number.value)
        
        # Apply updates
        if update_data.first_name is not None:
            user.first_name = update_data.first_name
        if update_data.last_name is not None:
            user.last_name = update_data.last_name
        if update_data.email is not None:
            user.email = Email(update_data.email)
        if update_data.document_number is not None:
            if update_data.document_type:
                user.document_number = DocumentNumber(update_data.document_number, update_data.document_type)
            else:
                user.document_number = DocumentNumber(update_data.document_number, user.document_number.document_type)
        if update_data.phone is not None:
            user.phone = update_data.phone
        if update_data.role is not None:
            user.role = update_data.role
        if update_data.is_active is not None:
            if update_data.is_active:
                user.activate()
            else:
                user.deactivate()
        if update_data.must_change_password is not None:
            user.must_change_password = update_data.must_change_password
        
        # Save changes
        updated_user = await self._user_repository.update(user)
        
        # Send notification if user was deactivated
        if update_data.is_active is False:
            try:
                await self._email_service.send_account_deactivation_notification(
                    to_email=updated_user.email.value,
                    user_name=updated_user.full_name(),
                )
            except Exception:
                pass
        
        return UserDetailDTO(
            id=updated_user.id,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            email=updated_user.email.value,
            document_number=updated_user.document_number.value,
            document_type=updated_user.document_number.document_type.value,
            phone=updated_user.phone,
            role=updated_user.role.value,
            is_active=updated_user.is_active,
            must_change_password=updated_user.must_change_password,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            last_login_at=updated_user.last_login_at,
            deleted_at=updated_user.deleted_at,
        )


class DeleteUserUseCase:
    """Use case for deleting (soft delete) a user."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        email_service: EmailServiceInterface,
    ):
        self._user_repository = user_repository
        self._email_service = email_service
    
    async def execute(self, user_id: UUID, admin_user_id: UUID) -> "DeleteUserResultDTO":
        """Soft delete a user."""
        from datetime import datetime
        from ..dtos import DeleteUserResultDTO
        
        # Prevent admin from deleting themselves
        if user_id == admin_user_id:
            raise ValueError("Admin cannot delete their own account")
        
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(str(user_id))
        
        # Perform soft delete
        user.soft_delete()
        
        # Save changes
        updated_user = await self._user_repository.update(user)
        
        # Send notification email
        try:
            await self._email_service.send_account_deactivation_notification(
                to_email=updated_user.email.value,
                user_name=updated_user.full_name(),
            )
        except Exception:
            pass
        
        return DeleteUserResultDTO(
            user_id=user_id,
            deleted_at=updated_user.deleted_at,
            message="User successfully deactivated"
        )


class BulkUploadUsersUseCase:
    """Use case for bulk user upload from CSV."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        password_service: PasswordServiceInterface,
        email_service: EmailServiceInterface,
    ):
        self._user_repository = user_repository
        self._password_service = password_service
        self._email_service = email_service
    
    async def execute(self, csv_content: str) -> BulkUploadResultDTO:
        """Process bulk user upload from CSV content."""
        import csv
        import io
        import base64
        
        total_processed = 0
        successful = 0
        failed = 0
        errors = []
        created_users = []
        
        try:
            # Decode base64 content if needed
            try:
                decoded_content = base64.b64decode(csv_content).decode('utf-8')
            except Exception:
                # If not base64, use as-is
                decoded_content = csv_content
            
            # Parse CSV
            csv_reader = csv.DictReader(io.StringIO(decoded_content))
            
            for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 because row 1 is headers
                total_processed += 1
                
                try:
                    # Validate required fields
                    required_fields = ['first_name', 'last_name', 'email', 'document_number', 'document_type', 'role']
                    missing_fields = [field for field in required_fields if not row.get(field)]
                    if missing_fields:
                        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
                    
                    # Create DTO
                    user_dto = BulkUploadUserDTO(
                        first_name=row['first_name'].strip(),
                        last_name=row['last_name'].strip(),
                        email=row['email'].strip(),
                        document_number=row['document_number'].strip(),
                        document_type=DocumentType(row['document_type'].strip()),
                        role=UserRole(row['role'].strip()),
                        phone=row.get('phone', '').strip() or None,
                    )
                    
                    # Create user (password = document number)
                    email = Email(user_dto.email)
                    document_number = DocumentNumber(user_dto.document_number, user_dto.document_type)
                    
                    # Check duplicates
                    if await self._user_repository.exists_by_email(email.value):
                        raise ValueError(f"Email already exists: {email.value}")
                    
                    if await self._user_repository.exists_by_document_number(document_number.value):
                        raise ValueError(f"Document number already exists: {document_number.value}")
                    
                    # Use document number as initial password
                    password = user_dto.document_number
                    hashed_password = self._password_service.hash_password(password)
                    
                    # Create user entity
                    user = User(
                        first_name=user_dto.first_name,
                        last_name=user_dto.last_name,
                        email=email,
                        document_number=document_number,
                        hashed_password=hashed_password,
                        role=user_dto.role,
                        phone=user_dto.phone,
                        must_change_password=True,  # Force password change on first login
                    )
                    
                    # Save user
                    created_user = await self._user_repository.create(user)
                    successful += 1
                    
                    created_users.append({
                        "id": str(created_user.id),
                        "email": created_user.email.value,
                        "document_number": created_user.document_number.value,
                        "role": created_user.role.value,
                    })
                    
                    # Send welcome email (async, don't fail if it fails)
                    try:
                        await self._email_service.send_welcome_email(
                            to_email=created_user.email.value,
                            user_name=created_user.full_name(),
                            temporary_password=password,
                        )
                    except Exception:
                        pass
                    
                except Exception as e:
                    failed += 1
                    errors.append({
                        "row": row_num,
                        "error": str(e),
                        "data": dict(row),
                    })
            
        except Exception as e:
            return BulkUploadResultDTO(
                total_processed=0,
                successful=0,
                failed=1,
                errors=[{"row": 1, "error": f"CSV parsing error: {str(e)}", "data": {}}],
                created_users=[],
            )
        
        return BulkUploadResultDTO(
            total_processed=total_processed,
            successful=successful,
            failed=failed,
            errors=errors,
            created_users=created_users,
        )
