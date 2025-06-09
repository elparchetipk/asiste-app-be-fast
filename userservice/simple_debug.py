#!/usr/bin/env python3
"""
Script para debuggear el bulk upload más simple.
"""
import requests
import base64
import uuid
import json

# Datos del test
suffix = str(uuid.uuid4())[:8]
print(f"🔢 Usando suffix: {suffix}")

csv_content = f"""first_name,last_name,email,document_number,document_type,role,phone
Maria,Garcia,maria.garcia.{suffix}@example.com,22222{suffix[:3]},CC,instructor,+573001234567
Carlos,Lopez,carlos.lopez.{suffix}@example.com,33333{suffix[:3]},CC,apprentice,+573007654321"""

print("📋 CSV Content:")
print(csv_content)

# Codificar a base64
encoded_content = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')

print("✅ CSV codificado a base64 exitosamente")
print(f"📤 Encoded length: {len(encoded_content)}")
