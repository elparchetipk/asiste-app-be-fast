"""Dependency injection configuration for the application."""

from functools import lru_cache
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.config.database import get_db_session
from app.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.infrastructure.adapters.bcrypt_password_service import BcryptPasswordService
from app.infrastructure.adapters.jwt_token_service import JWTTokenService
from app.infrastructure.adapters.smtp_email_service import SMTPEmailService

from app.application.interfaces.password_service_interface import PasswordServiceInterface
from app.application.interfaces.token_service_interface import TokenServiceInterface
from app.application.interfaces.email_service_interface import EmailServiceInterface
from app.domain.repositories.user_repository_interface import UserRepositoryInterface

from app.application.use_cases.auth_use_cases import (
    LoginUseCase,
    RefreshTokenUseCase,
    LogoutUseCase,
    ChangePasswordUseCase
)
from app.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
    ListUsersUseCase,
    GetUserProfileUseCase,
    UpdateUserProfileUseCase
)


# Repository dependencies
async def get_user_repository(
    session: AsyncSession = Depends(get_db_session)
) -> UserRepositoryInterface:
    """Get user repository instance."""
    return SQLAlchemyUserRepository(session)


# Service dependencies
@lru_cache()
def get_password_service() -> PasswordServiceInterface:
    """Get password service instance."""
    return BcryptPasswordService()


@lru_cache()
def get_token_service() -> TokenServiceInterface:
    """Get token service instance."""
    return JWTTokenService()


@lru_cache()
def get_email_service() -> EmailServiceInterface:
    """Get email service instance."""
    return SMTPEmailService()


# Use case dependencies - Authentication
def get_login_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    password_service: PasswordServiceInterface = Depends(get_password_service),
    token_service: TokenServiceInterface = Depends(get_token_service)
) -> LoginUseCase:
    """Get login use case instance."""
    return LoginUseCase(user_repository, password_service, token_service)


def get_refresh_token_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    token_service: TokenServiceInterface = Depends(get_token_service)
) -> RefreshTokenUseCase:
    """Get refresh token use case instance."""
    return RefreshTokenUseCase(user_repository, token_service)


def get_logout_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    token_service: TokenServiceInterface = Depends(get_token_service)
) -> LogoutUseCase:
    """Get logout use case instance."""
    return LogoutUseCase(user_repository, token_service)


def get_change_password_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    password_service: PasswordServiceInterface = Depends(get_password_service)
) -> ChangePasswordUseCase:
    """Get change password use case instance."""
    return ChangePasswordUseCase(user_repository, password_service)


# Use case dependencies - User Management
def get_create_user_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository),
    password_service: PasswordServiceInterface = Depends(get_password_service),
    email_service: EmailServiceInterface = Depends(get_email_service)
) -> CreateUserUseCase:
    """Get create user use case instance."""
    return CreateUserUseCase(user_repository, password_service, email_service)


def get_get_user_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> GetUserUseCase:
    """Get get user use case instance."""
    return GetUserUseCase(user_repository)


def get_update_user_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> UpdateUserUseCase:
    """Get update user use case instance."""
    return UpdateUserUseCase(user_repository)


def get_delete_user_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> DeleteUserUseCase:
    """Get delete user use case instance."""
    return DeleteUserUseCase(user_repository)


def get_list_users_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> ListUsersUseCase:
    """Get list users use case instance."""
    return ListUsersUseCase(user_repository)


def get_get_user_profile_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> GetUserProfileUseCase:
    """Get get user profile use case instance."""
    return GetUserProfileUseCase(user_repository)


def get_update_user_profile_use_case(
    user_repository: UserRepositoryInterface = Depends(get_user_repository)
) -> UpdateUserProfileUseCase:
    """Get update user profile use case instance."""
    return UpdateUserProfileUseCase(user_repository)
