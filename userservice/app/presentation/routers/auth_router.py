from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.dependencies import (
    get_login_use_case,
    get_refresh_token_use_case,
    get_logout_use_case,
    get_change_password_use_case
)
from app.application.use_cases.auth_use_cases import (
    LoginUseCase,
    RefreshTokenUseCase,
    LogoutUseCase,
    ChangePasswordUseCase
)
from app.application.dtos.user_dtos import (
    LoginResponseDTO,
    RefreshTokenRequestDTO,
    ChangePasswordRequestDTO
)
from app.presentation.schemas.user_schemas import (
    LoginResponse,
    RefreshTokenRequest,
    ChangePasswordRequest,
    MessageResponse
)
from app.presentation.dependencies.auth import get_current_user
from app.domain.entities.user_entity import User
from app.domain.exceptions.user_exceptions import (
    InvalidCredentialsError,
    UserNotFoundError,
    InvalidTokenError,
    WeakPasswordError
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    login_use_case: Annotated[LoginUseCase, Depends(get_login_use_case)]
):
    """
    Autenticar usuario y obtener tokens de acceso y refresh.
    
    - **username**: Email del usuario
    - **password**: Contraseña del usuario
    """
    try:
        result = await login_use_case.execute(form_data.username, form_data.password)
        return LoginResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            token_type=result.token_type,
            expires_in=result.expires_in,
            user=result.user
        )
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    refresh_use_case: Annotated[RefreshTokenUseCase, Depends(get_refresh_token_use_case)]
):
    """
    Renovar token de acceso usando el refresh token.
    
    - **refresh_token**: Token de refresh válido
    """
    try:
        dto = RefreshTokenRequestDTO(refresh_token=request.refresh_token)
        result = await refresh_use_case.execute(dto)
        return LoginResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            token_type=result.token_type,
            expires_in=result.expires_in,
            user=result.user
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: Annotated[User, Depends(get_current_user)],
    logout_use_case: Annotated[LogoutUseCase, Depends(get_logout_use_case)]
):
    """
    Cerrar sesión del usuario actual.
    """
    try:
        await logout_use_case.execute(current_user.id)
        return MessageResponse(message="Sesión cerrada exitosamente")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.put("/change-password", response_model=MessageResponse)
async def change_password(
    request: ChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    change_password_use_case: Annotated[ChangePasswordUseCase, Depends(get_change_password_use_case)]
):
    """
    Cambiar contraseña del usuario actual.
    
    - **current_password**: Contraseña actual
    - **new_password**: Nueva contraseña
    """
    try:
        dto = ChangePasswordRequestDTO(
            user_id=current_user.id,
            current_password=request.current_password,
            new_password=request.new_password
        )
        await change_password_use_case.execute(dto)
        return MessageResponse(message="Contraseña cambiada exitosamente")
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except WeakPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
