"""
Configuración global de pytest para tests del UserService.
Incluye fixtures para configuración de base de datos y autenticación.
"""

import asyncio
import pytest
from fastapi.testclient import TestClient

from main import app
from app.infrastructure.config.database import database_config


@pytest.fixture(scope="session")
def event_loop():
    """Crear un loop de eventos para toda la sesión de tests."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_database():
    """Setup de base de datos para tests - crear tablas al inicio de la sesión."""
    print("\n🔧 Configurando base de datos para tests...")
    
    # Crear tablas en la base de datos de test
    await database_config.create_tables()
    print("✅ Tablas de base de datos creadas para testing")
    
    yield
    
    # Cleanup al final de la sesión (opcional)
    try:
        await database_config.close()
        print("🧹 Base de datos de testing cerrada")
    except Exception as e:
        print(f"⚠️  Error al cerrar base de datos: {e}")


@pytest.fixture(scope="session")
def test_client():
    """Cliente de test para FastAPI."""
    return TestClient(app)


@pytest.fixture(scope="function")
async def db_tables_ready():
    """Fixture que asegura que las tablas estén disponibles para cada test."""
    # Verificar que las tablas existen, crear si es necesario
    try:
        await database_config.create_tables()
    except Exception as e:
        print(f"⚠️  Error al verificar/crear tablas: {e}")
    yield
