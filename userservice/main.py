"""FastAPI application main module."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime, timezone

from app.infrastructure.config.database import engine, get_db_session, check_database_health
from app.presentation.routers import auth_router, user_router, admin_user_router
from app.presentation.schemas.user_schemas import HealthCheckResponse, ErrorResponse
from app.domain.exceptions.user_exceptions import (
    UserDomainException,
    UserNotFoundError,
    EmailAlreadyExistsError,
    DocumentAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
    WeakPasswordError
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    logger.info("Starting UserService application")
    yield
    # Shutdown
    logger.info("Shutting down UserService application")
    await engine.dispose()


app = FastAPI(
    title="SICORA UserService API",
    description="""
    Microservicio de gestión de usuarios para el Sistema de Información 
    de Coordinación Académica (SICORA) - AsisTE App SENA.
    
    Este servicio implementa Clean Architecture y proporciona:
    - Autenticación y autorización con JWT
    - Gestión completa de usuarios con control de roles
    - Validación de documentos colombianos
    - API RESTful con documentación automática
    """,
    version="1.0.0",
    contact={
        "name": "Equipo de Desarrollo SICORA",
        "email": "dev@sicora.sena.edu.co"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    """Handle user not found exceptions."""
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc), "code": "USER_NOT_FOUND"}
    )


@app.exception_handler(EmailAlreadyExistsError)
async def email_exists_handler(request: Request, exc: EmailAlreadyExistsError):
    """Handle email already exists exceptions."""
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc), "code": "EMAIL_ALREADY_EXISTS"}
    )


@app.exception_handler(DocumentAlreadyExistsError)
async def document_exists_handler(request: Request, exc: DocumentAlreadyExistsError):
    """Handle document already exists exceptions."""
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc), "code": "DOCUMENT_ALREADY_EXISTS"}
    )


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    """Handle invalid credentials exceptions."""
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc), "code": "INVALID_CREDENTIALS"}
    )


@app.exception_handler(InvalidTokenError)
async def invalid_token_handler(request: Request, exc: InvalidTokenError):
    """Handle invalid token exceptions."""
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc), "code": "INVALID_TOKEN"}
    )


@app.exception_handler(WeakPasswordError)
async def weak_password_handler(request: Request, exc: WeakPasswordError):
    """Handle weak password exceptions."""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "code": "WEAK_PASSWORD"}
    )


@app.exception_handler(UserDomainException)
async def domain_exception_handler(request: Request, exc: UserDomainException):
    """Handle general domain exceptions."""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "code": "DOMAIN_ERROR"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor", "code": "INTERNAL_ERROR"}
    )


# Health check endpoint
@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint para verificar el estado del servicio.
    """
    try:
        # Verificar conexión a la base de datos
        db_healthy = await check_database_health()
        
        if not db_healthy:
            return JSONResponse(
                status_code=503,            content={
                "status": "unhealthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "version": "1.0.0",
                "error": "Database connection failed"
            }
            )
        
        return HealthCheckResponse(
            status="healthy",
            timestamp=datetime.now(timezone.utc),
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "version": "1.0.0",
                "error": str(e)
            }
        )


# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(admin_user_router, prefix="/api/v1")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz del UserService.
    """
    return {
        "service": "SICORA UserService",
        "version": "1.0.0",
        "description": "Microservicio de gestión de usuarios para AsisTE App SENA",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
