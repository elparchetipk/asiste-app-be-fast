#!/usr/bin/env python3
"""
Test detallado para diagnosticar el problema de autenticación.
"""

import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from app.infrastructure.config.database import get_db_session
from app.infrastructure.seeders.admin_seeder import AdminSeeder
from app.infrastructure.adapters.bcrypt_password_service import BcryptPasswordService
from app.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository

client = TestClient(app)

# Credenciales fijas para testing
FIXED_ADMIN_EMAIL = "debug.admin@sicora.test.com"
FIXED_ADMIN_PASSWORD = "DebugAdminPass123!"
FIXED_ADMIN_DOCUMENT = "1000000099"

async def debug_password_authentication():
    """Diagnosticar el problema de autenticación de contraseñas"""
    print("🔍 Iniciando diagnóstico de autenticación...")
    
    # 1. Crear servicios directamente
    password_service = BcryptPasswordService()
    print("✅ Password service creado")
    
    # 2. Test directo del password service
    print(f"\n🔐 Test directo del password service:")
    test_password = FIXED_ADMIN_PASSWORD
    hashed = password_service.hash_password(test_password)
    verification = password_service.verify_password(test_password, hashed)
    
    print(f"   Password original: {test_password}")
    print(f"   Hash generado: {hashed[:50]}...")
    print(f"   Verificación directa: {verification}")
    
    if not verification:
        print("❌ ERROR: El password service NO está funcionando correctamente")
        return False
    
    # 3. Crear admin y verificar hash en base de datos
    print(f"\n👤 Creando admin en base de datos...")
    try:
        async for session in get_db_session():
            seeder = AdminSeeder(session)
            user_repository = SQLAlchemyUserRepository(session)
            
            # Crear admin
            admin_user = await seeder.seed_test_admin(
                email=FIXED_ADMIN_EMAIL,
                password=FIXED_ADMIN_PASSWORD,
                first_name="Debug",
                last_name="Admin",
                document_number=FIXED_ADMIN_DOCUMENT,
                force_recreate=True
            )
            
            print(f"✅ Admin creado con ID: {admin_user.id}")
            
            # Obtener usuario de base de datos
            db_user = await user_repository.get_by_email(FIXED_ADMIN_EMAIL)
            
            if db_user:
                print(f"✅ Usuario encontrado en DB: {db_user.email.value}")
                print(f"   Hash en DB: {db_user.hashed_password[:50]}...")
                print(f"   Usuario activo: {db_user.is_active}")
                
                # Verificar hash directamente
                db_verification = password_service.verify_password(FIXED_ADMIN_PASSWORD, db_user.hashed_password)
                print(f"   Verificación con hash de DB: {db_verification}")
                
                if not db_verification:
                    print("❌ ERROR: La contraseña NO coincide con el hash de la base de datos")
                    return False
            else:
                print("❌ ERROR: Usuario no encontrado en base de datos")
                return False
            
            break
                
    except Exception as e:
        print(f"❌ Error al verificar en base de datos: {e}")
        return False
    
    # 4. Test del endpoint de login paso a paso
    print(f"\n🌐 Test del endpoint de login...")
    login_response = client.post("/auth/login", json={
        "email": FIXED_ADMIN_EMAIL,
        "password": FIXED_ADMIN_PASSWORD
    })
    
    print(f"   Status code: {login_response.status_code}")
    
    if login_response.status_code == 200:
        print("✅ Login exitoso!")
        token_data = login_response.json()
        print(f"   Token: {token_data.get('access_token', 'N/A')[:50]}...")
        return True
    else:
        print(f"❌ Login falló: {login_response.text}")
        
        # 5. Test adicional: simular el LoginUseCase manualmente
        print(f"\n🔬 Simulando LoginUseCase manualmente...")
        try:
            async for session in get_db_session():
                user_repository = SQLAlchemyUserRepository(session)
                password_service = BcryptPasswordService()
                
                # Obtener usuario
                user = await user_repository.get_by_email(FIXED_ADMIN_EMAIL)
                print(f"   Usuario encontrado: {user is not None}")
                
                if user:
                    print(f"   Usuario activo: {user.is_active}")
                    print(f"   Hash almacenado: {user.hashed_password[:50]}...")
                    
                    # Verificar contraseña paso a paso
                    print(f"   Contraseña a verificar: '{FIXED_ADMIN_PASSWORD}'")
                    verification_result = password_service.verify_password(FIXED_ADMIN_PASSWORD, user.hashed_password)
                    print(f"   Resultado verificación: {verification_result}")
                    
                    # Test adicional: crear un nuevo hash y comparar
                    new_hash = password_service.hash_password(FIXED_ADMIN_PASSWORD)
                    new_verification = password_service.verify_password(FIXED_ADMIN_PASSWORD, new_hash)
                    print(f"   Nuevo hash: {new_hash[:50]}...")
                    print(f"   Nuevo hash verifica: {new_verification}")
                break
                    
        except Exception as e:
            print(f"❌ Error en simulación: {e}")
        
        return False

if __name__ == "__main__":
    result = asyncio.run(debug_password_authentication())
    print(f"\n🎯 Resultado final: {'ÉXITO' if result else 'FALLO'}")
