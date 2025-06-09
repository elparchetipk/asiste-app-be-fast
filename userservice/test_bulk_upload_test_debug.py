#!/usr/bin/env python3
"""
Script para debuggear exactamente el mismo caso del test que está fallando.
"""
import asyncio
from fastapi.testclient import TestClient
from main import app
from tests.utils.test_helpers import AuthTestHelper
import base64
import uuid
import json

async def test_bulk_upload_test_debug():
    """Debuggear exactamente el mismo escenario del test que falla."""
    print("🔧 Iniciando debug del test bulk upload...")
    
    client = TestClient(app)
    auth_helper = AuthTestHelper(client)
    
    # Crear admin user
    admin_created = await auth_helper.seed_admin_user()
    if not admin_created:
        print("❌ No se pudo crear admin")
        return
        
    admin_token = auth_helper.get_admin_token()
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Crear CSV exactamente como en el test
    suffix = str(uuid.uuid4())[:8]
    print(f"🔢 Usando suffix: {suffix}")
    
    csv_content = f"""first_name,last_name,email,document_number,document_type,role,phone
Maria,Garcia,maria.garcia.{suffix}@example.com,22222{suffix[:3]},CC,instructor,+573001234567
Carlos,Lopez,carlos.lopez.{suffix}@example.com,33333{suffix[:3]},CC,apprentice,+573007654321"""
    
    print("📋 CSV Content:")
    print(csv_content)
    
    # Codificar a base64 exactamente como en el test
    encoded_content = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
    
    upload_data = {
        "file_content": encoded_content,
        "filename": "test_users.csv"
    }
    
    print("📤 Upload data:")
    print(json.dumps(upload_data, indent=2))
    
    # Probar upload exactamente como en el test
    upload_response = client.post(
        "/api/v1/admin/users/upload",
        json=upload_data,
        headers=admin_headers
    )
    
    print(f"📋 Upload response status: {upload_response.status_code}")
    print(f"📋 Upload response body: {upload_response.json()}")
    
    if upload_response.status_code == 200:
        data = upload_response.json()
        print(f"✅ Total processed: {data.get('total_processed')}")
        print(f"✅ Successful: {data.get('successful')}")
        print(f"❌ Failed: {data.get('failed')}")
        print(f"🔧 Errors: {data.get('errors')}")
        print(f"👤 Created users: {data.get('created_users')}")

if __name__ == "__main__":
    asyncio.run(test_bulk_upload_test_debug())
