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
]
