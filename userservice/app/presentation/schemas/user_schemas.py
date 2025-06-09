"""Pydantic schemas for user API endpoints."""

from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.domain.value_objects.user_role import UserRole
from app.domain.value_objects.document_type import DocumentType
from app.domain.entities.user_entity import User


class CreateUserRequest(BaseModel):
    """Schema for creating a new user."""
    
    first_name: str = Field(..., min_length=2, max_length=100, description="User's first name")
    last_name: str = Field(..., min_length=2, max_length=100, description="User's last name")
    email: EmailStr = Field(..., description="User's email address")
    document_number: str = Field(..., min_length=6, max_length=15, description="User's document number")
    document_type: DocumentType = Field(..., description="Type of document")
    password: str = Field(..., min_length=8, max_length=100, description="User's password")
    role: UserRole = Field(..., description="User's role in the system")
    phone: Optional[str] = Field(None, description="User's phone number")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Juan",
                "last_name": "Pérez",
                "email": "juan.perez@example.com",
                "document_number": "12345678",
                "document_type": "CC",
                "password": "SecurePass123!",
                "role": "APPRENTICE",
                "phone": "+573001234567"
            }
        }
    )


class UpdateUserRequest(BaseModel):
    """Schema for updating user information by admin."""
    
    first_name: Optional[str] = Field(None, min_length=2, max_length=100, description="User's first name")
    last_name: Optional[str] = Field(None, min_length=2, max_length=100, description="User's last name")
    phone: Optional[str] = Field(None, description="User's phone number")
    role: Optional[UserRole] = Field(None, description="User's role in the system")
    is_active: Optional[bool] = Field(None, description="Whether the user is active")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Juan Carlos",
                "last_name": "Pérez González",
                "phone": "+573009876543",
                "role": "INSTRUCTOR",
                "is_active": True
            }
        }
    )


class UpdateUserProfileRequest(BaseModel):
    """Schema for updating user profile by user."""
    
    first_name: Optional[str] = Field(None, min_length=2, max_length=100, description="User's first name")
    last_name: Optional[str] = Field(None, min_length=2, max_length=100, description="User's last name")
    phone: Optional[str] = Field(None, description="User's phone number")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Juan Carlos",
                "last_name": "Pérez González",
                "phone": "+573009876543"
            }
        }
    )


class ChangePasswordRequest(BaseModel):
    """Schema for changing user password."""
    
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "current_password": "OldPassword123!",
                "new_password": "NewSecurePass456!"
            }
        }
    )


# PASO 5: Schemas para funcionalidades de autenticación críticas

class ForgotPasswordRequest(BaseModel):
    """Schema for requesting password reset."""
    
    email: EmailStr = Field(..., description="User's email address for password reset")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com"
            }
        }
    )


class ResetPasswordRequest(BaseModel):
    """Schema for resetting password with token (HU-BE-006)."""
    
    token: str = Field(..., min_length=1, description="Password reset token")
    new_password: str = Field(..., min_length=10, max_length=100, description="New secure password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "token": "abc123def456789reset",
                "new_password": "NewSecurePass456!"
            }
        }
    )


class ForceChangePasswordRequest(BaseModel):
    """Schema for forced password change (HU-BE-007)."""
    
    new_password: str = Field(..., min_length=10, max_length=100, description="New secure password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "new_password": "NewSecurePass456!"
            }
        }
    )


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""
    
    refresh_token: str = Field(..., description="Refresh token")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
    )


class UserResponse(BaseModel):
    """Schema for user response data."""
    
    id: UUID = Field(..., description="User's unique identifier")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    email: str = Field(..., description="User's email address")
    document_number: str = Field(..., description="User's document number")
    document_type: str = Field(..., description="Type of document")
    role: str = Field(..., description="User's role in the system")
    is_active: bool = Field(..., description="Whether the user is active")
    must_change_password: bool = Field(..., description="Whether user must change password")
    phone: Optional[str] = Field(None, description="User's phone number")
    created_at: datetime = Field(..., description="When the user was created")
    updated_at: datetime = Field(..., description="When the user was last updated")
    last_login_at: Optional[datetime] = Field(None, description="When the user last logged in")
    
    @property
    def full_name(self) -> str:
        """Get the full name of the user."""
        return f"{self.first_name} {self.last_name}"
    
    @classmethod
    def from_entity(cls, user: User) -> "UserResponse":
        """Create UserResponse from User entity."""
        return cls(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email.value,
            document_number=user.document_number.value,
            document_type=user.document_type.value,
            role=user.role.value,
            is_active=user.is_active,
            must_change_password=user.must_change_password,
            phone=user.phone,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login_at=user.last_login_at
        )
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "first_name": "Juan",
                "last_name": "Pérez",
                "email": "juan.perez@example.com",
                "document_number": "12345678",
                "document_type": "CC",
                "role": "APPRENTICE",
                "is_active": True,
                "must_change_password": False,
                "phone": "+573001234567",
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z",
                "last_login_at": "2024-01-01T15:30:00Z"
            }
        }
    )


class LoginRequest(BaseModel):
    """Schema for user login request."""
    
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, description="User's password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "password123"
            }
        }
    )


class LoginResponse(BaseModel):
    """Schema for authentication token response."""
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Type of token (bearer)")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: UserResponse = Field(..., description="User information")
    refresh_token: Optional[str] = Field(None, description="JWT refresh token (optional)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600,
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "first_name": "Juan",
                    "last_name": "Pérez",
                    "email": "juan.perez@example.com",
                    "document_number": "12345678",
                    "document_type": "CC",
                    "role": "APPRENTICE",
                    "is_active": True,
                    "must_change_password": False,
                    "phone": "+573001234567",
                    "created_at": "2024-01-01T10:00:00Z",
                    "updated_at": "2024-01-01T10:00:00Z",
                    "last_login_at": "2024-01-01T15:30:00Z"
                }
            }
        }
    )


class UserListResponse(BaseModel):
    """Schema for paginated user list response."""
    
    users: List[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of users per page")
    total_pages: int = Field(..., description="Total number of pages")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "users": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "first_name": "Juan",
                        "last_name": "Pérez",
                        "email": "juan.perez@example.com",
                        "document_number": "12345678",
                        "document_type": "CC",
                        "role": "APPRENTICE",
                        "is_active": True,
                        "must_change_password": False,
                        "phone": "+573001234567",
                        "created_at": "2024-01-01T10:00:00Z",
                        "updated_at": "2024-01-01T10:00:00Z",
                        "last_login_at": "2024-01-01T15:30:00Z"
                    }
                ],
                "total": 100,
                "page": 1,
                "page_size": 10,
                "total_pages": 10
            }
        }
    )


class MessageResponse(BaseModel):
    """Schema for simple message responses."""
    
    message: str = Field(..., description="Response message")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Operation completed successfully"
            }
        }
    )


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    
    detail: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "User not found",
                "code": "USER_NOT_FOUND"
            }
        }
    )


class HealthCheckResponse(BaseModel):
    """Schema for health check response."""
    
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Current timestamp")
    version: str = Field(..., description="Service version")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-01T10:00:00Z",
                "version": "1.0.0"
            }
        }
    )


# PASO 4: Schemas para administración avanzada de usuarios

class AdminUpdateUserRequest(BaseModel):
    """Schema for updating any user field by admin (more comprehensive than UpdateUserRequest)."""
    
    first_name: Optional[str] = Field(None, min_length=2, max_length=100, description="User's first name")
    last_name: Optional[str] = Field(None, min_length=2, max_length=100, description="User's last name")
    email: Optional[EmailStr] = Field(None, description="User's email address")
    document_number: Optional[str] = Field(None, min_length=6, max_length=15, description="User's document number")
    document_type: Optional[DocumentType] = Field(None, description="Type of document")
    phone: Optional[str] = Field(None, description="User's phone number")
    role: Optional[UserRole] = Field(None, description="User's role in the system")
    is_active: Optional[bool] = Field(None, description="Whether the user is active")
    must_change_password: Optional[bool] = Field(None, description="Whether user must change password on next login")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Juan Carlos",
                "last_name": "Pérez González",
                "email": "juan.carlos@example.com",
                "role": "INSTRUCTOR",
                "is_active": True,
                "must_change_password": False
            }
        }
    )


class UserDetailResponse(BaseModel):
    """Schema for detailed user information (admin view)."""
    
    id: UUID = Field(..., description="User's unique identifier")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    email: str = Field(..., description="User's email address")
    document_number: str = Field(..., description="User's document number")
    document_type: str = Field(..., description="Type of document")
    phone: Optional[str] = Field(None, description="User's phone number")
    role: str = Field(..., description="User's role in the system")
    is_active: bool = Field(..., description="Whether the user is active")
    must_change_password: bool = Field(..., description="Whether user must change password on next login")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: datetime = Field(..., description="User last update timestamp")
    last_login_at: Optional[datetime] = Field(None, description="User last login timestamp")
    deleted_at: Optional[datetime] = Field(None, description="User deletion timestamp (soft delete)")
    
    # HATEOAS links
    links: dict = Field(..., description="Related operation links")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "first_name": "Juan",
                "last_name": "Pérez",
                "email": "juan.perez@example.com",
                "document_number": "12345678",
                "document_type": "CC",
                "phone": "+573001234567",
                "role": "APPRENTICE",
                "is_active": True,
                "must_change_password": False,
                "created_at": "2024-01-01T09:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z",
                "last_login_at": "2024-01-01T15:30:00Z",
                "deleted_at": None,
                "links": {
                    "self": "/api/v1/admin/users/123e4567-e89b-12d3-a456-426614174000",
                    "update": "/api/v1/admin/users/123e4567-e89b-12d3-a456-426614174000",
                    "delete": "/api/v1/admin/users/123e4567-e89b-12d3-a456-426614174000",
                    "activate": "/api/v1/users/123e4567-e89b-12d3-a456-426614174000/activate",
                    "deactivate": "/api/v1/users/123e4567-e89b-12d3-a456-426614174000/deactivate"
                }
            }
        }
    )


class BulkUploadRequest(BaseModel):
    """Schema for bulk user upload CSV."""
    
    file_content: str = Field(..., description="Base64 encoded CSV file content")
    filename: str = Field(..., description="Original filename")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "file_content": "Zmlyc3RfbmFtZSxsYXN0X25hbWUsZW1haWwsZG9jdW1lbnRfbnVtYmVyLGRvY3VtZW50X3R5cGUscm9sZSxwaG9uZQpKdWFuLFDDqXJleiwganVhbi5wZXJlekBleGFtcGxlLmNvbSwxMjM0NTY3OCxDQyxBUFBSRU5USUNFLCszNTczMDAxMjM0NTY3",
                "filename": "usuarios.csv"
            }
        }
    )


class BulkUploadResponse(BaseModel):
    """Schema for bulk upload operation result."""
    
    message: str = Field(..., description="Operation summary message")
    total_processed: int = Field(..., description="Total number of rows processed")
    successful: int = Field(..., description="Number of users created successfully")
    failed: int = Field(..., description="Number of rows that failed")
    errors: List[dict] = Field(..., description="Detailed error information for failed rows")
    created_users: List[dict] = Field(..., description="Summary of successfully created users")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Bulk upload completed",
                "total_processed": 10,
                "successful": 8,
                "failed": 2,
                "errors": [
                    {
                        "row": 3,
                        "error": "Email already exists: juan.perez@example.com",
                        "data": {"email": "juan.perez@example.com", "document_number": "12345678"}
                    },
                    {
                        "row": 7,
                        "error": "Invalid email format: invalid-email",
                        "data": {"email": "invalid-email", "document_number": "87654321"}
                    }
                ],
                "created_users": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "email": "maria.garcia@example.com",
                        "document_number": "98765432",
                        "role": "INSTRUCTOR"
                    }
                ]
            }
        }
    )


class DeleteUserResponse(BaseModel):
    """Schema for user deletion response."""
    
    message: str = Field(..., description="Deletion confirmation message")
    user_id: UUID = Field(..., description="ID of the deleted user")
    deleted_at: datetime = Field(..., description="Timestamp when user was deleted")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "User successfully deactivated",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "deleted_at": "2024-01-01T16:00:00Z"
            }
        }
    )
