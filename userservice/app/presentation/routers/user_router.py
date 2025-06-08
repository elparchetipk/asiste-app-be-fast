from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated, Optional
from uuid import UUID

from app.dependencies import (
    get_create_user_use_case,
    get_get_user_by_id_use_case,
    get_update_user_use_case,
    get_list_users_use_case,
    get_activate_user_use_case,
    get_deactivate_user_use_case,
    get_change_password_use_case,
)
from app.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    GetUserByIdUseCase,
    UpdateUserUseCase,
    ListUsersUseCase,
    ActivateUserUseCase,
    DeactivateUserUseCase,
    ChangePasswordUseCase,
)
from app.application.dtos.user_dtos import (
    CreateUserDTO,
    UpdateUserDTO,
    UserResponseDTO,
    UserListDTO,
    UserFilterDTO,
    ChangePasswordDTO,
)
from app.presentation.schemas.user_schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
    MessageResponse,
    UserListResponse,
    ChangePasswordRequest,
)

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_request: CreateUserRequest,
    create_user_use_case: Annotated[CreateUserUseCase, Depends(get_create_user_use_case)]
):
    """
    Crear un nuevo usuario en el sistema.
    """
    try:
        user_dto = CreateUserDTO(
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            email=user_request.email,
            document_number=user_request.document_number,
            document_type=user_request.document_type,
            password=user_request.password,
            role=user_request.role
        )
        
        result = await create_user_use_case.execute(user_dto)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=UserListResponse)
async def list_users(
    list_users_use_case: Annotated[ListUsersUseCase, Depends(get_list_users_use_case)],
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Page size"),
    role: Optional[str] = Query(None, description="Filter by role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search_term: Optional[str] = Query(None, description="Search in name, email, document")
):
    """
    Listar usuarios con paginación y filtros.
    """
    try:
        filters = UserFilterDTO(
            role=role,
            is_active=is_active,
            search_term=search_term
        ) if any([role, is_active is not None, search_term]) else None
        
        result = await list_users_use_case.execute(page, page_size, filters)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: UUID,
    get_user_use_case: Annotated[GetUserByIdUseCase, Depends(get_get_user_by_id_use_case)]
):
    """
    Obtener un usuario por su ID.
    """
    try:
        result = await get_user_use_case.execute(user_id)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: UUID,
    activate_user_use_case: Annotated[ActivateUserUseCase, Depends(get_activate_user_use_case)]
):
    """
    Activar un usuario.
    """
    try:
        result = await activate_user_use_case.execute(user_id)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
    user_id: UUID,
    deactivate_user_use_case: Annotated[DeactivateUserUseCase, Depends(get_deactivate_user_use_case)]
):
    """
    Desactivar un usuario.
    """
    try:
        result = await deactivate_user_use_case.execute(user_id)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/{user_id}/change-password", response_model=MessageResponse)
async def change_user_password(
    user_id: UUID,
    password_request: ChangePasswordRequest,
    change_password_use_case: Annotated[ChangePasswordUseCase, Depends(get_change_password_use_case)]
):
    """
    Cambiar la contraseña de un usuario.
    """
    try:
        password_dto = ChangePasswordDTO(
            current_password=password_request.current_password,
            new_password=password_request.new_password
        )
        
        await change_password_use_case.execute(user_id, password_dto)
        return MessageResponse(message="Password changed successfully")
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
