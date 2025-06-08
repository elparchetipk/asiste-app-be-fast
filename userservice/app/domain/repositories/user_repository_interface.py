import uuid
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.user_entity import User

class UserRepositoryInterface(ABC):
    """
    Abstract interface for User repository operations.
    This interface defines the contract that any User repository implementation must fulfill.
    """

    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Create a new user in the repository.
        
        Args:
            user: User entity to be created
            
        Returns:
            User: The created user entity
            
        Raises:
            UserAlreadyExistsException: If user with same email or document already exists
        """
        pass

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """
        Retrieve a user by their ID.
        
        Args:
            user_id: UUID of the user to retrieve
            
        Returns:
            Optional[User]: User entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        
        Args:
            email: Email address of the user
            
        Returns:
            Optional[User]: User entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_by_document_number(self, document_number: str) -> Optional[User]:
        """
        Retrieve a user by their document number.
        
        Args:
            document_number: Document number of the user
            
        Returns:
            Optional[User]: User entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """
        Update an existing user in the repository.
        
        Args:
            user: User entity with updated information
            
        Returns:
            User: The updated user entity
            
        Raises:
            UserNotFoundException: If user doesn't exist
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
        List users with optional filtering and pagination.
        
        Args:
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return
            role_filter: Optional role to filter by
            active_only: If True, only return active users
            search_term: Optional search term for name, email, or document
            
        Returns:
            List[User]: List of user entities matching the criteria
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
            role_filter: Optional role to filter by
            active_only: If True, only count active users
            search_term: Optional search term for name, email, or document
            
        Returns:
            int: Number of users matching the criteria
        """
        pass

    @abstractmethod
    async def exists_by_email(self, email: str, exclude_user_id: Optional[uuid.UUID] = None) -> bool:
        """
        Check if a user with the given email already exists.
        
        Args:
            email: Email address to check
            exclude_user_id: Optional user ID to exclude from the check (for updates)
            
        Returns:
            bool: True if email exists, False otherwise
        """
        pass

    @abstractmethod
    async def exists_by_document_number(self, document_number: str, exclude_user_id: Optional[uuid.UUID] = None) -> bool:
        """
        Check if a user with the given document number already exists.
        
        Args:
            document_number: Document number to check
            exclude_user_id: Optional user ID to exclude from the check (for updates)
            
        Returns:
            bool: True if document number exists, False otherwise
        """
        pass