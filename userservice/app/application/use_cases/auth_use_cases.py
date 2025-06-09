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


class ForgotPasswordUseCase:
    """Use case for requesting password reset (HU-BE-005)."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        # email_service: EmailServiceInterface,  # TODO: Implementar cuando esté disponible
    ):
        self._user_repository = user_repository
        # self._email_service = email_service
    
    async def execute(self, forgot_password_data: "ForgotPasswordDTO") -> None:
        """Execute forgot password request."""
        from ..dtos import ForgotPasswordDTO
        
        # Validate email format
        try:
            email = Email(forgot_password_data.email)
        except Exception as e:
            # Return success even for invalid emails (security)
            return
        
        # Get user by email
        user = await self._user_repository.get_by_email(email.value)
        if not user or not user.is_active:
            # Return success even if user doesn't exist (security)
            return
        
        # Generate secure reset token
        import secrets
        import string
        from datetime import timedelta
        
        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        expires_at = datetime.utcnow() + timedelta(hours=24)  # 24 hour expiration
        
        # Set reset token on user
        user.set_reset_password_token(token, expires_at)
        await self._user_repository.update(user)
        
        # TODO: Send email with reset link when email service is available
        # reset_link = f"https://app.example.com/reset-password?token={token}"
        # await self._email_service.send_password_reset_email(user.email.value, reset_link)


class ResetPasswordUseCase:
    """Use case for resetting password with token (HU-BE-006)."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        password_service: PasswordServiceInterface,
        token_service: TokenServiceInterface,
    ):
        self._user_repository = user_repository
        self._password_service = password_service
        self._token_service = token_service
    
    async def execute(self, reset_data: "ResetPasswordDTO") -> None:
        """Execute password reset with token."""
        from ..dtos import ResetPasswordDTO
        from ...domain.exceptions import InvalidTokenError
        
        # Find user by reset token
        user = await self._user_repository.get_by_reset_token(reset_data.token)
        if not user:
            raise InvalidTokenError("Invalid or expired reset token")
        
        # Validate token
        if not user.is_reset_token_valid(reset_data.token):
            raise InvalidTokenError("Invalid or expired reset token")
        
        # Validate new password strength
        if not self._password_service.is_password_strong(reset_data.new_password):
            from ...domain.exceptions import WeakPasswordError
            raise WeakPasswordError("Password does not meet security requirements")
        
        # Hash new password
        new_hashed_password = self._password_service.hash_password(reset_data.new_password)
        
        # Update user password and clear reset token
        user.change_password(new_hashed_password)
        user.clear_reset_password_token()
        
        # Revoke all existing refresh tokens for security
        # self._token_service.revoke_all_user_tokens(user.id)  # TODO: Implement when available
        
        await self._user_repository.update(user)


class ForceChangePasswordUseCase:
    """Use case for forced password change (HU-BE-007)."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        password_service: PasswordServiceInterface,
        token_service: TokenServiceInterface,
    ):
        self._user_repository = user_repository
        self._password_service = password_service
        self._token_service = token_service
    
    async def execute(self, force_change_data: "ForceChangePasswordDTO") -> None:
        """Execute forced password change."""
        from ..dtos import ForceChangePasswordDTO
        from ...domain.exceptions import WeakPasswordError
        
        # Get user
        user = await self._user_repository.get_by_id(force_change_data.user_id)
        if not user:
            raise UserNotFoundError(str(force_change_data.user_id))
        
        # Check if user is active
        if not user.is_active:
            raise UserInactiveError(str(user.id))
        
        # Verify user has must_change_password flag set
        if not user.must_change_password:
            raise AuthenticationError("User is not required to change password")
        
        # Validate new password strength
        if not self._password_service.is_password_strong(force_change_data.new_password):
            raise WeakPasswordError("Password does not meet security requirements")
        
        # Validate new password is different from current
        if self._password_service.verify_password(force_change_data.new_password, user.hashed_password):
            raise InvalidPasswordError("New password must be different from current password")
        
        # Hash new password
        new_hashed_password = self._password_service.hash_password(force_change_data.new_password)
        
        # Force change password (sets must_change_password to False)
        user.force_change_password(new_hashed_password)
        
        # Revoke all existing refresh tokens except current one for security
        # self._token_service.revoke_all_user_tokens_except_current(user.id)  # TODO: Implement when available
        
        await self._user_repository.update(user)
