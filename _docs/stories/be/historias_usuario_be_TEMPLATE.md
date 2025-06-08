# Historias de Usuario - Backend (BE) [PLANTILLA PARA OTROS EQUIPOS]

**Actualizado: 31 de mayo de 2025**

> ⚠️ **IMPORTANTE:** Esta es una plantilla para equipos de desarrollo en otros lenguajes/frameworks.  
> **TODAS las historias están marcadas como PENDIENTE** para implementación desde cero.  
> **Referencia:** El equipo de Go ya completó la implementación de UserService al 100%.

Estas historias describen las funcionalidades de la API desde la perspectiva del consumidor (principalmente el Frontend), basadas en la **[Especificación de Endpoints API](../../api/endpoints_specification_TEMPLATE.md)**.

## 📋 Documentación de Referencia

- **[Especificación de Endpoints API](../../api/endpoints_specification_TEMPLATE.md)**: Define todos los endpoints, formatos y contratos
- **[Especificación Implementada (Go)](../../api/endpoints_specification.md)**: Referencia completa del equipo de Go
- **[Reporte de Verificación](../../../VERIFICATION_REPORT.md)**: Estado actual de funcionalidades implementadas en Go
- **[Requisitos Funcionales](../../general/rf.md)**: Contexto y requisitos generales del sistema

## 🏷️ Estados de Implementación

- ✅ **Implementado**: Funcionalidad completamente desarrollada y verificada
- 🚧 **En desarrollo**: Funcionalidad parcialmente implementada o en progreso
- 📋 **Pendiente**: Funcionalidad planificada pero aún no desarrollada
- ❌ **Bloqueado**: Requiere dependencias o revisión de diseño

## 🔐 Autenticación y Usuarios (User Service)

### Autenticación

**HU-BE-001: Registro de Usuario**

- **Como** el Frontend
- **Quiero** poder enviar datos de registro al endpoint `POST /api/v1/auth/register`
- **Para** crear nuevas cuentas de usuario con validación completa
- **Estado**: 📋 **PENDIENTE** - Implementar validación de campos, constraints DB, manejo de duplicados

**HU-BE-002: Login de Usuario**

- **Como** el Frontend
- **Quiero** poder enviar credenciales al endpoint `POST /api/v1/auth/login`
- **Para** recibir tokens JWT (acceso y refresco) válidos por 1 hora
- **Estado**: 📋 **PENDIENTE** - Implementar generación JWT, información completa del usuario

**HU-BE-003: Refresco de Token**

- **Como** el Frontend
- **Quiero** poder renovar el token de acceso con `POST /api/v1/auth/refresh`
- **Para** mantener la sesión activa sin requerir nueva autenticación
- **Estado**: 📋 **PENDIENTE** - Implementar renovación exitosa, actualización last_login

**HU-BE-004: Cerrar Sesión**

- **Como** el Frontend
- **Quiero** poder invalidar tokens con `POST /api/v1/auth/logout`
- **Para** cerrar sesión y revocar el refresh token
- **Estado**: 📋 **PENDIENTE** - Implementar revocación de refresh tokens

**HU-BE-005: Solicitar Restablecimiento de Contraseña**

- **Como** el Frontend
- **Quiero** poder solicitar restablecimiento con `POST /api/v1/auth/forgot-password`
- **Para** iniciar proceso de recuperación de contraseña por email
- **Estado**: 📋 **PENDIENTE** - Implementar generación de tokens seguros, almacenamiento en DB, invalidación de tokens previos

**HU-BE-006: Restablecer Contraseña**

- **Como** el Frontend
- **Quiero** poder establecer nueva contraseña con `POST /api/v1/auth/reset-password`
- **Para** completar el proceso de recuperación de contraseña
- **Estado**: 📋 **PENDIENTE** - Implementar validación de tokens, expiración, actualización segura

**HU-BE-007: Cambio Forzado de Contraseña**

- **Como** el Frontend (usuario con flag must_change_password)
- **Quiero** poder cambiar contraseña obligatoriamente con `POST /api/v1/auth/force-change-password`
- **Para** establecer contraseña segura en primer inicio de sesión
- **Estado**: 📋 **PENDIENTE** - Implementar validación de flag obligatorio, actualización de estado

### Gestión de Perfil de Usuario

**HU-BE-008: Obtener Perfil de Usuario**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar mi perfil con `GET /api/v1/users/profile`
- **Para** obtener información completa del usuario autenticado
- **Estado**: 📋 **PENDIENTE** - Implementar acceso protegido JWT, información completa

**HU-BE-009: Actualizar Perfil de Usuario**

- **Como** el Frontend (con token válido)
- **Quiero** poder actualizar mis datos con `PUT /api/v1/users/profile`
- **Para** mantener mi información personal actualizada
- **Estado**: 📋 **PENDIENTE** - Implementar validación de campos editables, actualización segura

**HU-BE-010: Cambiar Contraseña (Usuario Autenticado)**

- **Como** el Frontend (con token válido)
- **Quiero** poder cambiar mi contraseña con `PUT /api/v1/users/change-password`
- **Para** actualizar mi contraseña de forma segura
- **Estado**: 📋 **PENDIENTE** - Implementar validación de contraseña actual, hash seguro

## 👥 Administración de Usuarios (Admin Service)

### Gestión CRUD de Usuarios

**HU-BE-011: Listar Usuarios (Admin)**

- **Como** un Administrador (con token válido)
- **Quiero** poder consultar usuarios con `GET /api/v1/users/`
- **Para** administrar las cuentas del sistema
- **Estado**: 📋 **PENDIENTE** - Implementar solo rol admin, ordenado por ID descendente

**HU-BE-012: Crear Usuario (Admin)**

- **Como** un Administrador
- **Quiero** poder crear usuarios con `POST /api/v1/admin/users`
- **Para** registrar nuevos usuarios (instructores, aprendices) desde panel admin
- **Estado**: 📋 **PENDIENTE** - Implementar validación completa, asignación automática de flags

**HU-BE-013: Obtener Usuario Específico (Admin)**

- **Como** un Administrador
- **Quiero** poder consultar un usuario con `GET /api/v1/admin/users/:id`
- **Para** revisar información detallada de usuarios específicos
- **Estado**: 📋 **PENDIENTE** - Implementar solo administradores, información completa

**HU-BE-014: Actualizar Usuario (Admin)**

- **Como** un Administrador
- **Quiero** poder actualizar usuarios con `PUT /api/v1/admin/users/:id`
- **Para** modificar información de usuarios existentes
- **Estado**: 📋 **PENDIENTE** - Implementar campos permitidos, actualización automática timestamps

**HU-BE-015: Eliminar/Desactivar Usuario (Admin)**

- **Como** un Administrador
- **Quiero** poder desactivar usuarios con `DELETE /api/v1/admin/users/:id`
- **Para** gestionar usuarios inactivos manteniendo historial
- **Estado**: 📋 **PENDIENTE** - Implementar soft delete, preservación de relaciones, actualización timestamps

### Carga Masiva de Datos

**HU-BE-016: Carga Masiva de Usuarios (Admin)**

- **Como** un Administrador
- **Quiero** poder subir CSV con `POST /api/v1/admin/users/upload`
- **Para** crear múltiples usuarios de forma masiva
- **Estado**: 📋 **PENDIENTE** - Implementar validación CSV completa, procesamiento por lotes, reporte detallado de errores

## 📅 Gestión de Horarios (Schedule Service)

**HU-BE-017: Obtener Horarios**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar horarios con `GET /api/v1/schedule`
- **Para** obtener horarios filtrados por fecha, ficha o instructor
- **Estado**: 📋 **PENDIENTE** - Implementar servicio con estructura básica

**HU-BE-018: Gestión CRUD de Horarios (Admin)**

- **Como** un Administrador
- **Quiero** poder administrar horarios con endpoints CRUD
- **Para** mantener actualizada la programación académica
- **Estado**: 📋 **PENDIENTE** - Implementar operaciones CRUD completas

**HU-BE-019: Carga Masiva de Horarios (Admin)**

- **Como** un Administrador
- **Quiero** poder subir CSV con `POST /api/v1/admin/schedule/upload`
- **Para** crear múltiples entradas de horario masivamente
- **Estado**: 📋 **PENDIENTE** - Implementar validación CSV, procesamiento por lotes

**HU-BE-020: Gestión de Entidades Maestras (Admin)**

- **Como** un Administrador
- **Quiero** poder administrar fichas, programas, sedes y ambientes
- **Para** mantener actualizada la información estructural del centro
- **Estado**: 📋 **PENDIENTE** - Implementar estructura de datos, endpoints básicos

## 📊 Control de Asistencia (Attendance Service)

**HU-BE-021: Registrar Asistencia (Instructor)**

- **Como** un Instructor (con token válido)
- **Quiero** poder registrar asistencia con `POST /api/v1/attendance`
- **Para** registrar entrada de aprendices mediante código QR (renovación cada 15s)
- **Estado**: 📋 **PENDIENTE** - Implementar servicio con estructura básica, tabla

**HU-BE-022: Obtener Resumen de Asistencia**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar resumen con `GET /api/v1/attendance/summary`
- **Para** obtener estadísticas de asistencia con filtros opcionales
- **Estado**: 📋 **PENDIENTE** - Implementar cálculos estadísticos

**HU-BE-023: Obtener Historial de Asistencia**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar historial con `GET /api/v1/attendance/history`
- **Para** revisar registro detallado por periodo, aprendiz o ficha
- **Estado**: 📋 **PENDIENTE** - Implementar consultas con filtros avanzados

**HU-BE-024: Cargar Justificación (Aprendiz)**

- **Como** un Aprendiz (con token válido)
- **Quiero** poder subir justificación con `POST /api/v1/attendance/justification`
- **Para** adjuntar documentos PDF que justifiquen ausencias
- **Estado**: 📋 **PENDIENTE** - Implementar tabla, upload de archivos

**HU-BE-025: Gestionar Justificaciones (Instructor)**

- **Como** un Instructor (con token válido)
- **Quiero** poder actualizar justificaciones con `PUT /api/v1/attendance/justification/:id`
- **Para** aprobar o rechazar justificaciones de aprendices
- **Estado**: 📋 **PENDIENTE** - Implementar workflow de aprobación

**HU-BE-026: Obtener Alertas de Asistencia**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar alertas con `GET /api/v1/attendance/alerts`
- **Para** identificar casos críticos de inasistencia consecutiva
- **Estado**: 📋 **PENDIENTE** - Implementar estructura básica

**HU-BE-027: Alertas de Instructores sin Registro (Admin)**

- **Como** un Administrador
- **Quiero** poder consultar con `GET /api/v1/attendance/alerts/admin/instructors/no-attendance`
- **Para** identificar instructores que no registraron asistencia el día anterior
- **Estado**: 📋 **PENDIENTE** - Implementar monitoreo administrativo

## 🤖 Inteligencia Artificial (AI Service)

### Análisis Predictivo

**HU-BE-028: Dashboard Predictivo de Deserción**

- **Como** un Admin/Instructor (con token válido)
- **Quiero** poder consultar predicciones con `GET /api/v1/ai/desertion/predictions`
- **Para** identificar aprendices en riesgo basado en patrones de asistencia
- **Estado**: 📋 **PENDIENTE** - Implementar modelos ML, análisis predictivo

**HU-BE-029: Optimizador de Horarios**

- **Como** un Administrador
- **Quiero** poder consultar optimizaciones con `GET /api/v1/ai/schedule/optimization`
- **Para** recibir recomendaciones de distribución horaria
- **Estado**: 📋 **PENDIENTE** - Implementar algoritmos de optimización

**HU-BE-030: Análisis con Procesamiento de Lenguaje Natural**

- **Como** un Admin/Instructor
- **Quiero** poder enviar consultas con `POST /api/v1/ai/insights/query`
- **Para** obtener análisis de datos mediante consultas en lenguaje natural
- **Estado**: 📋 **PENDIENTE** - Implementar integración NLP

### Validación y Asistencia Inteligente

**HU-BE-031: Validador Inteligente de CSV**

- **Como** un Administrador
- **Quiero** poder validar CSV con `POST /api/v1/ai/validate/csv`
- **Para** detectar anomalías antes de procesar datos masivos
- **Estado**: 📋 **PENDIENTE** - Implementar detección de anomalías

**HU-BE-032: Asistente de Gestión Proactiva**

- **Como** un Instructor
- **Quiero** poder consultar insights con `GET /api/v1/ai/attendance/insights`
- **Para** recibir recomendaciones personalizadas sobre asistencia
- **Estado**: 📋 **PENDIENTE** - Implementar recomendaciones automáticas

**HU-BE-033: Analizador de Justificaciones**

- **Como** un Instructor
- **Quiero** poder analizar PDF con `POST /api/v1/ai/justifications/analyze/:id`
- **Para** obtener extracción automática de información clave
- **Estado**: 📋 **PENDIENTE** - Implementar procesamiento de documentos

### Chatbot de Reglamento

**HU-BE-034: Consulta al Chatbot de Reglamento**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar con `POST /api/v1/ai/chatbot/query`
- **Para** obtener respuestas sobre reglamento académico con referencias precisas
- **Estado**: 📋 **PENDIENTE** - Implementar base de conocimiento, procesamiento consultas

**HU-BE-035: Obtener Reglamentos Disponibles**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar con `GET /api/v1/ai/chatbot/agreements`
- **Para** obtener lista de acuerdos disponibles para consulta
- **Estado**: 📋 **PENDIENTE** - Implementar catálogo de documentos

## 🌐 API Gateway y Seguridad

**HU-BE-036: Enrutamiento de Microservicios**

- **Como** el Frontend
- **Quiero** poder realizar peticiones a `/api/v1/...`
- **Para** acceder a microservicios sin conocer topología interna
- **Estado**: 📋 **PENDIENTE** - Implementar enrutamiento a servicios

**HU-BE-037: Autenticación Centralizada**

- **Como** el Frontend
- **Quiero** que la API Gateway valide tokens JWT automáticamente
- **Para** garantizar acceso solo a usuarios autenticados
- **Estado**: 📋 **PENDIENTE** - Implementar middleware de validación JWT

**HU-BE-038: Control de Acceso por Roles**

- **Como** el Frontend
- **Quiero** que la API Gateway verifique permisos por rol
- **Para** acceder solo a funcionalidades permitidas según mi rol
- **Estado**: 📋 **PENDIENTE** - Implementar middleware de verificación de roles

**HU-BE-039: Gestión de CORS**

- **Como** desarrollador frontend
- **Quiero** que la API Gateway gestione CORS correctamente
- **Para** permitir acceso seguro desde dominios específicos
- **Estado**: 📋 **PENDIENTE** - Implementar configuración CORS

**HU-BE-040: Logging Centralizado**

- **Como** administrador del sistema
- **Quiero** que la API Gateway registre todas las peticiones
- **Para** auditar uso del sistema y diagnosticar problemas
- **Estado**: 📋 **PENDIENTE** - Implementar logging

**HU-BE-041: Manejo Unificado de Errores**

- **Como** consumidor de la API
- **Quiero** recibir respuestas de error con formato consistente
- **Para** manejarlas uniformemente en el cliente
- **Estado**: 📋 **PENDIENTE** - Implementar formato JSON estándar

## 💾 Respaldo y Recuperación

**HU-BE-042: Respaldo Automático de BD**

- **Como** administrador de sistema
- **Quiero** respaldos automáticos diarios de todas las BD
- **Para** recuperar información en caso de fallos
- **Estado**: 📋 **PENDIENTE** - Implementar automatización de respaldos

**HU-BE-043: Restauración por Servicio**

- **Como** administrador de sistema
- **Quiero** poder restaurar BD individuales desde respaldos
- **Para** recuperar selectivamente sin afectar otros servicios
- **Estado**: 📋 **PENDIENTE** - Implementar scripts de restauración

**HU-BE-044: Verificación de Integridad**

- **Como** administrador de sistema
- **Quiero** recibir notificaciones del resultado de respaldos
- **Para** asegurar validez de respaldos para recuperación
- **Estado**: 📋 **PENDIENTE** - Implementar monitoreo automatizado

**HU-BE-045: Respaldo Incremental**

- **Como** administrador de sistema
- **Quiero** respaldos incrementales cada 6 horas además de completos diarios
- **Para** minimizar pérdida de datos en caso de fallos
- **Estado**: 📋 **PENDIENTE** - Implementar estrategia incremental

**HU-BE-046: Recuperación Point-in-Time**

- **Como** administrador de sistema
- **Quiero** poder restaurar BD a un momento específico
- **Para** recuperar sistema hasta el punto preciso antes de un fallo
- **Estado**: 📋 **PENDIENTE** - Implementar point-in-time recovery

---

## 📊 Resumen de Estado

### 📋 Funcionalidades TODAS PENDIENTES (46)

**User Service (16 historias):**

- 📋 Autenticación completa: registro, login, refresh, logout, reset de contraseña
- 📋 Gestión de perfil: consulta, actualización, cambio de contraseña
- 📋 Administración CRUD: listado, creación, consulta, actualización, eliminación
- 📋 Carga masiva: upload CSV con validaciones y reporte de errores

**Schedule Service (4 historias):**

- 📋 Gestión de horarios y entidades maestras
- 📋 Carga masiva de horarios

**Attendance Service (7 historias):**

- 📋 Control de asistencia completo
- 📋 Justificaciones y alertas

**AI Service (8 historias):**

- 📋 Análisis predictivo y chatbot
- 📋 Validación inteligente de datos

**Infrastructure (11 historias):**

- 📋 API Gateway y seguridad
- 📋 Sistema de respaldo y recuperación

**Total de Historias:** 46  
**Progreso:** 0% implementado, 0% en desarrollo, 100% pendiente

## 🎯 Plan de Implementación Sugerido

### Fase 1: Fundamentos (Semanas 1-4)

**Prioridad: CRÍTICA**

1. 📋 Configuración inicial del proyecto y base de datos
2. 📋 Implementación de autenticación básica (registro, login)
3. 📋 Middleware de JWT y validación de tokens
4. 📋 Gestión básica de perfil de usuario

### Fase 2: Autenticación Completa (Semanas 5-6)

**Prioridad: ALTA** 5. 📋 Sistema de refresh tokens 6. 📋 Reset de contraseña con tokens seguros 7. 📋 Logout con revocación de tokens 8. 📋 Cambio forzado de contraseña

### Fase 3: Administración (Semanas 7-8)

**Prioridad: ALTA** 9. 📋 CRUD completo de usuarios para administradores 10. 📋 Middleware de autorización por roles 11. 📋 Validaciones robustas y manejo de errores 12. 📋 Carga masiva CSV

### Fase 4: API Gateway (Semanas 9-10)

**Prioridad: MEDIA** 13. 📋 Enrutamiento de microservicios 14. 📋 CORS y manejo de errores centralizado 15. 📋 Logging y auditoría

### Fase 5: Servicios Adicionales (Semanas 11+)

**Prioridad: MEDIA-BAJA** 16. 📋 Schedule Service básico 17. 📋 Attendance Service básico 18. 📋 Sistema de respaldo básico

### Fase 6: Funcionalidades Avanzadas (Futuro)

**Prioridad: BAJA** 19. 📋 AI Service y análisis predictivo 20. 📋 Chatbot de reglamento 21. 📋 Optimizaciones avanzadas

## 💡 Recomendaciones de Implementación

### Tecnologías Sugeridas por Lenguaje

**Node.js/TypeScript:**

- Framework: Express.js o Fastify
- ORM: Prisma o TypeORM
- Autenticación: jsonwebtoken + bcrypt
- Validación: Joi o Zod

**Python:**

- Framework: FastAPI o Django REST
- ORM: SQLAlchemy o Django ORM
- Autenticación: PyJWT + bcrypt
- Validación: Pydantic

**Java:**

- Framework: Spring Boot
- ORM: Spring Data JPA
- Autenticación: Spring Security + JWT
- Validación: Bean Validation

**C#/.NET:**

- Framework: ASP.NET Core
- ORM: Entity Framework Core
- Autenticación: Microsoft.AspNetCore.Authentication.JwtBearer
- Validación: FluentValidation

### Patrones Arquitectónicos

- **Clean Architecture** o **Hexagonal Architecture**
- **Repository Pattern** para acceso a datos
- **Middleware Pattern** para funcionalidades transversales
- **Strategy Pattern** para diferentes tipos de autenticación

### Base de Datos

- **PostgreSQL** (recomendado para consistencia con Go)
- **Índices apropiados** en campos de consulta frecuente
- **Transacciones** para operaciones críticas
- **Connection pooling** para rendimiento

---

**📚 Referencia:** La implementación completa y funcional del equipo de Go está disponible en este repositorio para consulta de patrones, estructura y mejores prácticas.
