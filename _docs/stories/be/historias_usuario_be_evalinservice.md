# Historias de Usuario - Backend (BE) - Evaluación de Instructores (evalinservice)

**Actualizado: 7 de junio de 2025**

Estas historias describen las funcionalidades de la API del servicio de Evaluación de Instructores (evalinservice) desde la perspectiva del consumidor (principalmente el Frontend), basadas en los requisitos funcionales del módulo EVALIN.

## 📋 Documentación de Referencia

- **[Requisitos Funcionales](../../general/rf.md)**: Contexto y requisitos generales del sistema
- **[Especificación de Endpoints API](../../api/endpoints_specification.md)**: Define todos los endpoints, formatos y contratos

## 🏷️ Estados de Implementación

- **Pendiente**: Funcionalidad completamente desarrollada y verificada
- 🚧 **En desarrollo**: Funcionalidad parcialmente implementada o en progreso
- 📋 **Pendiente**: Funcionalidad planificada pero aún no desarrollada
- ❌ **Bloqueado**: Requiere dependencias o revisión de diseño

## 👨‍💼 Gestión de Preguntas y Cuestionarios

**HU-BE-EVALIN-001: Gestión de Preguntas de Evaluación**

- **Como** el Frontend (con token válido de administrador)
- **Quiero** poder realizar operaciones CRUD sobre preguntas de evaluación con los endpoints:
  - `POST /api/v1/evalin/questions` (crear)
  - `GET /api/v1/evalin/questions` (listar)
  - `GET /api/v1/evalin/questions/{id}` (obtener)
  - `PUT /api/v1/evalin/questions/{id}` (actualizar)
  - `DELETE /api/v1/evalin/questions/{id}` (eliminar)
- **Para** gestionar las preguntas que se usarán en los cuestionarios de evaluación
- **Estado**: **Pendiente** - Incluye validación de campos, almacenamiento en DB, manejo de errores y pruebas unitarias

**HU-BE-EVALIN-002: Agrupar Preguntas en Cuestionarios**

- **Como** el Frontend (con token válido de administrador)
- **Quiero** poder gestionar cuestionarios y asignar preguntas a ellos con los endpoints:
  - `POST /api/v1/evalin/questionnaires` (crear)
  - `GET /api/v1/evalin/questionnaires` (listar)
  - `GET /api/v1/evalin/questionnaires/{id}` (obtener)
  - `PUT /api/v1/evalin/questionnaires/{id}` (actualizar)
  - `DELETE /api/v1/evalin/questionnaires/{id}` (eliminar)
  - `POST /api/v1/evalin/questionnaires/{id}/questions` (asignar preguntas)
  - `DELETE /api/v1/evalin/questionnaires/{id}/questions/{questionId}` (desasignar pregunta)
- **Para** definir los instrumentos de evaluación que se aplicarán a los instructores
- **Estado**: **Pendiente** - Incluye validación de relaciones, integridad referencial, ordenamiento de preguntas y pruebas unitarias

**HU-BE-EVALIN-003: Definir Periodos de Evaluación**

- **Como** el Frontend (con token válido de administrador)
- **Quiero** poder gestionar periodos de evaluación con los endpoints:
  - `POST /api/v1/evalin/periods` (crear)
  - `GET /api/v1/evalin/periods` (listar)
  - `GET /api/v1/evalin/periods/{id}` (obtener)
  - `PUT /api/v1/evalin/periods/{id}` (actualizar)
  - `DELETE /api/v1/evalin/periods/{id}` (eliminar)
  - `POST /api/v1/evalin/periods/{id}/activate` (activar)
  - `POST /api/v1/evalin/periods/{id}/deactivate` (desactivar)
- **Para** controlar el proceso de evaluación y asegurar que se realice en los momentos oportunos
- **Estado**: **Pendiente** - Incluye validación de fechas, manejo de estados, filtrado por periodo, paginación y control de acceso por rol

**HU-BE-EVALIN-004: Cargar Preguntas desde CSV**

- **Como** el Frontend (con token válido de administrador)
- **Quiero** poder cargar múltiples preguntas desde un archivo CSV con `POST /api/v1/evalin/questions/upload`
- **Para** agregar o actualizar preguntas de forma masiva y eficiente
- **Estado**: **Pendiente** - Incluye validación de formato CSV, procesamiento por lotes, reporte de errores detallado y manejo transaccional

## 📝 Gestión de Evaluaciones

**HU-BE-EVALIN-005: Obtener Instructores a Evaluar**

- **Como** el Frontend (con token válido de aprendiz)
- **Quiero** poder obtener la lista de instructores evaluables con `GET /api/v1/evalin/instructors-to-evaluate`
- **Para** mostrar al aprendiz los instructores que puede evaluar según sus fichas activas y periodos abiertos
- **Estado**: 📋 **Pendiente** - Implementar filtrado por ficha, periodo, estado de evaluación

**HU-BE-EVALIN-006: Obtener Cuestionario para Evaluación**

- **Como** el Frontend (con token válido de aprendiz)
- **Quiero** poder obtener el cuestionario asignado a un instructor con `GET /api/v1/evalin/questionnaires/for-instructor/{instructorId}`
- **Para** mostrar al aprendiz las preguntas que debe responder para evaluar al instructor
- **Estado**: **Pendiente** - Incluye selección de cuestionario según periodo activo, validación de permisos y metadatos del periodo

**HU-BE-EVALIN-007: Enviar Evaluación Completada**

- **Como** el Frontend (con token válido de aprendiz)
- **Quiero** poder enviar una evaluación completada con `POST /api/v1/evalin/evaluations`
- **Para** almacenar las respuestas del aprendiz sobre un instructor específico
- **Estado**: **Pendiente** - Incluye validación de respuestas completas, verificación de permisos y almacenamiento seguro

**HU-BE-EVALIN-008: Verificar Estado de Evaluaciones**

- **Como** el Frontend (con token válido de aprendiz)
- **Quiero** poder verificar qué instructores ya he evaluado con `GET /api/v1/evalin/my-evaluations`
- **Para** mostrar al aprendiz su progreso en el proceso de evaluación
- **Estado**: **Pendiente** - Incluye filtrado por periodo, estado de evaluación y metadatos de periodos activos

## 📊 Reportes y Visualización

**HU-BE-EVALIN-009: Obtener Resultados Consolidados**

- **Como** el Frontend (con token válido de administrador o instructor autorizado)
- **Quiero** poder obtener resultados consolidados de evaluaciones con:
  - `GET /api/v1/evalin/reports/instructor/{instructorId}` (para un instructor)
  - `GET /api/v1/evalin/reports/program/{programId}` (para un programa)
  - `GET /api/v1/evalin/reports/ficha/{fichaId}` (para una ficha)
- **Para** mostrar estadísticas y análisis de las evaluaciones realizadas
- **Estado**: 📋 **Pendiente** - Implementar agregación de datos, cálculos estadísticos, anonimización

**HU-BE-EVALIN-010: Obtener Comentarios Cualitativos**

- **Como** el Frontend (con token válido de administrador o instructor autorizado)
- **Quiero** poder obtener comentarios cualitativos anonimizados con `GET /api/v1/evalin/reports/comments/{instructorId}`
- **Para** mostrar retroalimentación textual de los aprendices
- **Estado**: 📋 **Pendiente** - Implementar anonimización robusta, filtrado de contenido inapropiado

**HU-BE-EVALIN-011: Obtener Estado de Participación**

- **Como** el Frontend (con token válido de administrador o director de grupo)
- **Quiero** poder obtener el estado de participación de los aprendices con `GET /api/v1/evalin/reports/participation/{fichaId}`
- **Para** monitorear quién ha completado las evaluaciones y quién no
- **Estado**: **Pendiente** - Implementado con todos los criterios de aceptación

## ⚙️ Configuración y Notificaciones

**HU-BE-EVALIN-012: Gestionar Configuración del Módulo**

- **Como** el Frontend (con token válido de administrador)
- **Quiero** poder gestionar la configuración del módulo con:
  - `GET /api/v1/evalin/config` (obtener configuración)
  - `PUT /api/v1/evalin/config` (actualizar configuración)
- **Para** personalizar el comportamiento del sistema según las políticas institucionales
- **Estado**: 📋 **Pendiente** - Implementar validación de parámetros, valores por defecto

**HU-BE-EVALIN-013: Enviar Notificaciones de Periodos**

- **Como** el sistema
- **Quiero** poder enviar notificaciones automáticas cuando se abran nuevos periodos de evaluación
- **Para** informar a los aprendices que deben realizar evaluaciones
- **Estado**: 📋 **Pendiente** - Implementar integración con sistema de notificaciones, programación de envíos

**HU-BE-EVALIN-014: Enviar Recordatorios de Evaluación**

- **Como** el Frontend (con token válido de administrador o director de grupo)
- **Quiero** poder enviar recordatorios a aprendices con `POST /api/v1/evalin/notifications/reminder/{fichaId}`
- **Para** aumentar la participación en el proceso de evaluación
- **Estado**: 📋 **Pendiente** - Implementar filtrado de destinatarios, plantillas de mensajes
