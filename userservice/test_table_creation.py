"""Test para verificar que las tablas se crean correctamente"""
import asyncio
import sys
from pathlib import Path

# Agregar el directorio userservice al path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from app.infrastructure.config.database import get_db_session

async def test_table_creation():
    """Verificar que la tabla users existe"""
    print("🔍 Verificando creación de tablas...")
    
    # Obtener sesión de base de datos
    async for session in get_db_session():
        try:
            # Verificar que la tabla users existe
            result = await session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'"))
            table_exists = result.fetchone()
            
            if table_exists:
                print("✅ Tabla 'users' existe")
                
                # Verificar estructura de la tabla
                result = await session.execute(text("PRAGMA table_info(users)"))
                columns = result.fetchall()
                print(f"📊 Columnas de la tabla users: {len(columns)}")
                for col in columns:
                    print(f"   - {col[1]} ({col[2]})")
                    
                # Verificar alembic_version
                result = await session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='alembic_version'"))
                alembic_table = result.fetchone()
                
                if alembic_table:
                    print("✅ Tabla 'alembic_version' existe")
                    result = await session.execute(text("SELECT version_num FROM alembic_version"))
                    version = result.fetchone()
                    if version:
                        print(f"📝 Versión actual de migración: {version[0]}")
                    else:
                        print("⚠️  No hay versión registrada en alembic_version")
                else:
                    print("❌ Tabla 'alembic_version' no existe")
            else:
                print("❌ Tabla 'users' no existe")
                
        except Exception as e:
            print(f"❌ Error al verificar tablas: {e}")
        finally:
            await session.close()
            break

if __name__ == "__main__":
    asyncio.run(test_table_creation())
