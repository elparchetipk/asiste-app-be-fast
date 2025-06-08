# HU-BE-DB-001: Implementar Sistema de Permisos Atómicos de Base de Datos

**Fecha de creación:** 5 de junio de 2025  
**Prioridad:** ALTA - Seguridad crítica  
**Iteración:** Inmediata  
**Desarrollador asignado:** GitHub Copilot

## 📋 Descripción General

Actualmente el sistema utiliza un único superusuario PostgreSQL (`postgres/postgres`) para todas las operaciones de base de datos desde todos los microservicios, lo que representa un riesgo de seguridad significativo y viola las mejores prácticas de seguridad. Es necesario implementar un sistema de permisos atómicos que permita acceso granular según el principio de menor privilegio.

## 🎯 Objetivo

Crear un sistema de permisos de base de datos granular que asigne roles específicos a cada microservicio con los permisos mínimos necesarios para su funcionamiento, eliminando el uso del superusuario para operaciones de aplicación.

## 👥 Stakeholders

- **Administradores de Sistema**: Gestión segura de la infraestructura
- **Desarrolladores**: Acceso controlado a datos según necesidades
- **Auditores de Seguridad**: Trazabilidad de accesos y operaciones
- **DevOps**: Deployment seguro y monitoreo de accesos

## 📊 Análisis de Riesgo Actual

### Riesgos Identificados:

- **Acceso excesivo**: Todos los servicios tienen permisos de superusuario
- **Falta de trazabilidad**: No se puede identificar qué servicio realizó qué operación
- **Escalación de privilegios**: Un compromiso de seguridad afecta toda la BD
- **Violación de compliance**: No cumple con principios de seguridad estándar

### Impacto:

- **Seguridad**: CRÍTICO - Exposición completa de datos
- **Auditabilidad**: ALTO - Imposible rastrear accesos por servicio
- **Compliance**: ALTO - Violación de principios de seguridad

## 🎯 Criterios de Aceptación

### CA-BE-DB-001-01: Creación de Roles de Base de Datos

**Como** administrador de sistema  
**Quiero** que cada microservicio tenga un rol específico de PostgreSQL  
**Para** que solo pueda acceder a los recursos que necesita

**Criterios específicos:**

- Crear rol `userservice_role` con permisos sobre esquema `userservice`
- Crear rol `evalinservice_role` con permisos sobre esquema `evalinservice`
- Crear rol `scheduleservice_role` con permisos sobre esquema `scheduleservice`
- Crear rol `attendanceservice_role` con permisos sobre esquema `attendanceservice`
- Crear rol `aiservice_role` con permisos sobre esquema `aiservice`
- Crear rol `kbservice_role` con permisos sobre esquema `kbservice`
- Crear rol `app_admin_role` para operaciones administrativas transversales

### CA-BE-DB-001-02: Creación de Usuarios de Aplicación

**Como** administrador de sistema  
**Quiero** que cada microservicio tenga un usuario específico de base de datos  
**Para** eliminar el uso del superusuario postgres

**Criterios específicos:**

- Crear usuario `userservice_user` asignado a `userservice_role`
- Crear usuario `evalinservice_user` asignado a `evalinservice_role`
- Crear usuario `scheduleservice_user` asignado a `scheduleservice_role`
- Crear usuario `attendanceservice_user` asignado a `attendanceservice_role`
- Crear usuario `aiservice_user` asignado a `aiservice_role`
- Crear usuario `kbservice_user` asignado a `kbservice_role`
- Cada usuario con contraseña segura generada automáticamente

### CA-BE-DB-001-03: Configuración de Esquemas Aislados

**Como** administrador de base de datos  
**Quiero** que cada servicio opere en su propio esquema  
**Para** garantizar aislamiento de datos y permisos

**Criterios específicos:**

- Crear esquema `userservice` para gestión de usuarios
- Crear esquema `evalinservice` para evaluaciones docentes
- Crear esquema `scheduleservice` para horarios y programación
- Crear esquema `attendanceservice` para asistencia
- Crear esquema `aiservice` para inteligencia artificial
- Crear esquema `kbservice` para base de conocimientos
- Mantener esquema `public` solo para elementos compartidos

### CA-BE-DB-001-04: Asignación de Permisos Granulares

**Como** administrador de seguridad  
**Quiero** que cada rol tenga solo los permisos mínimos necesarios  
**Para** cumplir con el principio de menor privilegio

**Criterios específicos:**

- **userservice_role**: SELECT, INSERT, UPDATE, DELETE en tablas de usuarios
- **evalinservice_role**: SELECT, INSERT, UPDATE, DELETE en tablas de evaluaciones
- **scheduleservice_role**: SELECT, INSERT, UPDATE, DELETE en tablas de horarios
- **attendanceservice_role**: SELECT, INSERT, UPDATE, DELETE en tablas de asistencia
- **aiservice_role**: SELECT, INSERT, UPDATE, DELETE en tablas de IA
- **kbservice_role**: SELECT, INSERT, UPDATE, DELETE en tablas de conocimiento
- **app_admin_role**: Permisos de lectura en todos los esquemas para reportes

### CA-BE-DB-001-05: Migración de Configuración

**Como** DevOps engineer  
**Quiero** que las configuraciones de conexión se actualicen automáticamente  
**Para** que los servicios usen los nuevos usuarios sin interrupciones

**Criterios específicos:**

- Actualizar variables de entorno en docker-compose.yml
- Actualizar configuraciones de conexión en cada microservicio
- Mantener backward compatibility durante la migración
- Validar conexiones exitosas con nuevos usuarios

### CA-BE-DB-001-06: Auditoría y Monitoreo

**Como** auditor de seguridad  
**Quiero** poder identificar qué servicio realiza cada operación  
**Para** mantener trazabilidad completa de accesos

**Criterios específicos:**

- Logging de conexiones por usuario específico
- Configuración de pg_stat_statements para monitoreo
- Alertas de accesos anómalos o denegados
- Reportes de actividad por servicio

## 🔧 Especificaciones Técnicas

### Arquitectura de Permisos

```
PostgreSQL Database
├── Esquemas
│   ├── userservice (tablas de usuarios, auth, profiles)
│   ├── evalinservice (evaluaciones, cuestionarios, respuestas)
│   ├── scheduleservice (horarios, programación, calendarios)
│   ├── attendanceservice (asistencias, justificaciones)
│   ├── aiservice (modelos, vectores, embeddings)
│   ├── kbservice (documentos, conocimientos)
│   └── public (elementos compartidos, extensiones)
│
├── Roles
│   ├── userservice_role (permisos en esquema userservice)
│   ├── evalinservice_role (permisos en esquema evalinservice)
│   ├── scheduleservice_role (permisos en esquema scheduleservice)
│   ├── attendanceservice_role (permisos en esquema attendanceservice)
│   ├── aiservice_role (permisos en esquema aiservice)
│   ├── kbservice_role (permisos en esquema kbservice)
│   └── app_admin_role (lectura transversal para reportes)
│
└── Usuarios
    ├── userservice_user (miembro de userservice_role)
    ├── evalinservice_user (miembro de evalinservice_role)
    ├── scheduleservice_user (miembro de scheduleservice_role)
    ├── attendanceservice_user (miembro de attendanceservice_role)
    ├── aiservice_user (miembro de aiservice_role)
    └── kbservice_user (miembro de kbservice_role)
```

### Matriz de Permisos

| Servicio          | Esquema Propio | Lectura Otros Esquemas              | Escritura Otros Esquemas |
| ----------------- | -------------- | ----------------------------------- | ------------------------ |
| userservice       | FULL           | public (read)                       | -                        |
| evalinservice     | FULL           | userservice (read users)            | -                        |
| scheduleservice   | FULL           | userservice (read users)            | -                        |
| attendanceservice | FULL           | userservice, scheduleservice (read) | -                        |
| aiservice         | FULL           | todos (read)                        | -                        |
| kbservice         | FULL           | userservice (read)                  | -                        |
| app_admin         | -              | todos (read)                        | -                        |

## 🚀 Plan de Implementación

### Fase 1: Preparación y Análisis (Día 1)

- Análisis de tablas actuales por servicio
- Diseño de esquemas y permisos
- Creación de scripts de migración

### Fase 2: Implementación de Infraestructura (Día 1-2)

- Creación de esquemas de base de datos
- Creación de roles y usuarios
- Asignación de permisos granulares

### Fase 3: Migración de Datos (Día 2-3)

- Migración de tablas a esquemas correspondientes
- Actualización de referencias cruzadas
- Validación de integridad

### Fase 4: Actualización de Servicios (Día 3-4)

- Actualización de configuraciones de conexión
- Modificación de modelos SQLAlchemy
- Testing de conectividad

### Fase 5: Validación y Rollout (Día 4-5)

- Testing completo de funcionalidades
- Validación de permisos
- Deployment y monitoreo

## 📝 Entregables

1. **Scripts SQL de Migración**

   - Creación de esquemas, roles y usuarios
   - Migración de datos entre esquemas
   - Scripts de rollback

2. **Configuraciones Actualizadas**

   - docker-compose.yml con nuevas variables
   - Configuraciones de conexión por servicio
   - Variables de entorno de seguridad

3. **Documentación Técnica**

   - Guía de arquitectura de permisos
   - Procedimientos de mantenimiento
   - Guía de troubleshooting

4. **Tests de Validación**

   - Tests de conectividad por servicio
   - Validación de permisos
   - Tests de seguridad

5. **Monitoreo y Alertas**
   - Configuración de logging
   - Alertas de seguridad
   - Dashboards de monitoreo

## 🔍 Validación

### Tests de Seguridad

- [ ] Cada servicio puede conectarse solo con su usuario
- [ ] Cada servicio puede acceder solo a su esquema
- [ ] Operaciones no autorizadas son rechazadas
- [ ] Logging de accesos funciona correctamente

### Tests Funcionales

- [ ] Todas las operaciones CRUD funcionan
- [ ] Migraciones Alembic funcionan con nuevos usuarios
- [ ] Consultas cross-service funcionan según permisos
- [ ] Performance no se ve afectada

### Tests de Rollback

- [ ] Capacidad de revertir a configuración anterior
- [ ] Datos no se corrompen durante rollback
- [ ] Servicios siguen funcionando en caso de fallo

## 📊 Métricas de Éxito

- **Seguridad**: 0 servicios usando superusuario postgres
- **Aislamiento**: 100% de tablas en esquemas específicos
- **Permisos**: 100% de operaciones con permisos mínimos
- **Trazabilidad**: 100% de operaciones identificables por servicio
- **Performance**: < 5% de degradación en operaciones

## 🚨 Riesgos y Mitigación

### Riesgos Técnicos

- **Interrupción de servicio**: Migración gradual con rollback preparado
- **Pérdida de datos**: Backups completos antes de migración
- **Problemas de permisos**: Testing exhaustivo en ambiente de desarrollo

### Riesgos de Negocio

- **Downtime**: Migración en horarios de bajo tráfico
- **Funcionalidad afectada**: Validación completa antes de producción

## 📋 Dependencias

### Técnicas

- PostgreSQL 15+ con soporte para esquemas
- Docker Compose para orquestación
- Alembic para migraciones

### Organizacionales

- Aprobación de administradores de sistema
- Coordinación con equipo DevOps
- Ventana de mantenimiento aprobada

---

**Esta historia de usuario es crítica para la seguridad del sistema y debe implementarse con la máxima prioridad siguiendo las mejores prácticas de seguridad de bases de datos.**
