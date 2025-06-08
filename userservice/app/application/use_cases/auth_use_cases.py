"""Authentication use cases for user service."""

from datetime import datetime
from uuid import UUID

from ...domain import (
    UserRepositoryInterface, 
    User, 
    Email,
    AuthenticationError,
    UserNotFoundError,
    UserInactiveError,
    InvalidPasswordError,
)
from ..interfaces import PasswordServiceInterface, TokenServiceInterface
from ..dtos import LoginDTO, TokenResponseDTO, UserResponseDTO


class LoginUseCase:
    """Use case for user authentication."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        password_service: PasswordServiceInterface,
        token_service: TokenServiceInterface,
    ):
        self._user_repository = user_repository
        self._password_service = password_service
        self._token_service = token_service
    
    async def execute(self, login_data: LoginDTO) -> TokenResponseDTO:
        """Execute user login."""
        # Validate email format
        try:
            email = Email(login_data.email)
        except Exception as e:
            raise AuthenticationError("Invalid email format") from e
        
        # Get user by email
        user = await self._user_repository.get_by_email(email.value)
        if not user:
            raise AuthenticationError("Invalid credentials")
        
        # Check if user is active
        if not user.is_active:
            raise UserInactiveError(str(user.id))
        
        # Verify password
        if not self._password_service.verify_password(login_data.password, user.hashed_password):
            raise AuthenticationError("Invalid credentials")
        
        # Record login
        user.record_login()
        await self._user_repository.update(user)
        
        # Create tokens
        access_token = self._token_service.create_access_token(
            user_id=user.id,
            role=user.role.value
        )
        
        # Create user response DTO
        user_response = UserResponseDTO(
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
        
        return TokenResponseDTO(
            access_token=access_token,
            token_type="bearer",
            expires_in=3600,  # 1 hour
            user=user_response,
        )


class LogoutUseCase:
    """Use case for user logout."""
    
    def __init__(self, token_service: TokenServiceInterface):
        self._token_service = token_service
    
    async def execute(self, token: str) -> None:
        """Execute user logout by revoking token."""
        self._token_service.revoke_token(token)


class ValidateTokenUseCase:
    """Use case for token validation."""
    
    def __init__(
        self,
        token_service: TokenServiceInterface,
        user_repository: UserRepositoryInterface,
    ):
        self._token_service = token_service
        self._user_repository = user_repository
    
    async def execute(self, token: str) -> UserResponseDTO:
        """Validate token and return user information."""
        # Check if token is valid and not revoked
        if not self._token_service.is_token_valid(token) or self._token_service.is_token_revoked(token):
            raise AuthenticationError("Invalid or expired token")
        
        # Decode token to get user information
        try:
            token_data = self._token_service.decode_token(token)
            user_id = UUID(token_data["sub"])
        except Exception as e:
            raise AuthenticationError("Invalid token format") from e
        
        # Get user from database
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(str(user_id))
        
        # Check if user is still active
        if not user.is_active:
            raise UserInactiveError(str(user.id))
        
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
