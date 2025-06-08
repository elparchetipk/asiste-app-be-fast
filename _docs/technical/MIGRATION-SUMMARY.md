# Actualización de Dependencias para Eliminar el Directorio app/

## Resumen de Cambios

Se han actualizado todas las dependencias que apuntaban al directorio `app/` para garantizar que se pueda eliminar de manera segura. Estos cambios son parte de la migración del servicio de usuarios a una arquitectura de microservicios más consistente, donde el servicio ahora se encuentra en su propio directorio `userservice/`.

## Cambios Realizados

### 1. Archivos de Prueba

- **tests/conftest.py**: Actualizado para importar desde `userservice.app` en lugar de `app`.
  ```python
  # Antes
  from app.database import Base, get_db
  from app.main import app
  
  # Después
  from userservice.app.database import Base, get_db
  from userservice.app.main import app
  ```

### 2. Configuración de Alembic

- **alembic/env.py**: Actualizado para importar desde `userservice.app` en lugar de `app`.
  ```python
  # Antes
  from app.models import Base
  
  # Después
  from userservice.app.models import Base
  ```

### 3. Archivos de Configuración Docker

- **docker-compose.staging.yml**: 
  - Cambiado el nombre del servicio de `web` a `userservice`.
  - Actualizado el contexto de construcción para usar `./userservice`.
  - Actualizado el volumen para montar `./userservice:/app` en lugar de `./app:/app/app`.

- **docker-compose.prod.yml**:
  - Cambiado el nombre del servicio de `web` a `userservice`.

### 4. Flujos de Trabajo de GitHub

- **.github/workflows/ci.yml**:
  - Actualizado los comandos de linting para usar `userservice/app/` en lugar de `app/`.
  - Actualizado la construcción de la imagen Docker para usar `./userservice` como contexto.

- **.github/workflows/release.yml**:
  - Actualizado las referencias en `package.json` para usar `userservice/app/` en lugar de `app/`.
  - Actualizado la construcción de la imagen Docker para usar `./userservice` como contexto.

- **.github/workflows/deploy.yml**:
  - Actualizado el contexto de construcción de la imagen Docker para usar `./userservice`.
  - Actualizado el comando de migración para usar `userservice` en lugar de `web`.

## Implicaciones

1. **Eliminación Segura**: Con estos cambios, el directorio `app/` puede ser eliminado de manera segura, ya que todas las dependencias ahora apuntan a `userservice/app/`.

2. **Consistencia Arquitectónica**: El proyecto ahora sigue una arquitectura de microservicios más consistente, donde cada servicio tiene su propio directorio.

3. **Mantenibilidad Mejorada**: La separación clara de los servicios facilita el mantenimiento y la evolución independiente de cada uno.

## Próximos Pasos

1. **Eliminar el Directorio app/**: Una vez verificado que todos los cambios funcionan correctamente, se puede eliminar el directorio `app/`.

2. **Actualizar la Documentación**: Actualizar cualquier documentación adicional que pueda hacer referencia al directorio `app/`.

3. **Pruebas Exhaustivas**: Ejecutar pruebas completas para asegurar que la funcionalidad no se ha visto afectada por estos cambios.