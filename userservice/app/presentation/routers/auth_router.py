from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.dependencies import (
    get_login_use_case,
    get_refresh_token_use_case,  # PASO 6: Added
    get_logout_use_case,
    get_validate_token_use_case,
    # get_change_password_use_case
    get_forgot_password_use_case,
    get_reset_password_use_case,
    get_force_change_password_use_case,
)
from app.application.use_cases.auth_use_cases import (
    LoginUseCase,
    RefreshTokenUseCase,  # PASO 6: Added
    LogoutUseCase,
    ValidateTokenUseCase,
    # ChangePasswordUseCase
    ForgotPasswordUseCase,
    ResetPasswordUseCase,
    ForceChangePasswordUseCase,
)
from app.application.dtos.user_dtos import (
    LoginDTO,
    TokenResponseDTO,
    RefreshTokenDTO,  # PASO 6: Added
    ForgotPasswordDTO,
    ResetPasswordDTO,
    ForceChangePasswordDTO,
)
from app.presentation.schemas.user_schemas import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,  # PASO 6: Added
    RefreshTokenResponse,  # PASO 6: Added
    MessageResponse,
    UserResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ForceChangePasswordRequest,
)
from app.presentation.dependencies.auth import get_current_user, get_current_active_user
from app.domain.entities.user_entity import User
from app.domain.exceptions.user_exceptions import (
    AuthenticationError,
    UserNotFoundError,
    InvalidTokenError,
    WeakPasswordError,
    UserInactiveError,
    InvalidPasswordError,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
async def login(
    login_request: LoginRequest,
    login_use_case: Annotated[LoginUseCase, Depends(get_login_use_case)]
):
    """
    Autenticar usuario y obtener tokens de acceso.
    
    - **email**: Email del usuario
    - **password**: Contraseña del usuario
    """
    try:
        login_dto = LoginDTO(
            email=login_request.email,
            password=login_request.password
        )
        result = await login_use_case.execute(login_dto)
        
        return LoginResponse(
            access_token=result.access_token,
            token_type=result.token_type,
            expires_in=result.expires_in,
            user=result.user
        )
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
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


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Obtener el perfil del usuario autenticado.
    """
    from app.application.dtos.user_dtos import UserResponseDTO
    
    return UserResponseDTO(
        id=current_user.id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email.value,
        document_number=current_user.document_number.value,
        document_type=current_user.document_number.document_type.value,
        role=current_user.role.value,
        is_active=current_user.is_active,
        must_change_password=current_user.must_change_password,
        phone=current_user.phone,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        last_login_at=current_user.last_login_at
    )


@router.post("/validate", response_model=UserResponse)
async def validate_token(
    validate_use_case: Annotated[ValidateTokenUseCase, Depends(get_validate_token_use_case)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Validar token y obtener información del usuario.
    """
    return UserResponseDTO(
        id=current_user.id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email.value,
        document_number=current_user.document_number.value,
        document_type=current_user.document_number.document_type.value,
        role=current_user.role.value,
        is_active=current_user.is_active,
        must_change_password=current_user.must_change_password,
        phone=current_user.phone,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        last_login_at=current_user.last_login_at
    )


# PASO 6: Refresh token endpoint for HU-BE-003
@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    refresh_token_use_case: Annotated[RefreshTokenUseCase, Depends(get_refresh_token_use_case)]
):
    """
    Refresh access token using valid refresh token.
    
    - **refresh_token**: Valid refresh token to exchange for new access token
    """
    try:
        refresh_dto = RefreshTokenDTO(
            refresh_token=request.refresh_token
        )
        result = await refresh_token_use_case.execute(refresh_dto)
        
        return RefreshTokenResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            token_type=result.token_type,
            expires_in=result.expires_in
        )
    except InvalidTokenError as e:
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
    except UserInactiveError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )


# @router.post("/logout", response_model=MessageResponse)
# async def logout(
#     current_user: Annotated[User, Depends(get_current_user)],
#     logout_use_case: Annotated[LogoutUseCase, Depends(get_logout_use_case)]
# ):
#     """
#     Cerrar sesión del usuario actual.
#     """
#     try:
#         await logout_use_case.execute(current_user.id)
#         return MessageResponse(message="Sesión cerrada exitosamente")
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Error interno del servidor"
#         )


# @router.put("/change-password", response_model=MessageResponse)
# async def change_password(
#     request: ChangePasswordRequest,
#     current_user: Annotated[User, Depends(get_current_user)],
#     change_password_use_case: Annotated[ChangePasswordUseCase, Depends(get_change_password_use_case)]
# ):
#     """
#     Cambiar contraseña del usuario actual.
#     
#     - **current_password**: Contraseña actual
#     - **new_password**: Nueva contraseña
#     """
#     try:
#         dto = ChangePasswordRequestDTO(
#             user_id=current_user.id,
#             current_password=request.current_password,
#             new_password=request.new_password
#         )
#         await change_password_use_case.execute(dto)
#         return MessageResponse(message="Contraseña cambiada exitosamente")
#     except InvalidCredentialsError as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e)
#         )
#     except WeakPasswordError as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e)
#         )
#     except UserNotFoundError as e:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=str(e)
#         )


# PASO 5: Endpoints para funcionalidades de autenticación críticas

@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    request: ForgotPasswordRequest,
    forgot_password_use_case: Annotated[ForgotPasswordUseCase, Depends(get_forgot_password_use_case)]
):
    """
    Solicitar restablecimiento de contraseña (HU-BE-005).
    
    - **email**: Email del usuario para enviar instrucciones de restablecimiento
    """
    try:
        dto = ForgotPasswordDTO(email=request.email)
        await forgot_password_use_case.execute(dto)
        return MessageResponse(
            message="Si el email existe en nuestro sistema, recibirás instrucciones para restablecer tu contraseña"
        )
    except Exception:
        # Por seguridad, siempre retornamos el mismo mensaje
        return MessageResponse(
            message="Si el email existe en nuestro sistema, recibirás instrucciones para restablecer tu contraseña"
        )


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    request: ResetPasswordRequest,
    reset_password_use_case: Annotated[ResetPasswordUseCase, Depends(get_reset_password_use_case)]
):
    """
    Restablecer contraseña con token (HU-BE-006).
    
    - **token**: Token de restablecimiento recibido por email
    - **new_password**: Nueva contraseña que cumple requisitos de seguridad
    """
    try:
        dto = ResetPasswordDTO(
            token=request.token,
            new_password=request.new_password
        )
        await reset_password_use_case.execute(dto)
        return MessageResponse(message="Contraseña restablecida exitosamente")
    
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except WeakPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/force-change-password", response_model=MessageResponse)
async def force_change_password(
    request: ForceChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    force_change_password_use_case: Annotated[ForceChangePasswordUseCase, Depends(get_force_change_password_use_case)]
):
    """
    Cambio forzado de contraseña (HU-BE-007).
    Requerido para usuarios con flag must_change_password = true.
    
    - **new_password**: Nueva contraseña que cumple requisitos de seguridad
    """
    try:
        dto = ForceChangePasswordDTO(
            user_id=current_user.id,
            new_password=request.new_password
        )
        await force_change_password_use_case.execute(dto)
        return MessageResponse(message="Contraseña cambiada exitosamente")
    
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except UserInactiveError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except InvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except WeakPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
