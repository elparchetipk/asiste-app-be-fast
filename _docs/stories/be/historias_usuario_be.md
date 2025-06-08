# Historias de Usuario - Backend (BE)

**Actualizado: 7 de junio de 2025**

Estas historias describen las funcionalidades de la API desde la perspectiva del consumidor (principalmente el Frontend), basadas en la **[Especificación de Endpoints API](../../api/endpoints_specification.md)**.

## 📋 Documentación de Referencia

- **[Especificación de Endpoints API](../../api/endpoints_specification.md)**: Define todos los endpoints, formatos y contratos
- **[Reporte de Verificación](../../../VERIFICATION_REPORT.md)**: Estado actual de funcionalidades implementadas
- **[Requisitos Funcionales](../../general/rf.md)**: Contexto y requisitos generales del sistema

## 🏷️ Estados de Implementación

- **Pendiente**: Funcionalidad completamente desarrollada y verificada
- 🚧 **En desarrollo**: Funcionalidad parcialmente implementada o en progreso
- 📋 **Pendiente**: Funcionalidad planificada pero aún no desarrollada
- ❌ **Bloqueado**: Requiere dependencias o revisión de diseño

## 🔐 Autenticación y Usuarios (User Service)

### Autenticación

**HU-BE-001: Registro de Usuario**

- **Como** el Frontend
- **Quiero** poder enviar datos de registro al endpoint `POST /api/v1/auth/register`
- **Para** crear nuevas cuentas de usuario con validación completa
- **Estado**: **Pendiente** - Validación de campos, constraints DB, manejo de duplicados

**HU-BE-002: Login de Usuario**

- **Como** el Frontend
- **Quiero** poder enviar credenciales al endpoint `POST /api/v1/auth/login`
- **Para** recibir tokens JWT (acceso y refresco) válidos por 1 hora
- **Estado**: **Pendiente** - Generación JWT, información completa del usuario

**HU-BE-003: Refresco de Token**

- **Como** el Frontend
- **Quiero** poder renovar el token de acceso con `POST /api/v1/auth/refresh`
- **Para** mantener la sesión activa sin requerir nueva autenticación
- **Estado**: **Pendiente** - Renovación exitosa, actualización last_login

**HU-BE-004: Cerrar Sesión**

- **Como** el Frontend
- **Quiero** poder invalidar tokens con `POST /api/v1/auth/logout`
- **Para** cerrar sesión y revocar el refresh token
- **Estado**: **Pendiente** - Revocación de refresh tokens

**HU-BE-005: Solicitar Restablecimiento de Contraseña**

- **Como** el Frontend
- **Quiero** poder solicitar restablecimiento con `POST /api/v1/auth/forgot-password`
- **Para** iniciar proceso de recuperación de contraseña por email
- **Estado**: **Pendiente** - Generación de tokens seguros, almacenamiento en DB, invalidación de tokens previos

**HU-BE-006: Restablecer Contraseña**

- **Como** el Frontend
- **Quiero** poder establecer nueva contraseña con `POST /api/v1/auth/reset-password`
- **Para** completar el proceso de recuperación de contraseña
- **Estado**: **Pendiente** - Validación de tokens, expiración, actualización segura

**HU-BE-007: Cambio Forzado de Contraseña**

- **Como** el Frontend (usuario con flag must_change_password)
- **Quiero** poder cambiar contraseña obligatoriamente con `POST /api/v1/auth/force-change-password`
- **Para** establecer contraseña segura en primer inicio de sesión
- **Estado**: **Pendiente** - Validación de flag obligatorio, actualización de estado

### Gestión de Perfil de Usuario

**HU-BE-008: Obtener Perfil de Usuario**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar mi perfil con `GET /api/v1/users/profile`
- **Para** obtener información completa del usuario autenticado
- **Estado**: **Pendiente** - Acceso protegido JWT, información completa

**HU-BE-009: Actualizar Perfil de Usuario**

- **Como** el Frontend (con token válido)
- **Quiero** poder actualizar mis datos con `PUT /api/v1/users/profile`
- **Para** mantener mi información personal actualizada
- **Estado**: **Pendiente** - Validación de campos editables, actualización segura

**HU-BE-010: Cambiar Contraseña (Usuario Autenticado)**

- **Como** el Frontend (con token válido)
- **Quiero** poder cambiar mi contraseña con `PUT /api/v1/users/change-password`
- **Para** actualizar mi contraseña de forma segura
- **Estado**: **Pendiente** - Validación de contraseña actual, hash seguro

## 👥 Administración de Usuarios (Admin Service)

### Gestión CRUD de Usuarios

**HU-BE-011: Listar Usuarios (Admin)**

- **Como** un Administrador (con token válido)
- **Quiero** poder consultar usuarios con `GET /api/v1/users/`
- **Para** administrar las cuentas del sistema
- **Estado**: **Pendiente** - Solo rol admin, paginación, filtrado por rol/estado/búsqueda, ordenamiento configurable, metadatos de paginación, enlaces HATEOAS

**HU-BE-012: Crear Usuario (Admin)**

- **Como** un Administrador
- **Quiero** poder crear usuarios con `POST /api/v1/admin/users`
- **Para** registrar nuevos usuarios (instructores, aprendices) desde panel admin
- **Estado**: **Pendiente** - Solo rol admin, validación de campos, verificación de duplicados (email/username/documento), generación de contraseña inicial igual al documento, flag must_change_password, hash seguro, código 201 (Created)

**HU-BE-013: Obtener Usuario Específico (Admin)**

- **Como** un Administrador
- **Quiero** poder consultar un usuario con `GET /api/v1/admin/users/:id`
- **Para** revisar información detallada de usuarios específicos
- **Estado**: **Pendiente** - Solo rol admin, validación de ID existente, información completa del usuario, enlaces HATEOAS para operaciones relacionadas, manejo de errores 404 para IDs no existentes

**HU-BE-014: Actualizar Usuario (Admin)**

- **Como** un Administrador
- **Quiero** poder actualizar usuarios con `PUT /api/v1/admin/users/:id`
- **Para** modificar información de usuarios existentes
- **Estado**: **Pendiente** - Solo rol admin, validación de ID existente, validación de campos editables, verificación de duplicados (email/username/documento), actualización de rol, actualización automática de timestamps, respuesta con información completa actualizada

**HU-BE-015: Eliminar/Desactivar Usuario (Admin)**

- **Como** un Administrador
- **Quiero** poder desactivar usuarios con `DELETE /api/v1/admin/users/:id`
- **Para** gestionar usuarios inactivos manteniendo historial
- **Estado**: **Pendiente** - Solo rol admin, validación de ID existente, soft delete (is_active=false, deleted_at), preservación de relaciones y datos históricos, prevención de auto-eliminación, mensaje de confirmación

### Carga Masiva de Datos

**HU-BE-016: Carga Masiva de Usuarios (Admin)**

- **Como** un Administrador
- **Quiero** poder subir CSV con `POST /api/v1/admin/users/upload`
- **Para** crear múltiples usuarios de forma masiva
- **Estado**: **Pendiente** - Solo rol admin, validación completa del CSV, procesamiento por lotes, contraseña inicial igual al documento, flag must_change_password, reporte detallado de errores por fila, estadísticas del proceso

## 📅 Gestión de Horarios (Schedule Service)

**HU-BE-017: Obtener Horarios**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar horarios con `GET /api/v1/schedule`
- **Para** obtener horarios filtrados por fecha, ficha o instructor
- **Estado**: **Pendiente** - Filtrado completo, paginación, HATEOAS, comportamiento por rol

**HU-BE-018: Gestión CRUD de Horarios (Admin)**

- **Como** un Administrador
- **Quiero** poder administrar horarios con endpoints CRUD
- **Para** mantener actualizada la programación académica
- **Estado**: 📋 **Pendiente** - Operaciones CRUD completas

**HU-BE-019: Carga Masiva de Horarios (Admin)**

- **Como** un Administrador
- **Quiero** poder subir CSV con `POST /api/v1/admin/schedule/upload`
- **Para** crear múltiples entradas de horario masivamente
- **Estado**: 📋 **Pendiente** - Validación CSV, procesamiento por lotes

**HU-BE-020: Gestión de Entidades Maestras (Admin)**

- **Como** un Administrador
- **Quiero** poder administrar fichas, programas, sedes y ambientes
- **Para** mantener actualizada la información estructural del centro
- **Estado**: **Pendiente** - Estructura de datos definida, endpoints básicos en progreso

## 📊 Control de Asistencia (Attendance Service)

**HU-BE-021: Registrar Asistencia (Instructor)**

- **Como** un Instructor (con token válido)
- **Quiero** poder registrar asistencia con `POST /api/v1/attendance`
- **Para** registrar entrada de aprendices mediante código QR (renovación cada 15s)
- **Estado**: 📋 **Pendiente** - Servicio con estructura básica, tabla creada

**HU-BE-022: Obtener Resumen de Asistencia**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar resumen con `GET /api/v1/attendance/summary`
- **Para** obtener estadísticas de asistencia con filtros opcionales
- **Estado**: **Pendiente** - Endpoint completo con filtros, roles y HATEOAS

**HU-BE-023: Obtener Historial de Asistencia**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar historial con `GET /api/v1/attendance/history`
- **Para** revisar registro detallado por periodo, aprendiz o ficha
- **Estado**: **Pendiente** - Endpoint completo con filtros, paginación, roles y HATEOAS

**HU-BE-024: Cargar Justificación (Aprendiz)**

- **Como** un Aprendiz (con token válido)
- **Quiero** poder subir justificación con `POST /api/v1/attendance/justification`
- **Para** adjuntar documentos PDF que justifiquen ausencias
- **Estado**: **Pendiente** - Validación completa, upload de archivos PDF, almacenamiento seguro

**HU-BE-025: Gestionar Justificaciones (Instructor)**

- **Como** un Instructor (con token válido)
- **Quiero** poder actualizar justificaciones con `PUT /api/v1/attendance/justification/:id`
- **Para** aprobar o rechazar justificaciones de aprendices
- **Estado**: **Pendiente** - Validación completa, workflow de aprobación/rechazo, actualización automática de asistencia

**HU-BE-026: Obtener Alertas de Asistencia**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar alertas con `GET /api/v1/attendance/alerts`
- **Para** identificar casos críticos de inasistencia consecutiva
- **Estado**: **Pendiente** - Filtrado por rol, categorización por criticidad, recomendaciones de acción, HATEOAS

**HU-BE-027: Alertas de Instructores sin Registro (Admin)**

- **Como** un Administrador
- **Quiero** poder consultar con `GET /api/v1/attendance/alerts/admin/instructors/no-attendance`
- **Para** identificar instructores que no registraron asistencia el día anterior
- **Estado**: **Pendiente** - Filtrado por sede/programa/ficha, validación de rol, enlaces HATEOAS

## 🤖 Inteligencia Artificial (AI Service)

### Análisis Predictivo

**HU-BE-028: Dashboard Predictivo de Deserción**

- **Como** un Admin/Instructor (con token válido)
- **Quiero** poder consultar predicciones con `GET /api/v1/ai/desertion/predictions`
- **Para** identificar aprendices en riesgo basado en patrones de asistencia
- **Estado**: 📋 **Pendiente** - Modelos ML, análisis predictivo

**HU-BE-029: Optimizador de Horarios**

- **Como** un Administrador
- **Quiero** poder consultar optimizaciones con `GET /api/v1/ai/schedule/optimization`
- **Para** recibir recomendaciones de distribución horaria
- **Estado**: 📋 **Pendiente** - Algoritmos de optimización

**HU-BE-030: Análisis con Procesamiento de Lenguaje Natural**

- **Como** un Admin/Instructor
- **Quiero** poder enviar consultas con `POST /api/v1/ai/insights/query`
- **Para** obtener análisis de datos mediante consultas en lenguaje natural
- **Estado**: 📋 **Pendiente** - Integración NLP

### Validación y Asistencia Inteligente

**HU-BE-031: Validador Inteligente de CSV**

- **Como** un Administrador
- **Quiero** poder validar CSV con `POST /api/v1/ai/validate/csv`
- **Para** detectar anomalías antes de procesar datos masivos
- **Estado**: 📋 **Pendiente** - Detección de anomalías

**HU-BE-032: Asistente de Gestión Proactiva**

- **Como** un Instructor
- **Quiero** poder consultar insights con `GET /api/v1/ai/attendance/insights`
- **Para** recibir recomendaciones personalizadas sobre asistencia
- **Estado**: 📋 **Pendiente** - Recomendaciones automáticas

**HU-BE-033: Analizador de Justificaciones**

- **Como** un Instructor
- **Quiero** poder analizar PDF con `POST /api/v1/ai/justifications/analyze/:id`
- **Para** obtener extracción automática de información clave
- **Estado**: 📋 **Pendiente** - Procesamiento de documentos

### Chatbot de Reglamento

**HU-BE-034: Consulta al Chatbot de Reglamento**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar con `POST /api/v1/ai/chatbot/query`
- **Para** obtener respuestas sobre reglamento académico con referencias precisas
- **Estado**: 📋 **Pendiente** - Base de conocimiento, procesamiento consultas

**HU-BE-035: Obtener Reglamentos Disponibles**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar con `GET /api/v1/ai/chatbot/agreements`
- **Para** obtener lista de acuerdos disponibles para consulta
- **Estado**: 📋 **Pendiente** - Catálogo de documentos

## 🌐 API Gateway y Seguridad

**HU-BE-036: Enrutamiento de Microservicios**

- **Como** el Frontend
- **Quiero** poder realizar peticiones a `/api/v1/...`
- **Para** acceder a microservicios sin conocer topología interna
- **Estado**: **Pendiente** - Gin enrutando a servicios

**HU-BE-037: Autenticación Centralizada**

- **Como** el Frontend
- **Quiero** que la API Gateway valide tokens JWT automáticamente
- **Para** garantizar acceso solo a usuarios autenticados
- **Estado**: **Pendiente** - Middleware de validación JWT

**HU-BE-038: Control de Acceso por Roles**

- **Como** el Frontend
- **Quiero** que la API Gateway verifique permisos por rol
- **Para** acceder solo a funcionalidades permitidas según mi rol
- **Estado**: **Pendiente** - Middleware básico de verificación de roles

**HU-BE-039: Gestión de CORS**

- **Como** desarrollador frontend
- **Quiero** que la API Gateway gestione CORS correctamente
- **Para** permitir acceso seguro desde dominios específicos
- **Estado**: **Pendiente** - Configurado para desarrollo

**HU-BE-040: Logging Centralizado**

- **Como** administrador del sistema
- **Quiero** que la API Gateway registre todas las peticiones
- **Para** auditar uso del sistema y diagnosticar problemas
- **Estado**: **Pendiente** - Logging básico activo

**HU-BE-041: Manejo Unificado de Errores**

- **Como** consumidor de la API
- **Quiero** recibir respuestas de error con formato consistente
- **Para** manejarlas uniformemente en el cliente
- **Estado**: **Pendiente** - Formato JSON estándar

## 💾 Respaldo y Recuperación

**HU-BE-042: Respaldo Automático de BD**

- **Como** administrador de sistema
- **Quiero** respaldos automáticos diarios de todas las BD
- **Para** recuperar información en caso de fallos
- **Estado**: **Pendiente** - Sistema automatizado con política de retención granular

**HU-BE-043: Restauración por Servicio**

- **Como** administrador de sistema
- **Quiero** poder restaurar BD individuales desde respaldos
- **Para** recuperar selectivamente sin afectar otros servicios
- **Estado**: *Pendiente** - Scripts de restauración

**HU-BE-044: Verificación de Integridad**

- **Como** administrador de sistema
- **Quiero** recibir notificaciones del resultado de respaldos
- **Para** asegurar validez de respaldos para recuperación
- **Estado**: 📋 **Pendiente** - Monitoreo automatizado

**HU-BE-045: Respaldo Incremental**

- **Como** administrador de sistema
- **Quiero** respaldos incrementales cada 6 horas además de completos diarios
- **Para** minimizar pérdida de datos en caso de fallos
- **Estado**: 📋 **Pendiente** - Estrategia incremental

**HU-BE-046: Recuperación Point-in-Time**

- **Como** administrador de sistema
- **Quiero** poder restaurar BD a un momento específico
- **Para** recuperar sistema hasta el punto preciso antes de un fallo
- **Estado**: 📋 **Pendiente** - Implementación point-in-time recovery

---

## 🏗️ Arquitectura y Calidad de Código

### Clean Architecture

**HU-BE-047: Implementar Domain Layer**

- **Como** desarrollador del equipo
- **Quiero** que todos los microservicios implementen una capa de dominio clara
- **Para** encapsular la lógica de negocio independientemente de frameworks y tecnologías externas
- **Estado**: **Pendiente** - UserService: Domain Layer completo con entidades, Value Objects, Repository Interfaces, excepciones de dominio y 69 tests unitarios funcionando

**HU-BE-048: Implementar Application Layer**

- **Como** desarrollador del equipo
- **Quiero** que todos los microservicios tengan una capa de aplicación bien definida
- **Para** coordinar casos de uso y manejar flujos de trabajo de manera testeable
- **Estado**: **Pendiente** - Implementando casos de uso y DTOs para UserService

**HU-BE-049: Implementar Infrastructure Layer**

- **Como** desarrollador del equipo
- **Quiero** que todos los microservicios separen la infraestructura (BD, APIs externas) del dominio
- **Para** facilitar testing, mantenimiento y escalabilidad del sistema
- **Estado**: 📋 **Pendiente** - Separación de responsabilidades de infraestructura

**HU-BE-050: Refactorizar Microservicios Existentes**

- **Como** desarrollador del equipo
- **Quiero** migrar la estructura actual de microservicios a Clean Architecture
- **Para** mejorar la mantenibilidad, testabilidad y escalabilidad del código existente
- **Estado**: 📋 **Pendiente** - Refactoring gradual manteniendo funcionalidad

### Testing Integral

**HU-BE-051: Implementar Unit Testing Completo**

- **Como** desarrollador del equipo
- **Quiero** cobertura de tests unitarios del 90% en todos los microservicios
- **Para** garantizar calidad del código y prevenir regresiones
- **Estado**: 📋 **Pendiente** - Suite completa de tests unitarios

**HU-BE-052: Implementar Integration Testing**

- **Como** desarrollador del equipo
- **Quiero** tests de integración para todos los endpoints y flujos críticos
- **Para** validar el correcto funcionamiento entre capas y servicios
- **Estado**: 📋 **Pendiente** - Tests de integración automatizados

**HU-BE-053: Implementar End-to-End Testing**

- **Como** desarrollador del equipo
- **Quiero** tests end-to-end que validen flujos completos del sistema
- **Para** asegurar que la funcionalidad opere correctamente desde la perspectiva del usuario
- **Estado**: 📋 **Pendiente** - Tests E2E automatizados

**HU-BE-054: Configurar Pipeline de Testing**

- **Como** desarrollador del equipo
- **Quiero** un pipeline automatizado que ejecute todos los tests en CI/CD
- **Para** garantizar que todo cambio de código mantenga la calidad y funcionalidad
- **Estado**: 📋 **Pendiente** - Integración continua con testing automatizado

---
