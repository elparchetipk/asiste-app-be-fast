# Historias de Usuario - Backend (BE) - Knowledge Base Service (kbservice)

**Actualizado: 7 de junio de 2025**

Estas historias describen las funcionalidades de la API del Knowledge Base Service desde la perspectiva del consumidor (principalmente el Frontend), basadas en los requisitos funcionales definidos en **[Requisitos Funcionales KB](../../general/rf_kb.md)**.

## 📋 Documentación de Referencia

- **[Requisitos Funcionales KB](../../general/rf_kb.md)**: Contexto y requisitos
  específicos del Knowledge Base Service
- **[Requisitos Funcionales](../../general/rf.md)**: Contexto y requisitos generales del
  sistema
- **[Especificación de Endpoints API](../../api/endpoints_specification.md)**: Define
  todos los endpoints, formatos y contratos

## 🏷️ Estados de Implementación

- ✅ **Implementado**: Funcionalidad completamente desarrollada y verificada
- 🚧 **En desarrollo**: Funcionalidad parcialmente implementada o en progreso
- 📋 **Pendiente**: Funcionalidad planificada pero aún no desarrollada
- ❌ **Bloqueado**: Requiere dependencias o revisión de diseño

## 🧠 Knowledge Base Service (kbservice)

### Gestión de Contenido de Conocimiento

**HU-BE-KB-001: Crear Elemento de Conocimiento**

- **Como** un Administrador (con token válido)
- **Quiero** poder crear nuevos elementos de conocimiento con `POST /api/v1/kb/items`
- **Para** agregar documentación, guías y respuestas a preguntas frecuentes al sistema
- **Estado**: 📋 **PENDIENTE** - Implementar validación de campos, almacenamiento en DB,
  generación de embeddings

**HU-BE-KB-002: Obtener Elemento de Conocimiento**

- **Como** el Frontend (con token válido)
- **Quiero** poder consultar un elemento específico con `GET /api/v1/kb/items/{id}`
- **Para** mostrar su contenido completo al usuario
- **Estado**: 📋 **PENDIENTE** - Implementar recuperación por ID, manejo de errores

**HU-BE-KB-003: Actualizar Elemento de Conocimiento**

- **Como** un Administrador (con token válido)
- **Quiero** poder actualizar elementos existentes con `PUT /api/v1/kb/items/{id}`
- **Para** mantener la información actualizada y corregir errores
- **Estado**: 📋 **PENDIENTE** - Implementar validación de campos, actualización en DB,
  regeneración de embeddings

**HU-BE-KB-004: Eliminar Elemento de Conocimiento**

- **Como** un Administrador (con token válido)
- **Quiero** poder eliminar elementos con `DELETE /api/v1/kb/items/{id}`
- **Para** remover información obsoleta o incorrecta
- **Estado**: 📋 **PENDIENTE** - Implementar eliminación segura, validación de permisos

**HU-BE-KB-005: Listar Elementos de Conocimiento**

- **Como** el Frontend (con token válido)
- **Quiero** poder listar elementos con `GET /api/v1/kb/items`
- **Para** mostrar un catálogo de la información disponible
- **Estado**: 📋 **PENDIENTE** - Implementar paginación, filtrado por categoría/tipo,
  ordenamiento

**HU-BE-KB-006: Filtrar Elementos por Tipo de Usuario**

- **Como** el Frontend (con token válido)
- **Quiero** poder filtrar elementos por tipo de usuario con
  `GET /api/v1/kb/items?user_type={type}`
- **Para** mostrar solo información relevante según el rol del usuario (admin, instructor,
  aprendiz)
- **Estado**: 📋 **PENDIENTE** - Implementar filtrado específico por tipo de usuario

### Búsqueda y Consulta de Conocimiento

**HU-BE-KB-007: Búsqueda de Texto Tradicional**

- **Como** el Frontend (con token válido)
- **Quiero** poder buscar elementos por texto con `GET /api/v1/kb/search?query={text}`
- **Para** encontrar información basada en coincidencias de palabras clave
- **Estado**: 📋 **PENDIENTE** - Implementar búsqueda de texto completo con PostgreSQL

**HU-BE-KB-008: Búsqueda Semántica**

- **Como** el Frontend (con token válido)
- **Quiero** poder realizar búsquedas semánticas con
  `GET /api/v1/kb/semantic-search?query={text}`
- **Para** encontrar información conceptualmente similar aunque use palabras diferentes
- **Estado**: 📋 **PENDIENTE** - Implementar búsqueda vectorial con pgvector, generación de
  embeddings

**HU-BE-KB-009: Consulta Inteligente**

- **Como** el Frontend (con token válido)
- **Quiero** poder enviar consultas a `POST /api/v1/kb/query`
- **Para** recibir respuestas inteligentes basadas en la base de conocimiento
- **Estado**: 📋 **PENDIENTE** - Implementar análisis NLP, routing inteligente, combinación
  de fuentes

**HU-BE-KB-010: Consulta con Contexto de Usuario**

- **Como** el Frontend (con token válido)
- **Quiero** poder incluir el contexto del usuario en las consultas
- **Para** recibir respuestas personalizadas según el rol y necesidades específicas
- **Estado**: 📋 **PENDIENTE** - Implementar personalización basada en roles, historial y
  preferencias

### Integración con Chatbot de Reglamento

**HU-BE-KB-011: Routing Inteligente al Chatbot**

- **Como** el sistema
- **Quiero** poder determinar si una consulta debe dirigirse al chatbot de reglamentos
- **Para** proporcionar respuestas precisas sobre normativas institucionales
- **Estado**: 📋 **PENDIENTE** - Implementar clasificación de intenciones, integración con
  aiservice

**HU-BE-KB-012: Consulta Híbrida**

- **Como** el Frontend (con token válido)
- **Quiero** poder obtener respuestas combinadas de la base de conocimiento y el chatbot
- **Para** proporcionar información completa que integre procedimientos y reglamentos
- **Estado**: 📋 **PENDIENTE** - Implementar orquestación de respuestas, combinación
  coherente

**HU-BE-KB-013: Fallback Automático**

- **Como** el sistema
- **Quiero** poder recurrir a fuentes alternativas cuando una fuente primaria no está
  disponible
- **Para** garantizar respuestas incluso cuando hay problemas con algún componente
- **Estado**: 📋 **PENDIENTE** - Implementar mecanismos de fallback, manejo de errores

### Gestión de Embeddings y Vectores

**HU-BE-KB-014: Generación de Embeddings**

- **Como** el sistema
- **Quiero** poder generar embeddings vectoriales para el contenido de conocimiento
- **Para** habilitar búsquedas semánticas eficientes
- **Estado**: 📋 **PENDIENTE** - Implementar integración con APIs de embeddings,
  almacenamiento eficiente

**HU-BE-KB-015: Regeneración de Embeddings**

- **Como** un Administrador
- **Quiero** poder regenerar embeddings para contenido existente con
  `POST /api/v1/kb/admin/regenerate-embeddings`
- **Para** actualizar vectores cuando se mejoran los modelos o algoritmos
- **Estado**: 📋 **PENDIENTE** - Implementar proceso batch, manejo de errores, logging

**HU-BE-KB-016: Optimización de Índices Vectoriales**

- **Como** un Administrador
- **Quiero** poder optimizar los índices vectoriales con
  `POST /api/v1/kb/admin/optimize-indices`
- **Para** mantener el rendimiento óptimo de las búsquedas semánticas
- **Estado**: 📋 **PENDIENTE** - Implementar optimización de índices HNSW, configuración de
  parámetros

### Análisis y Métricas

**HU-BE-KB-017: Registro de Consultas**

- **Como** el sistema
- **Quiero** registrar todas las consultas y sus resultados
- **Para** analizar patrones y mejorar el servicio continuamente
- **Estado**: 📋 **PENDIENTE** - Implementar logging estructurado, almacenamiento eficiente

**HU-BE-KB-018: Métricas de Rendimiento**

- **Como** un Administrador
- **Quiero** poder consultar métricas de rendimiento con `GET /api/v1/kb/admin/metrics`
- **Para** monitorear la efectividad y eficiencia del servicio
- **Estado**: 📋 **PENDIENTE** - Implementar recopilación de métricas, endpoints de
  consulta

**HU-BE-KB-019: Análisis de Patrones de Consulta**

- **Como** un Administrador
- **Quiero** poder ver análisis de patrones de consulta con
  `GET /api/v1/kb/admin/query-patterns`
- **Para** identificar áreas de mejora y contenido faltante
- **Estado**: 📋 **PENDIENTE** - Implementar análisis estadístico, visualización de datos

**HU-BE-KB-020: Feedback de Usuarios**

- **Como** el Frontend (con token válido)
- **Quiero** poder enviar feedback sobre respuestas con `POST /api/v1/kb/feedback`
- **Para** mejorar la calidad de las respuestas futuras
- **Estado**: 📋 **PENDIENTE** - Implementar recopilación de feedback, análisis de
  satisfacción

### Caché y Optimización

**HU-BE-KB-021: Caché de Respuestas Frecuentes**

- **Como** el sistema
- **Quiero** poder cachear respuestas a consultas frecuentes
- **Para** mejorar el tiempo de respuesta y reducir la carga del sistema
- **Estado**: 📋 **PENDIENTE** - Implementar estrategia de caché con Redis, invalidación
  inteligente

**HU-BE-KB-022: Caché de Embeddings**

- **Como** el sistema
- **Quiero** poder cachear embeddings de consultas recientes
- **Para** evitar regenerar vectores para consultas similares
- **Estado**: 📋 **PENDIENTE** - Implementar caché de vectores, estrategia de expiración

**HU-BE-KB-023: Optimización de Consultas Complejas**

- **Como** el sistema
- **Quiero** optimizar el rendimiento de consultas que combinan búsqueda vectorial y
  filtros tradicionales
- **Para** mantener tiempos de respuesta rápidos incluso en consultas complejas
- **Estado**: 📋 **PENDIENTE** - Implementar estrategias de optimización, índices
  compuestos

### Administración del Sistema

**HU-BE-KB-024: Configuración del Servicio**

- **Como** un Administrador
- **Quiero** poder configurar parámetros del servicio con `PUT /api/v1/kb/admin/config`
- **Para** ajustar el comportamiento del sistema sin requerir redeployment
- **Estado**: 📋 **PENDIENTE** - Implementar gestión de configuración, validación de
  parámetros

**HU-BE-KB-025: Monitoreo de Salud del Servicio**

- **Como** un Administrador
- **Quiero** poder verificar el estado del servicio con `GET /api/v1/kb/admin/health`
- **Para** detectar y resolver problemas rápidamente
- **Estado**: 📋 **PENDIENTE** - Implementar health checks, monitoreo de componentes

**HU-BE-KB-026: Backup y Restauración**

- **Como** un Administrador
- **Quiero** poder realizar backups y restauraciones de la base de conocimiento
- **Para** prevenir pérdida de datos y facilitar migraciones
- **Estado**: 📋 **PENDIENTE** - Implementar mecanismos de backup/restore, validación de
  integridad

**HU-BE-KB-027: Gestión de Versiones de Contenido**

- **Como** un Administrador
- **Quiero** poder ver y gestionar versiones de elementos de conocimiento
- **Para** mantener un historial de cambios y poder revertir modificaciones incorrectas
- **Estado**: 📋 **PENDIENTE** - Implementar versionado de contenido, comparación de
  versiones