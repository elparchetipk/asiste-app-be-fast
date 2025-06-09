"""DTOs module for application layer."""

from .user_dtos import (
    CreateUserDTO,
    UpdateUserDTO,
    ChangePasswordDTO,
    UserResponseDTO,
    LoginDTO,
    TokenResponseDTO,
    UserListDTO,
    UserFilterDTO,
    # PASO 4: Admin DTOs
    AdminUpdateUserDTO,
    UserDetailDTO,
    BulkUploadUserDTO,
    BulkUploadResultDTO,
    DeleteUserResultDTO,
    # PASO 5: Auth Critical DTOs
    ForgotPasswordDTO,
    ResetPasswordDTO,
    ForceChangePasswordDTO,
)

__all__ = [
    "CreateUserDTO",
    "UpdateUserDTO",
    "ChangePasswordDTO",
    "UserResponseDTO",
    "LoginDTO",
    "TokenResponseDTO",
    "UserListDTO",
    "UserFilterDTO",
    # PASO 4: Admin DTOs
    "AdminUpdateUserDTO",
    "UserDetailDTO",
    "BulkUploadUserDTO",
    "BulkUploadResultDTO",
    "DeleteUserResultDTO",
    # PASO 5: Auth Critical DTOs
    "ForgotPasswordDTO",
    "ResetPasswordDTO",
    "ForceChangePasswordDTO",
]
