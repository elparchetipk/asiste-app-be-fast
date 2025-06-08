from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated, Optional
from uuid import UUID

from app.dependencies import (
    get_create_user_use_case,
    get_get_user_use_case,
    get_update_user_use_case,
    get_delete_user_use_case,
    get_list_users_use_case,
    get_get_user_profile_use_case,
    get_update_user_profile_use_case
)
from app.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
    ListUsersUseCase,
    GetUserProfileUseCase,
    UpdateUserProfileUseCase
)
from app.application.dtos.user_dtos import (
    CreateUserRequestDTO,
    UpdateUserRequestDTO,
    UserFiltersDTO,
    UpdateUserProfileRequestDTO
)
from app.presentation.schemas.user_schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
    UserListResponse,
    MessageResponse,
    UpdateUserProfileRequest
)
from app.presentation.dependencies.auth import (
    get_current_user,
    require_role,
    get_current_active_user
)
from app.domain.entities.user_entity import User
from app.domain.value_objects.user_role import UserRole
from app.domain.exceptions.user_exceptions import (
    UserNotFoundError,
    EmailAlreadyExistsError,
    DocumentAlreadyExistsError,
    InvalidDocumentError,
    InvalidEmailError
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    current_user: Annotated[User, Depends(require_role([UserRole.ADMIN, UserRole.ADMINISTRATIVE]))],
    create_user_use_case: Annotated[CreateUserUseCase, Depends(get_create_user_use_case)]
):
    """
    Crear un nuevo usuario.
    
    Requiere rol ADMIN o ADMINISTRATIVE.
    """
    try:
        dto = CreateUserRequestDTO(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            document_type=request.document_type,
            document_number=request.document_number,
            phone=request.phone,
            role=request.role,
            password=request.password
        )
        user = await create_user_use_case.execute(dto)
        return UserResponse.from_entity(user)
    except EmailAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except DocumentAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except (InvalidDocumentError, InvalidEmailError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=UserListResponse)
async def list_users(
    current_user: Annotated[User, Depends(require_role([UserRole.ADMIN, UserRole.ADMINISTRATIVE]))],
    list_users_use_case: Annotated[ListUsersUseCase, Depends(get_list_users_use_case)],
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    role: Optional[UserRole] = Query(None, description="Filtrar por rol"),
    search: Optional[str] = Query(None, description="Buscar por nombre o email"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo")
):
    """
    Listar usuarios con paginación y filtros.
    
    Requiere rol ADMIN o ADMINISTRATIVE.
    """
    try:
        filters = UserFiltersDTO(
            role=role,
            search=search,
            is_active=is_active,
            page=page,
            page_size=page_size
        )
        result = await list_users_use_case.execute(filters)
        
        return UserListResponse(
            users=[UserResponse.from_entity(user) for user in result.users],
            total=result.total,
            page=result.page,
            page_size=result.page_size,
            total_pages=result.total_pages
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)],
    get_profile_use_case: Annotated[GetUserProfileUseCase, Depends(get_get_user_profile_use_case)]
):
    """
    Obtener perfil del usuario actual.
    """
    try:
        user = await get_profile_use_case.execute(current_user.id)
        return UserResponse.from_entity(user)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    request: UpdateUserProfileRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    update_profile_use_case: Annotated[UpdateUserProfileUseCase, Depends(get_update_user_profile_use_case)]
):
    """
    Actualizar perfil del usuario actual.
    """
    try:
        dto = UpdateUserProfileRequestDTO(
            user_id=current_user.id,
            first_name=request.first_name,
            last_name=request.last_name,
            phone=request.phone
        )
        user = await update_profile_use_case.execute(dto)
        return UserResponse.from_entity(user)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    current_user: Annotated[User, Depends(require_role([UserRole.ADMIN, UserRole.ADMINISTRATIVE]))],
    get_user_use_case: Annotated[GetUserUseCase, Depends(get_get_user_use_case)]
):
    """
    Obtener usuario por ID.
    
    Requiere rol ADMIN o ADMINISTRATIVE.
    """
    try:
        user = await get_user_use_case.execute(user_id)
        return UserResponse.from_entity(user)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    request: UpdateUserRequest,
    current_user: Annotated[User, Depends(require_role([UserRole.ADMIN, UserRole.ADMINISTRATIVE]))],
    update_user_use_case: Annotated[UpdateUserUseCase, Depends(get_update_user_use_case)]
):
    """
    Actualizar usuario por ID.
    
    Requiere rol ADMIN o ADMINISTRATIVE.
    """
    try:
        dto = UpdateUserRequestDTO(
            user_id=user_id,
            first_name=request.first_name,
            last_name=request.last_name,
            phone=request.phone,
            role=request.role,
            is_active=request.is_active
        )
        user = await update_user_use_case.execute(dto)
        return UserResponse.from_entity(user)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: UUID,
    current_user: Annotated[User, Depends(require_role([UserRole.ADMIN]))],
    delete_user_use_case: Annotated[DeleteUserUseCase, Depends(get_delete_user_use_case)]
):
    """
    Eliminar usuario por ID (soft delete).
    
    Requiere rol ADMIN.
    """
    try:
        await delete_user_use_case.execute(user_id)
        return MessageResponse(message="Usuario eliminado exitosamente")
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
