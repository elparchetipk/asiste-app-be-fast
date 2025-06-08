"""Domain exceptions for User entity."""

from typing import Optional


class UserDomainException(Exception):
    """Base exception for user domain operations."""
    
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(UserDomainException):
    """Raised when a user is not found."""
    
    def __init__(self, user_id: Optional[str] = None, email: Optional[str] = None, document_number: Optional[str] = None) -> None:
        if user_id:
            message = f"User with ID {user_id} not found"
        elif email:
            message = f"User with email {email} not found"
        elif document_number:
            message = f"User with document number {document_number} not found"
        else:
            message = "User not found"
        super().__init__(message)


class UserAlreadyExistsError(UserDomainException):
    """Raised when attempting to create a user that already exists."""
    
    def __init__(self, email: Optional[str] = None, document_number: Optional[str] = None) -> None:
        if email and document_number:
            message = f"User with email {email} or document number {document_number} already exists"
        elif email:
            message = f"User with email {email} already exists"
        elif document_number:
            message = f"User with document number {document_number} already exists"
        else:
            message = "User already exists"
        super().__init__(message)


class InvalidUserDataError(UserDomainException):
    """Raised when user data is invalid."""
    pass


class UserNotActiveError(UserDomainException):
    """Raised when attempting operations on inactive user."""
    
    def __init__(self, user_id: str) -> None:
        super().__init__(f"User {user_id} is not active")


class InvalidPasswordError(UserDomainException):
    """Raised when password validation fails."""
    pass


class UserOperationNotAllowedError(UserDomainException):
    """Raised when a user operation is not allowed."""
    pass