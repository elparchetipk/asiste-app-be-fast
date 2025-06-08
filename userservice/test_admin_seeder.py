#!/usr/bin/env python3
"""
Test rápido para verificar que AdminSeeder funciona correctamente.
"""

import asyncio
import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infrastructure.config.database import get_db_session
from app.infrastructure.seeders.admin_seeder import AdminSeeder


async def test_admin_seeder():
    """Test básico del AdminSeeder"""
    print("🔧 Iniciando test del AdminSeeder...")
    
    try:
        # Obtener sesión de base de datos
        async for session in get_db_session():
            print("✅ Sesión de base de datos obtenida")
            
            # Crear seeder
            seeder = AdminSeeder(session)
            print("✅ AdminSeeder inicializado")
            
            # Intentar crear admin de test
            admin_user = await seeder.seed_test_admin(
                email="test.admin@test.com",
                password="TestAdmin123!",
                first_name="Test",
                last_name="Admin",
                document_number="1000000002"
            )
            
            if admin_user:
                print(f"✅ Admin creado exitosamente:")
                print(f"   ID: {admin_user.id}")
                print(f"   Email: {admin_user.email.value}")
                print(f"   Nombre: {admin_user.first_name} {admin_user.last_name}")
                print(f"   Rol: {admin_user.role.value}")
                print(f"   Activo: {admin_user.is_active}")
                return True
            else:
                print("❌ No se pudo crear el admin")
                return False
            
    except Exception as e:
        print(f"❌ Error en test del AdminSeeder: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_first_admin_seeder():
    """Test del método seed_first_admin"""
    print("\n🔧 Iniciando test del seed_first_admin...")
    
    try:
        async for session in get_db_session():
            seeder = AdminSeeder(session)
            
            # Intentar crear primer admin
            admin_user = await seeder.seed_first_admin(
                email="first.admin@sicora.sena.edu.co",
                password="FirstAdmin123!",
                first_name="First",
                last_name="Admin",
                document_number="1000000001"
            )
            
            if admin_user:
                print(f"✅ Primer admin creado exitosamente:")
                print(f"   Email: {admin_user.email.value}")
                return True
            else:
                print("ℹ️  Primer admin no creado (posiblemente ya existen usuarios)")
                return True  # No es error si ya existen usuarios
                
    except Exception as e:
        print(f"❌ Error en test de seed_first_admin: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Función principal"""
    print("🚀 Iniciando tests del AdminSeeder...\n")
    
    # Test 1: AdminSeeder básico
    success1 = await test_admin_seeder()
    
    # Test 2: First admin
    success2 = await test_first_admin_seeder()
    
    print(f"\n📊 Resultados:")
    print(f"   Test AdminSeeder: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"   Test First Admin: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 Todos los tests del AdminSeeder pasaron exitosamente!")
        return 0
    else:
        print("\n💥 Algunos tests fallaron")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
