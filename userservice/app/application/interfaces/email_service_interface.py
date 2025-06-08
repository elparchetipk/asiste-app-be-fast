"""Email service interface for application layer."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class EmailServiceInterface(ABC):
    """Interface for email operations."""
    
    @abstractmethod
    async def send_welcome_email(self, to_email: str, user_name: str, temporary_password: str) -> bool:
        """Send welcome email with temporary password."""
        pass
    
    @abstractmethod
    async def send_password_reset_email(self, to_email: str, user_name: str, reset_token: str) -> bool:
        """Send password reset email."""
        pass
    
    @abstractmethod
    async def send_password_changed_notification(self, to_email: str, user_name: str) -> bool:
        """Send notification that password was changed."""
        pass
    
    @abstractmethod
    async def send_account_activation_email(self, to_email: str, user_name: str, activation_token: str) -> bool:
        """Send account activation email."""
        pass
    
    @abstractmethod
    async def send_account_deactivation_notification(self, to_email: str, user_name: str) -> bool:
        """Send notification that account was deactivated."""
        pass
    
    @abstractmethod
    async def send_custom_email(self, to_email: str, subject: str, template: str, context: Dict[str, Any]) -> bool:
        """Send custom email using template."""
        pass
