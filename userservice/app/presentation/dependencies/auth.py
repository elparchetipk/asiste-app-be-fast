"""Authentication dependencies for FastAPI endpoints."""

from typing import Annotated, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID

from app.domain.entities.user_entity import User
from app.domain.value_objects.user_role import UserRole
from app.domain.exceptions.user_exceptions import (
    InvalidTokenError,
    UserNotFoundError,
    UserDomainException
)
from app.dependencies import get_token_service, get_user_repository
from app.application.interfaces.token_service_interface import TokenServiceInterface
from app.domain.repositories.user_repository_interface import UserRepositoryInterface

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    token_service: Annotated[TokenServiceInterface, Depends(get_token_service)],
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> User:
    """Dependency to get current authenticated user."""
    try:
        # Validar y decodificar el token
        payload = token_service.decode_token(credentials.credentials)
        user_id = UUID(payload.get("sub"))
        
        # Obtener el usuario de la base de datos
        user = await user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error de autenticación",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """Dependency to get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user


def require_role(required_roles: List[UserRole]):
    """Dependency factory to require specific roles."""
    def role_checker(
        current_user: Annotated[User, Depends(get_current_active_user)]
    ) -> User:
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permisos insuficientes. Roles requeridos: {[role.value for role in required_roles]}"
            )
        return current_user
    return role_checker


# Role-specific dependencies
async def get_admin_user(
    current_user: Annotated[User, Depends(require_role([UserRole.ADMIN]))]
) -> User:
    """Dependency to get admin user."""
    return current_user


async def get_instructor_or_admin_user(
    current_user: Annotated[User, Depends(require_role([UserRole.INSTRUCTOR, UserRole.ADMIN]))]
) -> User:
    """Dependency to get instructor or admin user."""
    return current_user


async def get_administrative_or_admin_user(
    current_user: Annotated[User, Depends(require_role([UserRole.ADMINISTRATIVE, UserRole.ADMIN]))]
) -> User:
    """Dependency to get administrative or admin user."""
    return current_user


async def get_any_authenticated_user(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """Dependency to get any authenticated active user."""
    return current_user
