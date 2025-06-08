# Especificación de Endpoints API - Asiste Backend [PLANTILLA PARA OTROS EQUIPOS]

**Actualizado:** 31 de mayo de 2025  
**Versión API:** v1  
**Base URL:** `https://sicora.elparcheti.co/api/v1`

> ⚠️ **IMPORTANTE:** Esta es una plantilla para equipos de desarrollo en otros lenguajes/frameworks.  
> **TODOS los endpoints están marcados como PENDIENTE** para implementación desde cero.  
> **Referencia:** El equipo de Go ya completó esta implementación al 100%.

## 🎯 Principios de Diseño

- **RESTful**: Siguiendo convenciones REST estándar
- **HATEOAS**: Hypermedia as the Engine of Application State
- **Versionado**: API versionada con `/v1/`
- **Consistencia**: Formato uniforme en todas las respuestas
- **Seguridad**: JWT Bearer tokens para autenticación

## 📋 Formato de Respuesta Estándar

### Respuesta Exitosa (2xx)

```json
{
  "success": true,
  "message": "Descripción de la operación",
  "data": {
    /* datos específicos */
  },
  "links": {
    "self": { "href": "/api/v1/resource", "method": "GET" },
    "related": { "href": "/api/v1/related", "method": "GET" }
  },
  "meta": {
    "timestamp": "2025-05-30T10:00:00Z",
    "version": "1.0",
    "pagination": {
      /* si aplica */
    }
  }
}
```

### Respuesta de Error (4xx, 5xx)

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Mensaje descriptivo del error",
    "details": "Información adicional si está disponible"
  },
  "links": {
    "documentation": { "href": "/api/v1/docs", "method": "GET" },
    "support": { "href": "/api/v1/support", "method": "POST" }
  },
  "meta": {
    "timestamp": "2025-05-30T10:00:00Z",
    "version": "1.0",
    "request_id": "uuid-unique-identifier"
  }
}
```

## 🔐 User Service Endpoints

### Autenticación Pública

#### POST /api/v1/auth/register

**Descripción:** Registrar nuevo usuario  
**Estado:** 📋 **PENDIENTE** - Implementar registro con validaciones robustas  
**Autenticación:** No requerida

**Request Body:**

```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña_segura",
  "first_name": "Nombre",
  "last_name": "Apellido",
  "role": "aprendiz|instructor|admin",
  "document": "1234567890",
  "document_type": "CC|TI|CE|PP"
}
```

**Response 201:**

```json
{
  "success": true,
  "message": "Usuario creado exitosamente",
  "data": {
    "user_id": 123,
    "email": "usuario@ejemplo.com",
    "must_change_password": true
  },
  "links": {
    "self": { "href": "/api/v1/auth/register", "method": "POST" },
    "login": { "href": "/api/v1/auth/login", "method": "POST" },
    "profile": { "href": "/api/v1/users/profile", "method": "GET" }
  }
}
```

#### POST /api/v1/auth/login

**Descripción:** Autenticar usuario  
**Estado:** 📋 **PENDIENTE** - Implementar autenticación con JWT + Refresh Tokens  
**Autenticación:** No requerida

**Request Body:**

```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña"
}
```

**Response 200:**

```json
{
  "success": true,
  "message": "Autenticación exitosa",
  "data": {
    "access_token": "jwt_access_token",
    "refresh_token": "jwt_refresh_token",
    "expires_in": 3600,
    "token_type": "Bearer",
    "user": {
      "id": 123,
      "email": "usuario@ejemplo.com",
      "first_name": "Nombre",
      "last_name": "Apellido",
      "role": "aprendiz",
      "must_change_password": false
    }
  },
  "links": {
    "self": { "href": "/api/v1/auth/login", "method": "POST" },
    "profile": { "href": "/api/v1/users/profile", "method": "GET" },
    "refresh": { "href": "/api/v1/auth/refresh", "method": "POST" },
    "logout": { "href": "/api/v1/auth/logout", "method": "POST" }
  }
}
```

#### POST /api/v1/auth/refresh

**Descripción:** Refrescar token de acceso  
**Estado:** 📋 **PENDIENTE** - Implementar renovación de tokens JWT  
**Autenticación:** Refresh token requerido

#### POST /api/v1/auth/forgot-password

**Descripción:** Solicitar restablecimiento de contraseña  
**Estado:** 📋 **PENDIENTE** - Implementar con tokens seguros (crypto/rand)  
**Autenticación:** No requerida

#### POST /api/v1/auth/reset-password

**Descripción:** Restablecer contraseña con token  
**Estado:** 📋 **PENDIENTE** - Implementar validación de tokens y actualización segura  
**Autenticación:** Token de reset requerido

#### POST /api/v1/auth/logout

**Descripción:** Cerrar sesión e invalidar tokens  
**Estado:** 📋 **PENDIENTE** - Implementar revocación de refresh tokens  
**Autenticación:** Bearer token requerido

### Gestión de Usuarios Autenticados

#### GET /api/v1/users/profile

**Descripción:** Obtener perfil del usuario autenticado  
**Estado:** 📋 **PENDIENTE** - Implementar consulta de perfil protegida por JWT  
**Autenticación:** Bearer token requerido

**Response 200:**

```json
{
  "success": true,
  "message": "Perfil obtenido exitosamente",
  "data": {
    "id": 123,
    "email": "usuario@ejemplo.com",
    "first_name": "Nombre",
    "last_name": "Apellido",
    "role": "aprendiz",
    "document": "1234567890",
    "document_type": "CC",
    "created_at": "2025-05-30T10:00:00Z",
    "updated_at": "2025-05-30T10:00:00Z",
    "last_login": "2025-05-30T09:30:00Z"
  },
  "links": {
    "self": { "href": "/api/v1/users/profile", "method": "GET" },
    "update": { "href": "/api/v1/users/profile", "method": "PUT" },
    "change_password": {
      "href": "/api/v1/users/change-password",
      "method": "PUT"
    },
    "logout": { "href": "/api/v1/auth/logout", "method": "POST" }
  }
}
```

#### PUT /api/v1/users/profile

**Descripción:** Actualizar perfil del usuario autenticado  
**Estado:** 📋 **PENDIENTE** - Implementar actualización de perfil con validaciones  
**Autenticación:** Bearer token requerido

#### PUT /api/v1/users/change-password

**Descripción:** Cambiar contraseña del usuario autenticado  
**Estado:** 📋 **PENDIENTE** - Implementar cambio de contraseña con verificación  
**Autenticación:** Bearer token requerido

#### POST /api/v1/auth/force-change-password

**Descripción:** Cambio forzado de contraseña (primer login)  
**Estado:** 📋 **PENDIENTE** - Implementar cambio obligatorio para primer inicio  
**Autenticación:** Bearer token requerido

### Administración de Usuarios (Admin)

#### GET /api/v1/admin/users

**Descripción:** Listar todos los usuarios  
**Estado:** 📋 **PENDIENTE** - Implementar listado con paginación para administradores  
**Autenticación:** Bearer token + rol admin

#### POST /api/v1/admin/users

**Descripción:** Crear nuevo usuario (admin)  
**Estado:** 📋 **PENDIENTE** - Implementar creación de usuarios por administradores  
**Autenticación:** Bearer token + rol admin

#### GET /api/v1/admin/users/{id}

**Descripción:** Obtener usuario específico  
**Estado:** 📋 **PENDIENTE** - Implementar consulta de usuario específico por ID  
**Autenticación:** Bearer token + rol admin

#### PUT /api/v1/admin/users/{id}

**Descripción:** Actualizar usuario específico  
**Estado:** 📋 **PENDIENTE** - Implementar actualización de cualquier usuario  
**Autenticación:** Bearer token + rol admin

#### DELETE /api/v1/admin/users/{id}

**Descripción:** Eliminar/desactivar usuario  
**Estado:** 📋 **PENDIENTE** - Implementar soft delete de usuarios  
**Autenticación:** Bearer token + rol admin

#### POST /api/v1/admin/users/upload

**Descripción:** Carga masiva de usuarios desde CSV  
**Estado:** 📋 **PENDIENTE** - Implementar carga masiva con validaciones CSV  
**Autenticación:** Bearer token + rol admin

## 🔄 Estados de Implementación

- ✅ **Implementado**: Funcionalidad completa y probada
- 🚧 **En desarrollo**: Implementación parcial
- 📋 **Pendiente**: Planificado pero no iniciado
- ❌ **Bloqueado**: Requiere dependencias

## 📊 Resumen de Progreso

### User Service

- **Implementados**: 0/15 endpoints (0%)
- **Pendientes**: 15/15 endpoints (100%)
- **Estado**: 📋 **PENDIENTE** - Todo por implementar

### Funcionalidades a Implementar

📋 **Autenticación Completa**

- Registro de usuarios con validaciones robustas
- Login con JWT + Refresh Tokens
- Sistema de logout seguro con invalidación de tokens
- Reset de contraseña con tokens seguros (crypto/rand)
- Cambio forzado de contraseña para primer login

📋 **Gestión de Perfil**

- Consulta de perfil de usuario autenticado
- Actualización de datos de perfil
- Cambio de contraseña con validaciones

📋 **Administración de Usuarios**

- CRUD completo para administradores
- Listado con paginación y filtros
- Carga masiva desde CSV con validaciones
- Soft delete con preservación de datos

📋 **Seguridad y Validaciones**

- Hash de contraseñas con bcrypt o equivalente
- Tokens seguros de 256 bits para reset
- Middleware de autenticación y autorización
- Validación completa de entrada de datos
- Manejo consistente de errores

## 🚀 Tareas de Implementación

### Fase 1: Autenticación Básica

1. 📋 Implementar registro de usuarios con validaciones
2. 📋 Implementar login con generación de JWT
3. 📋 Implementar middleware de autenticación
4. 📋 Implementar logout con revocación de tokens

### Fase 2: Gestión de Perfil

5. 📋 Implementar consulta de perfil de usuario
6. 📋 Implementar actualización de perfil
7. 📋 Implementar cambio de contraseña

### Fase 3: Funcionalidades Avanzadas

8. 📋 Implementar refresh de tokens
9. 📋 Implementar forgot/reset password
10. 📋 Implementar cambio forzado de contraseña

### Fase 4: Administración

11. 📋 Implementar CRUD de usuarios para admin
12. 📋 Implementar middleware de autorización por roles
13. 📋 Implementar carga masiva CSV

### Fase 5: Seguridad y Mejoras

14. 📋 Implementar hash seguro de contraseñas
15. 📋 Implementar tokens seguros para reset
16. 📋 Mejorar validaciones y manejo de errores
17. 📋 Integrar servicio de email para notificaciones
18. 📋 Implementar tests unitarios y de integración

## 💡 Recomendaciones Técnicas

### Seguridad

- Usar bibliotecas estándar para hash de contraseñas (bcrypt, scrypt, etc.)
- Generar tokens seguros con cryptographic random
- Implementar rate limiting para endpoints críticos
- Validar entrada de datos con bibliotecas robustas

### Base de Datos

- Implementar transacciones para operaciones críticas
- Usar soft delete para preservar relaciones
- Implementar índices apropiados para rendimiento
- Considerar connection pooling

### Arquitectura

- Seguir patrones MVC o Clean Architecture
- Implementar middleware reutilizable
- Estructurar manejo de errores consistente
- Documentar API con Swagger/OpenAPI

---

**📚 Referencia:** La implementación completa en Go está disponible en este mismo repositorio para consulta y referencia de patrones de implementación.
