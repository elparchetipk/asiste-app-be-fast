# AsisTE-APP Backend - Sistema de Información SICORA

## 📋 Descripción

Backend de la aplicación AsisTE para el control de asistencia de aprendices del SENA, desarrollado como parte del sistema SICORA (Sistema de Información de Coordinación Académica).

## 🏗️ Arquitectura

- **Patrón**: Microservicios con Clean Architecture (rate limiting)
- **Framework**: FastAPI con Python 3.13
- **Base de Datos**: PostgreSQL 15 con pgvector
- **Caché**: Redis
- **Proxy**: Nginx
- **Contenedores**: Docker & Docker Compose

## 🧩 Microservicios

### 1. userservice (Puerto 8001)

Gestión de usuarios y autenticación:

- Registro, login, logout
- Gestión de perfiles
- Autenticación JWT
- Administración CRUD de usuarios

### 2. scheduleservice (Puerto 8002)

Gestión de horarios y programación académica:

- Horarios por ficha
- Entidades maestras (programas, sedes, ambientes)
- Carga masiva de horarios

### 3. attendanceservice (Puerto 8003)

Control de asistencia:

- Registro de asistencia
- Justificaciones
- Reportes de asistencia

### 4. evalinservice (Puerto 8004)

Evaluación de instructores:

- Cuestionarios de evaluación
- Reportes de evaluación
- Gestión de periodos

### 5. kbservice (Puerto 8005)

Base de conocimientos y soporte:

- Artículos de ayuda
- FAQ por rol
- Búsqueda semántica

### 6. aiservice (Puerto 8006)

Servicios de inteligencia artificial:

- Chatbot de reglamento académico
- Análisis predictivo de deserción
- Optimización de horarios

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker & Docker Compose v2.36.2+
- Python 3.13.3 (para desarrollo local)
- Git

### Instalación

1. **Clonar el repositorio**:

```bash
git clone <repository-url>
cd asiste-app-be-fast
```

2. **Configurar variables de entorno**:

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

3. **Inicializar base de datos**:

```bash
docker compose up postgres -d
make db-init
```

4. **Ejecutar todos los servicios**:

```bash
docker compose up -d
```

5. **Verificar servicios**:

```bash
make health-check
```

## 🛠️ Desarrollo

### Comandos Make disponibles

```bash
# Desarrollo
make dev-userservice     # Ejecutar userservice en modo desarrollo
make dev-scheduleservice # Ejecutar scheduleservice en modo desarrollo
make dev-all            # Ejecutar todos los servicios en modo desarrollo

# Base de datos
make db-init            # Inicializar esquemas y permisos
make db-migrate         # Ejecutar migraciones
make db-seed            # Poblar datos de prueba

# Testing
make test               # Ejecutar todos los tests
make test-userservice   # Tests específicos de userservice
make test-coverage      # Reporte de cobertura

# Calidad de código
make lint               # Linting con ruff
make format             # Formatear código
make type-check         # Verificación de tipos

# Docker
make build              # Construir todas las imágenes
make clean              # Limpiar contenedores y volúmenes
```

### Estructura de directorios

```
asiste-app-be-fast/
├── userservice/           # Microservicio de usuarios
│   ├── app/
│   │   ├── domain/       # Entidades, Value Objects, Interfaces
│   │   ├── application/  # Casos de uso, DTOs
│   │   ├── infrastructure/ # Implementaciones, DB, APIs
│   │   └── presentation/ # Routers, Schemas, Dependencies
│   ├── tests/            # Tests unitarios e integración
│   ├── Dockerfile
│   └── requirements.txt
├── scheduleservice/       # Microservicio de horarios
├── attendanceservice/     # Microservicio de asistencia
├── evalinservice/         # Microservicio de evaluaciones
├── kbservice/            # Microservicio de conocimientos
├── aiservice/            # Microservicio de IA
├── nginx/                # Configuración proxy
├── database/             # Scripts SQL e inicialización
├── _docs/                # Documentación técnica
└── docker-compose.yml
```

## 📊 API Endpoints

### Base URL

- **Desarrollo**: `http://localhost/api/v1`
- **Producción**: `https://sicora.elparcheti.co/api/v1`

### Servicios principales

- **Autenticación**: `/api/v1/auth/*`
- **Usuarios**: `/api/v1/users/*`
- **Administración**: `/api/v1/admin/*`
- **Horarios**: `/api/v1/schedule/*`
- **Asistencia**: `/api/v1/attendance/*`
- **Evaluaciones**: `/api/v1/evalin/*`
- **Conocimientos**: `/api/v1/kb/*`
- **IA**: `/api/v1/ai/*`

## 🔐 Seguridad

- **Autenticación**: JWT Bearer tokens
- **Autorización**: Control por roles (admin, instructor, aprendiz)
- **Permisos de BD**: Usuarios específicos por microservicio
- **Hashing**: bcrypt para contraseñas
- **CORS**: Configurado para frontend específico

## 🧪 Testing

- **Unitarios**: Domain layer (90% cobertura objetivo)
- **Integración**: Application layer
- **E2E**: Endpoints completos
- **Performance**: Load testing para endpoints críticos

## 📈 Monitoreo

- **Health Checks**: `/health` en cada servicio
- **Métricas**: Prometheus + Grafana (planificado)
- **Logs**: Estructurados con timestamp y trace ID
- **Alertas**: UptimeRobot para disponibilidad

## 🔄 CI/CD

- **GitHub Actions**: Tests, build, deploy automático
- **Watchtower**: Auto-deployment en producción
- **Commits**: Conventional commits con tags semánticos

## 📚 Documentación

- **API**: Swagger/OpenAPI automático en `/docs`
- **Arquitectura**: `_docs/technical/`
- **Historias de usuario**: `_docs/stories/`
- **Especificaciones**: `_docs/api/`

## 🤝 Contribución

1. Fork del proyecto
2. Crear feature branch: `git checkout -b feat/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'feat: agregar nueva funcionalidad'`
4. Push branch: `git push origin feat/nueva-funcionalidad`
5. Crear Pull Request

## 📄 Licencia

Proyecto Open Source para fines educativos - SENA CGMLTI

---

**Documentación completa**: Ver directorio `_docs/` para especificaciones técnicas detalladas.
