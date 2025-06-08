# Requisitos Funcionales - Asiste App

**Actualizado: 31 de mayo de 2025**

Este documento describe los requisitos funcionales de la aplicación Asiste App, parte del
sistema de información SICORA (Sistema de Información de Coordinación Académica).

## 📋 Documentación de Referencia

Este documento debe leerse en conjunto con los siguientes documentos técnicos:

- **[Especificación de Endpoints API](../api/endpoints_specification.md)**: Define la
  interfaz RESTful completa del backend, formatos de respuesta, códigos de estado y
  estructura HATEOAS.
- **[Historias de Usuario Backend](../stories/be/historias_usuario_be.md)**: Especifica
  las funcionalidades desde la perspectiva del consumidor de la API.
- **[Automatización CI/CD](../automation/CI_CD_AUTOMATION.md)**: Describe el pipeline
  de desarrollo y despliegue automatizado.

## Contexto General

Asiste App es una aplicación para el control de asistencia de aprendices del SENA. Forma
parte de SICORA, que incluirá los siguientes módulos:

- **Asiste** (gestión de asistencia - módulo actual)
- **Comité** (gestión de comités académicos)
- **Evaluación de instructores** (evalin - evaluación de instructores)
- **Horarios** (gestión de horarios y ambientes)
- **Onboarding** (solo para instructores)

## Arquitectura y Tecnologías

### Frontend

- **Framework**: React Native con Expo (enfoque Mobile First). Estrategia completa y
  detallada de respaldo y recuperación. Automatización de respaldo y recuperación.
- **Compilación**: Web
- **Estilización**: TailwindCSS
- **Navegación**: Expo Router

### Backend

- **Arquitectura**: Microservicios con fastapi, Clean Architecture(domain layer, application layer, infrastructure layer, unit testing, integration testing)
- **API**: RESTful (con implementación HATEOAS) con documentación Swagger, API versioning
- **Microservicios**:
  - `userservice` (usuarios y autenticación)
  - `scheduleservice` (horarios y fichas)
  - `attendanceservice` (control de asistencia)
  - `apigateway` (punto de entrada único)
  - `aiservice` (chatbot de reglamento académico y análisis predictivo)
  - `evalinservice` (evaluación de instructores)
  - `kbservice` (knowledge base para soporte IA de admin, instructores, aprendices)
- **Microservicios planificados**:
  - Expansiones futuras según necesidades

### Infraestructura

- **Web Server**: Nginx (balanceo de carga y estrategia de failover)
- **Proxy Inverso**: Traefik (gestión de certificados SSL)
- **Base de Datos**: PostgreSQL 15 con pgvector (balanceo de carga y estrategia de failover). 
  Crear estrategia completa y detallada de respaldo y recuperación. Automatización de respaldo y recuperación.
- **Migraciones**: alembic
- **Caché**: Redis (balanceo de carga y failover)
- **Entorno de Desarrollo**: Docker
- **Despliegue**: Hostinger VPS (Ubuntu 24.04 LTS, UFW firewall)
- **Despliegue Automatizado**: Watchtower
- **Monitoreo**: UptimeRobot
- **Dominio**: sicora.elparcheti.co

### CI/CD

- commits automáticos, con buenas prácticas, escritos en INGLES
- auto release

## 🔗 Especificación de API REST

La interfaz del backend está completamente definida en la *
*[Especificación de Endpoints API](../api/endpoints_specification.md)**, que establece:

### Principios de Diseño API

- **RESTful**: Siguiendo convenciones REST estándar
- **HATEOAS**: Hypermedia as the Engine of Application State para navegación dinámica
- **Versionado**: API versionada con `/v1/` para compatibilidad futura
- **Consistencia**: Formato uniforme en todas las respuestas
- **Seguridad**: JWT Bearer tokens para autenticación y autorización

### Estructura de Endpoints

- **Base URL**: `https://sicora.elparcheti.co/api/v1`
- **Autenticación**: `/api/v1/auth/*` (registro, login, refresh, recuperación)
- **Usuarios**: `/api/v1/users/*` (perfil, gestión personal)
- **Administración**: `/api/v1/admin/*` (gestión administrativa)
- **Horarios**: `/api/v1/schedule/*` (gestión de horarios)
- **Asistencia**: `/api/v1/attendance/*` (registro y consulta)
- **IA**: `/api/v1/ai/*` (análisis predictivo y chatbot)

### Formatos de Respuesta

- **Respuestas exitosas**: Incluyen `success`, `message`, `data`, `links` (HATEOAS) y
  `meta`
- **Respuestas de error**: Incluyen `success: false`, `error` con código y mensaje,
  `links` de ayuda
- **Paginación**: Metadatos de paginación en sección `meta`
- **Timestamps**: Formato ISO 8601 con zona horaria

### Estados de Implementación

- ✅ **Implementado**: Funcionalidad completa y verificada
- 🚧 **En desarrollo**: Implementación parcial
- 📋 **Pendiente**: Planificado pero no iniciado

**Requisito funcional**: Todos los endpoints deben implementarse según la especificación
definida, manteniendo consistencia en formatos, códigos de estado HTTP y estructura
HATEOAS.

## Organización Académica

### Estructura Organizacional

- El Centro de Gestión de Mercados, Logística y Tecnologías de la Información (CGMLTI)
  tiene dos sedes:
  - Sede Calle 52
  - Sede Fontibón
- Cada sede tiene varios ambientes de formación (191, 205, 412, 413, 509, etc.)
- El CGMLTI imparte varios programas, incluyendo Análisis y Desarrollo de Software (ADSO)
- ADSO está asociado a la Coordinación de Teleinformática e Industrias Creativas
- El programa ADSO tiene una duración de 7 trimestres (etapa lectiva)
- Los aprendices deben asistir de forma presencial (98% de la formación)

### Organización de Estudiantes

- Los aprendices se agrupan en fichas (ej. 2826503)
- Un aprendiz solo puede matricularse en una ficha y un único programa
- La carga trimestral de aprendices se realiza mediante archivos CSV. **Nota:** Solo los aprendices debidamente matriculados en el sistema de gestión académica oficial del SENA
  son cargados en SICORA.

### Actividades de Formación

- Durante cada trimestre, los aprendices reciben diferentes actividades de formación
- Las actividades son impartidas por instructores asignados
- Un instructor puede impartir múltiples actividades (sin cruces horarios)
- La carga trimestral de instructores se realiza mediante archivos CSV

### Horarios

- Las actividades se registran en un horario por ficha y trimestre
- La carga de horarios se realiza mediante archivos CSV
- Existen tres jornadas de formación:
  - Mañana: 6:00 a.m. - 12:00 p.m. (lunes a sábado)
  - Tarde: 12:00 p.m. - 6:00 p.m. (lunes a sábado)
  - Noche: 6:00 p.m. - 10:00 p.m. (lunes a viernes) y sábado (6:00 a.m. - 6:00 p.m.)
- Los bloques son de una hora con identificadores específicos (MLUN1, TLUN2, NLUN3, etc.)

## Requisitos de Seguridad

### Gestión de Contraseñas

- Contraseña inicial: número de documento (para aprendices e instructores)
- Cambio obligatorio después del primer uso
- Requisitos de seguridad:
  - Mínimo 10 caracteres
  - Al menos una mayúscula
  - Al menos una minúscula
  - Al menos un dígito numérico
  - Al menos un símbolo (caracter especial !@$%&)
- Contraseñas almacenadas con hashing (bcrypt o Argon2)

### Protección de Datos

- Datos sensibles (documento, correos, teléfono) almacenados con protección
- Implementación mediante control de acceso y logging seguro

## Roles y Permisos

### Administrador

- Carga de datos masivos (CSV)
- Gestión completa de usuarios
- Acceso a reportes y análisis

### Instructor

- Registro de asistencia de aprendices
- Visualización de horarios propios
- Consulta de asistencia histórica

### Aprendiz

- Consulta de su registro de asistencia
- Visualización de horarios de su ficha
- Justificación de inasistencias

## Funcionalidades Principales

### Gestión de Usuarios

- Autenticación (JWT)
- Recuperación de contraseña
- Cambio de contraseña
- Perfil de usuario
- Gestión de roles

### Gestión de Horarios

- Visualización de horarios por ficha
- Visualización de horarios por instructor
- Filtrado por fechas y jornadas

### Control de Asistencia

- Registro de asistencia por parte de instructores
- Consulta de asistencia por parte de aprendices
- Justificación de inasistencias
- Reportes de asistencia

### Funcionalidades Adicionales Implementadas

- Chatbot de reglamento académico
- Análisis predictivo inicial de deserción

### Funcionalidades Planificadas

- Optimización de horarios mediante IA
- Alertas automáticas de asistencia
- Chatbot para consultas sobre reglamento
- Notificaciones automáticas

### Funcionamiento Offline (Aplicación Móvil)

- **RF-OFFLINE-001: Selección de Modo de Sincronización de Datos:** El usuario debe poder configurar la aplicación móvil para:
  - Sincronizar datos (cargar y descargar) únicamente cuando esté conectado a una red
    WiFi.
  - Sincronizar datos utilizando la red de datos móviles del usuario.
  - Por defecto, la aplicación intentará sincronizar datos siempre que haya conexión a internet, priorizando WiFi si está disponible.
- **RF-OFFLINE-002: Sincronización Automática con WiFi:** Siempre que la aplicación móvil
  detecte una conexión WiFi activa y estable, intentará sincronizar automáticamente toda
  la información pendiente con la base de datos del servidor (subir datos locales y
  descargar actualizaciones).
- **RF-OFFLINE-003: Almacenamiento Local de Datos Críticos:** La aplicación móvil debe ser
  capaz de almacenar localmente los datos esenciales para su funcionamiento offline. Esto incluye, como mínimo:
  - Datos de autenticación del usuario (de forma segura).
  - Horario del usuario (aprendiz o instructor).
  - Listas de asistencia pendientes de tomar o enviar (para instructores).
  - Justificaciones creadas pendientes de enviar (para aprendices).
  - Datos necesarios para la visualización del perfil y configuraciones básicas.
- **RF-OFFLINE-004: Indicador de Estado de Conexión y Sincronización:** La interfaz de
  usuario debe mostrar claramente el estado actual de la conexión a internet y el estado
  de la última sincronización de datos.
- **RF-OFFLINE-005: Manejo de Conflictos de Datos (Estrategia Básica):** Se debe definir e
  implementar una estrategia básica para el manejo de conflictos que puedan surgir durante la sincronización (ej. "último en escribir gana" o notificación al usuario para resolución manual en casos complejos). Inicialmente, se priorizará la información del servidor en caso de conflicto simple, con notificación al usuario si se sobrescriben datos locales significativos.
- **RF-OFFLINE-006: Funcionalidad Offline para Registro de Asistencia (Instructor):** Un
  instructor debe poder tomar asistencia de sus fichas asignadas incluso sin conexión a
  internet. Los registros se almacenarán localmente y se sincronizarán cuando la conexión
  esté disponible según la configuración del usuario.
- **RF-OFFLINE-007: Funcionalidad Offline para Creación de Justificaciones (Aprendiz):**
  Un aprendiz debe poder redactar y guardar una justificación por inasistencia incluso sin conexión a internet. La justificación se almacenará localmente y se enviará cuando la conexión esté disponible.
- **RF-OFFLINE-008: Acceso a Horarios Offline:** Tanto aprendices como instructores deben poder consultar sus horarios almacenados localmente incluso sin conexión a internet.
