"""Authentication use cases for user service."""

import secrets
from datetime import datetime, timedelta
from uuid import UUID

from ...domain import (
    UserRepositoryInterface, 
    RefreshTokenRepositoryInterface,  # PASO 6: Added
    User, 
    RefreshToken,  # PASO 6: Added
    Email,
    AuthenticationError,
    UserNotFoundError,
    UserInactiveError,
    InvalidPasswordError,
    WeakPasswordError,
    InvalidTokenError,
)
from ..interfaces import PasswordServiceInterface, TokenServiceInterface, EmailServiceInterface
from ..dtos import (
    LoginDTO, 
    TokenResponseDTO, 
    RefreshTokenDTO,  # PASO 6: Added
    RefreshTokenResponseDTO,  # PASO 6: Added
    UserResponseDTO,
    ForgotPasswordDTO,
    ResetPasswordDTO,
    ForceChangePasswordDTO,
)


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
        email_service: EmailServiceInterface,
    ):
        self._user_repository = user_repository
        self._email_service = email_service
    
    async def execute(self, request_data: ForgotPasswordDTO) -> None:
        """Generate reset token and send email."""
        try:
            email = Email(request_data.email)
        except Exception as e:
            # Por seguridad, no revelamos si el email existe o no
            return
        
        # Get user by email
        user = await self._user_repository.get_by_email(email.value)
        if not user or not user.is_active:
            # Por seguridad, no revelamos si el email existe o no
            return
        
        # Generate secure reset token (24 hours expiration)
        reset_token = secrets.token_urlsafe(32)
        
        # Set reset token in user
        user.set_password_reset_token(reset_token)
        await self._user_repository.update(user)
        
        # Send email with reset link
        await self._email_service.send_password_reset_email(
            email=user.email.value,
            reset_token=reset_token,
            user_name=user.first_name
        )


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
    
    async def execute(self, reset_data: ResetPasswordDTO) -> None:
        """Reset password using valid token."""
        # Find user by reset token
        user = await self._user_repository.get_by_reset_token(reset_data.token)
        if not user:
            raise InvalidTokenError("Invalid or expired reset token")
        
        # Check if token is expired (24 hours)
        if not user.is_reset_token_valid():
            raise InvalidTokenError("Reset token has expired")
        
        # Validate new password
        if not self._password_service.is_password_strong(reset_data.new_password):
            raise WeakPasswordError("Password does not meet security requirements")
        
        # Check if new password is different from current
        if self._password_service.verify_password(reset_data.new_password, user.hashed_password):
            raise InvalidPasswordError("New password must be different from current password")
        
        # Hash new password
        new_hashed_password = self._password_service.hash_password(reset_data.new_password)
        
        # Update password and clear reset token
        user.change_password(new_hashed_password)
        user.clear_password_reset_token()
        await self._user_repository.update(user)
        
        # Invalidate all existing refresh tokens for this user
        self._token_service.revoke_all_user_tokens(user.id)


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
    
    async def execute(self, change_data: ForceChangePasswordDTO) -> None:
        """Force password change for users with must_change_password flag."""
        # Get user
        user = await self._user_repository.get_by_id(change_data.user_id)
        if not user:
            raise UserNotFoundError(str(change_data.user_id))
        
        # Check if user is active
        if not user.is_active:
            raise UserInactiveError(str(user.id))
        
        # Verify must_change_password flag
        if not user.must_change_password:
            raise InvalidPasswordError("User is not required to change password")
        
        # Validate new password
        if not self._password_service.is_password_strong(change_data.new_password):
            raise WeakPasswordError("Password does not meet security requirements")
        
        # Check if new password is different from current
        if self._password_service.verify_password(change_data.new_password, user.hashed_password):
            raise InvalidPasswordError("New password must be different from current password")
        
        # Hash new password
        new_hashed_password = self._password_service.hash_password(change_data.new_password)
        
        # Update password and clear must_change_password flag
        user.change_password(new_hashed_password)
        user.clear_must_change_password()
        await self._user_repository.update(user)
        
        # Invalidate all existing refresh tokens except current one
        # (The user should remain logged in after forced change)
        self._token_service.revoke_all_user_tokens(user.id, exclude_current=True)


# PASO 6: Refresh Token Use Case for HU-BE-003

class RefreshTokenUseCase:
    """Use case for refreshing access tokens (HU-BE-003)."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        refresh_token_repository: RefreshTokenRepositoryInterface,
        token_service: TokenServiceInterface,
    ):
        self._user_repository = user_repository
        self._refresh_token_repository = refresh_token_repository
        self._token_service = token_service
    
    async def execute(self, refresh_data: RefreshTokenDTO) -> RefreshTokenResponseDTO:
        """Refresh access token using valid refresh token."""
        # Get refresh token from repository
        refresh_token = await self._refresh_token_repository.get_by_token(refresh_data.refresh_token)
        if not refresh_token:
            raise InvalidTokenError("Invalid refresh token")
        
        # Validate refresh token
        try:
            refresh_token.validate_for_refresh()
        except InvalidTokenError:
            # Clean up invalid token
            await self._refresh_token_repository.delete(refresh_token.id)
            raise
        
        # Get user
        user = await self._user_repository.get_by_id(refresh_token.user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {refresh_token.user_id}")
        
        # Check if user is still active
        if not user.is_active:
            # Revoke all tokens for inactive user
            await self._refresh_token_repository.revoke_all_user_tokens(user.id)
            raise UserInactiveError(f"User account is inactive: {user.id}")
        
        # Mark token as used
        refresh_token.mark_as_used()
        
        # Create new access token
        access_token = self._token_service.create_access_token(
            user_id=user.id,
            role=user.role.value,
            expires_delta=3600  # 1 hour
        )
        
        # Rotate refresh token (create new one and revoke old one)
        new_refresh_token = refresh_token.rotate()
        await self._refresh_token_repository.save(new_refresh_token)
        
        # Update the used token in repository
        await self._refresh_token_repository.update(refresh_token)
        
        return RefreshTokenResponseDTO(
            access_token=access_token,
            refresh_token=new_refresh_token.token,
            token_type="bearer",
            expires_in=3600,  # 1 hour
        )
