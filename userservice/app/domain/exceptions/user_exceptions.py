"""Domain exceptions for User entity."""

from typing import Optional


class UserDomainException(Exception):
    """Base exception for user domain errors."""
    
    def __init__(self, message: str, details: Optional[str] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class UserNotFoundError(UserDomainException):
    """Raised when a user is not found."""
    
    def __init__(self, identifier: str, identifier_type: str = "id"):
        message = f"User not found with {identifier_type}: {identifier}"
        super().__init__(message)


class UserAlreadyExistsError(UserDomainException):
    """Raised when trying to create a user that already exists."""
    
    def __init__(self, field: str, value: str):
        message = f"User already exists with {field}: {value}"
        super().__init__(message)


class InvalidUserDataError(UserDomainException):
    """Raised when user data is invalid."""
    
    def __init__(self, field: str, reason: str):
        message = f"Invalid {field}: {reason}"
        super().__init__(message)


class UserInactiveError(UserDomainException):
    """Raised when trying to perform operations on inactive user."""
    
    def __init__(self, user_id: str):
        message = f"User {user_id} is inactive"
        super().__init__(message)


class InvalidPasswordError(UserDomainException):
    """Raised when password is invalid."""
    
    def __init__(self, reason: str = "Password does not meet requirements"):
        super().__init__(reason)


class AuthenticationError(UserDomainException):
    """Raised when authentication fails."""
    
    def __init__(self, reason: str = "Invalid credentials"):
        super().__init__(reason)


class AuthorizationError(UserDomainException):
    """Raised when user lacks required permissions."""
    
    def __init__(self, action: str, role: str):
        message = f"User with role '{role}' is not authorized to perform action: {action}"
        super().__init__(message)


class UserSessionError(UserDomainException):
    """Raised when user session is invalid or expired."""
    
    def __init__(self, reason: str = "Invalid or expired session"):
        super().__init__(reason)


class InvalidTokenError(UserDomainException):
    """Raised when a token is invalid or expired."""
    
    def __init__(self, reason: str = "Invalid or expired token"):
        super().__init__(reason)


class EmailAlreadyExistsError(UserDomainException):
    """Raised when trying to create a user with an email that already exists."""
    
    def __init__(self, email: str):
        message = f"User with email '{email}' already exists"
        super().__init__(message)


class DocumentAlreadyExistsError(UserDomainException):
    """Raised when trying to create a user with a document that already exists."""
    
    def __init__(self, document_number: str):
        message = f"User with document number '{document_number}' already exists"
        super().__init__(message)


class InvalidCredentialsError(UserDomainException):
    """Raised when login credentials are invalid."""
    
    def __init__(self, reason: str = "Invalid email or password"):
        super().__init__(reason)


class WeakPasswordError(UserDomainException):
    """Raised when password doesn't meet security requirements."""
    
    def __init__(self, reason: str = "Password is too weak"):
        super().__init__(reason)