"""Use cases module for application layer."""

from .auth_use_cases import (
    LoginUseCase,
    LogoutUseCase,
    ValidateTokenUseCase,
)

from .user_use_cases import (
    CreateUserUseCase,
    GetUserByIdUseCase,
    UpdateUserUseCase,
    ChangePasswordUseCase,
    ActivateUserUseCase,
    DeactivateUserUseCase,
    ListUsersUseCase,
    # PASO 4: Nuevos casos de uso para administración avanzada
    GetUserDetailUseCase,
    AdminUpdateUserUseCase,
    DeleteUserUseCase,
    BulkUploadUsersUseCase,
)

__all__ = [
    # Auth use cases
    "LoginUseCase",
    "LogoutUseCase",
    "ValidateTokenUseCase",
    # User use cases
    "CreateUserUseCase",
    "GetUserByIdUseCase",
    "UpdateUserUseCase",
    "ChangePasswordUseCase",
    "ActivateUserUseCase",
    "DeactivateUserUseCase",
    "ListUsersUseCase",
    # PASO 4: Casos de uso de administración avanzada
    "GetUserDetailUseCase",
    "AdminUpdateUserUseCase",
    "DeleteUserUseCase",
    "BulkUploadUsersUseCase",
]
