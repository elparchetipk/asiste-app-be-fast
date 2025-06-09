from abc import ABC, abstractmethod
from typing import Optional, List
import uuid
from ..entities.user_entity import User


class UserRepositoryInterface(ABC):
    """
    Repository interface for User entity.
    Defines the contract for user persistence operations.
    """

    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Create a new user in the repository.
        
        Args:
            user: User entity to create
            
        Returns:
            User: The created user with any additional fields populated
            
        Raises:
            UserAlreadyExistsError: If user with email or document already exists
        """
        pass

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """
        Retrieve a user by their ID.
        
        Args:
            user_id: UUID of the user to retrieve
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        
        Args:
            email: Email address to search for
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_by_document_number(self, document_number: str) -> Optional[User]:
        """
        Retrieve a user by their document number.
        
        Args:
            document_number: Document number to search for
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """
        Update an existing user in the repository.
        
        Args:
            user: User entity with updated data
            
        Returns:
            User: The updated user
            
        Raises:
            UserNotFoundError: If user doesn't exist
        """
        pass

    @abstractmethod
    async def delete(self, user_id: uuid.UUID) -> bool:
        """
        Soft delete a user (set is_active to False).
        
        Args:
            user_id: UUID of the user to delete
            
        Returns:
            bool: True if user was deleted, False if not found
        """
        pass

    @abstractmethod
    async def list_users(
        self, 
        skip: int = 0, 
        limit: int = 100,
        role_filter: Optional[str] = None,
        active_only: bool = True,
        search_term: Optional[str] = None
    ) -> List[User]:
        """
        List users with pagination and filtering.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            role_filter: Filter by user role (optional)
            active_only: If True, only return active users
            search_term: Search in name, email, or document (optional)
            
        Returns:
            List[User]: List of users matching the criteria
        """
        pass

    @abstractmethod
    async def count_users(
        self,
        role_filter: Optional[str] = None,
        active_only: bool = True,
        search_term: Optional[str] = None
    ) -> int:
        """
        Count users matching the given criteria.
        
        Args:
            role_filter: Filter by user role (optional)
            active_only: If True, only count active users
            search_term: Search in name, email, or document (optional)
            
        Returns:
            int: Number of users matching the criteria
        """
        pass

    @abstractmethod
    async def exists_by_email(self, email: str, exclude_user_id: Optional[uuid.UUID] = None) -> bool:
        """
        Check if a user with the given email exists.
        
        Args:
            email: Email to check
            exclude_user_id: User ID to exclude from the check (for updates)
            
        Returns:
            bool: True if user exists, False otherwise
        """
        pass

    @abstractmethod
    async def exists_by_document_number(self, document_number: str, exclude_user_id: Optional[uuid.UUID] = None) -> bool:
        """
        Check if a user with the given document number exists.
        
        Args:
            document_number: Document number to check
            exclude_user_id: User ID to exclude from the check (for updates)
            
        Returns:
            bool: True if user exists, False otherwise
        """
        pass

    # PASO 5: Métodos adicionales para funcionalidades de autenticación críticas
    
    @abstractmethod
    async def get_by_reset_token(self, reset_token: str) -> Optional[User]:
        """
        Retrieve a user by their password reset token.
        
        Args:
            reset_token: Password reset token to search for
            
        Returns:
            Optional[User]: User if found and token is valid, None otherwise
        """
        pass