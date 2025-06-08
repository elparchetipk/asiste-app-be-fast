# Implementación de PostgreSQL con pgvector para Servicios de IA

## Descripción

Este documento describe la implementación de PostgreSQL con la extensión pgvector para soportar las funcionalidades de IA en los servicios `aiservice` y `kbservice` del sistema.

## Contexto

Según los requisitos funcionales definidos en `rf.md`, el sistema debe utilizar "PostgreSQL con pgvector (balanceo de carga y estrategia de failover)" para las funcionalidades de IA. La extensión pgvector permite almacenar y buscar vectores de embeddings, que son fundamentales para:

- Búsqueda semántica (encontrar documentos conceptualmente similares)
- Procesamiento de lenguaje natural
- Recomendaciones personalizadas
- Análisis de similitud

## Implementación

### 1. Configuración de PostgreSQL con pgvector

Se ha modificado el servicio `db` en `docker-compose.yml` para utilizar la imagen oficial de pgvector:

```yaml
db:
  image: pgvector/pgvector:pg15
  environment:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
  ports:
    - '5432:5432'
  volumes:
    - postgres_data:/var/lib/postgresql/data
    - ./docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d
  healthcheck:
    test: ['CMD-SHELL', 'pg_isready -U postgres']
    interval: 30s
    timeout: 10s
    retries: 5
  restart: unless-stopped
  command: ["postgres", "-c", "shared_preload_libraries=vector"]
```

Cambios realizados:
- Uso de la imagen `pgvector/pgvector:pg15` que incluye la extensión pgvector preinstalada
- Montaje del directorio `docker-entrypoint-initdb.d` para scripts de inicialización
- Configuración de `shared_preload_libraries=vector` para cargar la biblioteca pgvector al inicio

### 2. Script de Inicialización

Se ha creado un script SQL (`docker-entrypoint-initdb.d/01-install-pgvector.sql`) que se ejecuta cuando el contenedor de PostgreSQL se inicia por primera vez:

```sql
-- Script para instalar la extensión pgvector en PostgreSQL
-- Este script se ejecutará cuando el contenedor de PostgreSQL se inicie por primera vez

-- Instalar la extensión pgvector en la base de datos template1
-- Esto hará que todas las bases de datos nuevas tengan la extensión disponible
\c template1
CREATE EXTENSION IF NOT EXISTS vector;

-- Mensaje de confirmación
SELECT 'Extensión pgvector instalada en template1' as message;
```

Este script instala la extensión pgvector en la base de datos `template1`, lo que hace que todas las bases de datos nuevas que se creen a partir de ella tengan la extensión disponible automáticamente.

### 3. Uso en los Servicios de IA

#### kbservice

El servicio `kbservice` utiliza pgvector para implementar búsqueda semántica y procesamiento de lenguaje natural. En sus modelos (`models.py`), se definen columnas de tipo `VECTOR(1536)` para almacenar embeddings:

```python
contenido_vector = Column(VECTOR(1536))  # Vector de embeddings para búsqueda semántica
```

También se define un índice HNSW para búsquedas vectoriales eficientes:

```python
Index('idx_knowledge_item_vector', contenido_vector, postgresql_using='hnsw', postgresql_with={'m': 16, 'ef_construction': 64})
```

El servicio incluye la biblioteca pgvector de Python en sus dependencias (`requirements.txt`):

```
pgvector==0.2.4
```

#### aiservice

Aunque actualmente el servicio `aiservice` no utiliza explícitamente pgvector en sus modelos, está preparado para implementar funcionalidades de IA como chatbot de reglamento y análisis predictivo que podrían beneficiarse de esta extensión en el futuro.

## Beneficios

1. **Búsqueda Semántica Avanzada**: Permite encontrar documentos conceptualmente similares aunque usen palabras diferentes.
2. **Procesamiento de Lenguaje Natural Mejorado**: Facilita la comprensión y análisis de consultas en lenguaje natural.
3. **Recomendaciones Personalizadas**: Permite generar recomendaciones basadas en similitud semántica.
4. **Análisis de Similitud**: Facilita la identificación de patrones y relaciones en los datos.

## Conclusión

La implementación de PostgreSQL con pgvector proporciona una base sólida para las funcionalidades de IA del sistema, cumpliendo con los requisitos especificados en `rf.md`. Esta configuración permite almacenar y buscar eficientemente vectores de embeddings, lo que es fundamental para las capacidades de búsqueda semántica y procesamiento de lenguaje natural de los servicios de IA.