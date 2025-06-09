"""User DTOs for application layer."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from ...domain import UserRole, DocumentType


@dataclass(frozen=True)
class CreateUserDTO:
    """DTO for creating a new user."""
    
    first_name: str
    last_name: str
    email: str
    document_number: str
    document_type: DocumentType
    password: str
    role: UserRole


@dataclass(frozen=True)
class UpdateUserDTO:
    """DTO for updating user information."""
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


@dataclass(frozen=True)
class ChangePasswordDTO:
    """DTO for changing user password."""
    
    current_password: str
    new_password: str


@dataclass(frozen=True)
class UserResponseDTO:
    """DTO for user response data."""
    
    id: UUID
    first_name: str
    last_name: str
    email: str
    document_number: str
    document_type: str
    role: str
    is_active: bool
    must_change_password: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]
    phone: Optional[str] = None  # PASO 4: Additional user field
    
    @property
    def full_name(self) -> str:
        """Get the full name of the user."""
        return f"{self.first_name} {self.last_name}"


@dataclass(frozen=True)
class LoginDTO:
    """DTO for user login."""
    
    email: str
    password: str


@dataclass(frozen=True)
class TokenResponseDTO:
    """DTO for authentication token response."""
    
    access_token: str
    token_type: str
    expires_in: int
    user: UserResponseDTO


@dataclass
class RefreshTokenDTO:
    """DTO for token refresh request (HU-BE-003)."""
    refresh_token: str


@dataclass
class RefreshTokenResponseDTO:
    """DTO for token refresh response (HU-BE-003)."""
    access_token: str
    token_type: str
    expires_in: int


@dataclass(frozen=True)
class UserListDTO:
    """DTO for paginated user list."""
    
    users: list[UserResponseDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass(frozen=True)
class UserFilterDTO:
    """DTO for user filtering parameters."""
    
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    search_term: Optional[str] = None  # Search in name, email, document
    document_type: Optional[DocumentType] = None


# PASO 5: DTOs para funcionalidades de autenticación críticas

@dataclass(frozen=True)
class ForgotPasswordDTO:
    """DTO for requesting password reset."""
    
    email: str


@dataclass(frozen=True)
class ResetPasswordDTO:
    """DTO for resetting password with token (HU-BE-006)."""
    
    token: str
    new_password: str


@dataclass(frozen=True)
class ForceChangePasswordDTO:
    """DTO for forced password change (HU-BE-007)."""
    
    user_id: UUID
    new_password: str


# PASO 4: DTOs para administración avanzada de usuarios

@dataclass(frozen=True)
class AdminUpdateUserDTO:
    """DTO for admin user update with all possible fields."""
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    document_number: Optional[str] = None
    document_type: Optional[DocumentType] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    must_change_password: Optional[bool] = None


@dataclass(frozen=True)
class UserDetailDTO:
    """DTO for detailed user information (admin view)."""
    
    id: UUID
    first_name: str
    last_name: str
    email: str
    document_number: str
    document_type: str
    phone: Optional[str]
    role: str
    is_active: bool
    must_change_password: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    @property
    def full_name(self) -> str:
        """Get the full name of the user."""
        return f"{self.first_name} {self.last_name}"


@dataclass(frozen=True)
class BulkUploadUserDTO:
    """DTO for individual user in bulk upload."""
    
    first_name: str
    last_name: str
    email: str
    document_number: str
    document_type: DocumentType
    role: UserRole
    phone: Optional[str] = None


@dataclass(frozen=True)
class BulkUploadResultDTO:
    """DTO for bulk upload operation result."""
    
    total_processed: int
    successful: int
    failed: int
    errors: list[dict]
    created_users: list[dict]
    
    @property
    def message(self) -> str:
        """Generate summary message."""
        return f"Bulk upload completed: {self.successful}/{self.total_processed} users created successfully"


@dataclass(frozen=True)
class DeleteUserResultDTO:
    """DTO for user deletion result."""
    
    user_id: UUID
    deleted_at: datetime
    message: str = "User successfully deactivated"
