"""Router for admin user management endpoints (PASO 4)."""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Annotated
from uuid import UUID

from app.dependencies import (
    get_get_user_detail_use_case,
    get_admin_update_user_use_case,
    get_delete_user_use_case,
    get_bulk_upload_users_use_case,
)
from app.presentation.dependencies.auth import get_admin_user
from app.domain.entities.user_entity import User
from app.application.use_cases.user_use_cases import (
    GetUserDetailUseCase,
    AdminUpdateUserUseCase,
    DeleteUserUseCase,
    BulkUploadUsersUseCase,
)
from app.application.dtos.user_dtos import (
    AdminUpdateUserDTO,
)
from app.presentation.schemas.user_schemas import (
    AdminUpdateUserRequest,
    UserDetailResponse,
    DeleteUserResponse,
    BulkUploadRequest,
    BulkUploadResponse,
    MessageResponse,
)

router = APIRouter(prefix="/admin/users", tags=["Admin - User Management"])


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user_detail(
    user_id: UUID,
    get_user_detail_use_case: Annotated[GetUserDetailUseCase, Depends(get_get_user_detail_use_case)],
    current_user: Annotated[User, Depends(get_admin_user)]
):
    """
    Obtener información detallada de un usuario específico.
    Requiere permisos de ADMIN.
    
    HU-BE-013: Obtener Usuario Específico (Admin)
    """
    try:
        user_detail = await get_user_detail_use_case.execute(user_id)
        
        # Generate HATEOAS links
        links = {
            "self": f"/api/v1/admin/users/{user_id}",
            "update": f"/api/v1/admin/users/{user_id}",
            "delete": f"/api/v1/admin/users/{user_id}",
            "activate": f"/api/v1/users/{user_id}/activate",
            "deactivate": f"/api/v1/users/{user_id}/deactivate",
        }
        
        return UserDetailResponse(
            id=user_detail.id,
            first_name=user_detail.first_name,
            last_name=user_detail.last_name,
            email=user_detail.email,
            document_number=user_detail.document_number,
            document_type=user_detail.document_type,
            phone=user_detail.phone,
            role=user_detail.role,
            is_active=user_detail.is_active,
            must_change_password=user_detail.must_change_password,
            created_at=user_detail.created_at,
            updated_at=user_detail.updated_at,
            last_login_at=user_detail.last_login_at,
            deleted_at=user_detail.deleted_at,
            links=links,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{user_id}", response_model=UserDetailResponse)
async def update_user(
    user_id: UUID,
    update_request: AdminUpdateUserRequest,
    admin_update_user_use_case: Annotated[AdminUpdateUserUseCase, Depends(get_admin_update_user_use_case)],
    current_user: Annotated[User, Depends(get_admin_user)]
):
    """
    Actualizar información de un usuario.
    Requiere permisos de ADMIN.
    
    HU-BE-014: Actualizar Usuario (Admin)
    """
    try:
        update_dto = AdminUpdateUserDTO(
            first_name=update_request.first_name,
            last_name=update_request.last_name,
            email=update_request.email,
            document_number=update_request.document_number,
            document_type=update_request.document_type,
            phone=update_request.phone,
            role=update_request.role,
            is_active=update_request.is_active,
            must_change_password=update_request.must_change_password,
        )
        
        updated_user = await admin_update_user_use_case.execute(user_id, update_dto)
        
        # Generate HATEOAS links
        links = {
            "self": f"/api/v1/admin/users/{user_id}",
            "update": f"/api/v1/admin/users/{user_id}",
            "delete": f"/api/v1/admin/users/{user_id}",
            "activate": f"/api/v1/users/{user_id}/activate",
            "deactivate": f"/api/v1/users/{user_id}/deactivate",
        }
        
        return UserDetailResponse(
            id=updated_user.id,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            email=updated_user.email,
            document_number=updated_user.document_number,
            document_type=updated_user.document_type,
            phone=updated_user.phone,
            role=updated_user.role,
            is_active=updated_user.is_active,
            must_change_password=updated_user.must_change_password,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            last_login_at=updated_user.last_login_at,
            deleted_at=updated_user.deleted_at,
            links=links,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}", response_model=DeleteUserResponse)
async def delete_user(
    user_id: UUID,
    delete_user_use_case: Annotated[DeleteUserUseCase, Depends(get_delete_user_use_case)],
    current_user: Annotated[User, Depends(get_admin_user)]
):
    """
    Eliminar (desactivar) un usuario del sistema.
    Realiza soft delete preservando datos históricos.
    Requiere permisos de ADMIN.
    
    HU-BE-015: Eliminar/Desactivar Usuario (Admin)
    """
    try:
        result = await delete_user_use_case.execute(user_id, current_user.id)
        
        return DeleteUserResponse(
            message=result.message,
            user_id=result.user_id,
            deleted_at=result.deleted_at,
        )
        
    except ValueError as e:
        # Handle specific business rule violations (e.g., admin deleting themselves)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/upload", response_model=BulkUploadResponse)
async def bulk_upload_users(
    upload_request: BulkUploadRequest,
    bulk_upload_use_case: Annotated[BulkUploadUsersUseCase, Depends(get_bulk_upload_users_use_case)],
    current_user: Annotated[User, Depends(get_admin_user)]
):
    """
    Carga masiva de usuarios desde archivo CSV.
    Requiere permisos de ADMIN.
    
    HU-BE-016: Carga Masiva de Usuarios (Admin)
    
    Formato CSV esperado:
    first_name,last_name,email,document_number,document_type,role,phone
    Juan,Pérez,juan.perez@example.com,12345678,CC,APPRENTICE,+573001234567
    """
    try:
        result = await bulk_upload_use_case.execute(upload_request.file_content)
        
        return BulkUploadResponse(
            message=result.message,
            total_processed=result.total_processed,
            successful=result.successful,
            failed=result.failed,
            errors=result.errors,
            created_users=result.created_users,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing bulk upload: {str(e)}"
        )


@router.post("/upload-file", response_model=BulkUploadResponse)
async def bulk_upload_users_file(
    bulk_upload_use_case: Annotated[BulkUploadUsersUseCase, Depends(get_bulk_upload_users_use_case)],
    current_user: Annotated[User, Depends(get_admin_user)],
    file: UploadFile = File(..., description="CSV file with user data")
):
    """
    Carga masiva de usuarios desde archivo CSV subido directamente.
    Requiere permisos de ADMIN.
    
    Alternativa para HU-BE-016 que acepta archivos directamente.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only CSV files are allowed"
            )
        
        # Read file content
        content = await file.read()
        csv_content = content.decode('utf-8')
        
        # Process upload
        result = await bulk_upload_use_case.execute(csv_content)
        
        return BulkUploadResponse(
            message=result.message,
            total_processed=result.total_processed,
            successful=result.successful,
            failed=result.failed,
            errors=result.errors,
            created_users=result.created_users,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing file upload: {str(e)}"
        )
