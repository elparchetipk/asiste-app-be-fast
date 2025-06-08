# Historias de Usuario - Frontend (FE) - Evaluación de Instructores (evalinservice)

**Actualizado: 1 de junio de 2025**

Estas historias describen las funcionalidades del frontend para el servicio de Evaluación de Instructores (evalinservice) desde la perspectiva del usuario final. El estado actual de implementación se indica con los siguientes marcadores:

- ✅ **Implementado**: Funcionalidad completamente desarrollada y disponible.
- 🚧 **En desarrollo**: Funcionalidad parcialmente implementada o en progreso.
- 📋 **Pendiente**: Funcionalidad planificada pero aún no desarrollada.
- ❌ **Bloqueado**: Requiere dependencias o revisión de diseño.

## Panel de Administración

### HU-FE-EVALIN-001: Gestión de Preguntas de Evaluación
- **Como** Administrador
- **Quiero** poder crear, editar, visualizar y eliminar preguntas para los cuestionarios de evaluación
- **Para** asegurar que las evaluaciones contengan las preguntas adecuadas y actualizadas según las dimensiones a evaluar.
- **Estado**: 📋 **Pendiente** (requiere implementación en app/admin/evalin/questions.tsx).

### HU-FE-EVALIN-002: Agrupar Preguntas en Cuestionarios
- **Como** Administrador
- **Quiero** poder crear cuestionarios y asignar preguntas a ellos, organizándolas en secciones y estableciendo su orden
- **Para** definir los instrumentos de evaluación que se aplicarán a los instructores.
- **Estado**: 📋 **Pendiente** (requiere implementación en app/admin/evalin/questionnaires.tsx).

### HU-FE-EVALIN-003: Definir Periodos de Evaluación
- **Como** Administrador
- **Quiero** poder definir y gestionar los periodos durante los cuales los aprendices podrán realizar las evaluaciones
- **Para** controlar el proceso de evaluación y asegurar que se realice en los momentos oportunos.
- **Estado**: 📋 **Pendiente** (requiere implementación en app/admin/evalin/periods.tsx).

### HU-FE-EVALIN-004: Consultar Reportes Consolidados de Evaluación
- **Como** Administrador
- **Quiero** poder visualizar reportes consolidados de los resultados de las evaluaciones con gráficos y tablas
- **Para** analizar el desempeño de los instructores y tomar decisiones informadas.
- **Estado**: 📋 **Pendiente** (requiere implementación en app/admin/evalin/reports.tsx).

### HU-FE-EVALIN-005: Configurar Parámetros del Módulo de Evaluación
- **Como** Administrador
- **Quiero** poder configurar parámetros generales del módulo de EVALIN mediante una interfaz intuitiva
- **Para** adaptar el funcionamiento del módulo a las políticas de la institución.
- **Estado**: 📋 **Pendiente** (requiere implementación en app/admin/evalin/settings.tsx).

### HU-FE-EVALIN-006: Dashboard de Seguimiento para Directores de Grupo
- **Como** Administrador o Instructor con rol de Director de Grupo
- **Quiero** tener un dashboard para visualizar el estado de las evaluaciones en las fichas
- **Para** poder realizar seguimiento y enviar recordatorios a los aprendices.
- **Estado**: 📋 **Pendiente** (requiere implementación en app/admin/evalin/dashboard.tsx y app/instructor/evalin/dashboard.tsx).

### HU-FE-EVALIN-007: Cargar Preguntas desde CSV
- **Como** Administrador
- **Quiero** poder cargar múltiples preguntas de evaluación desde un archivo CSV
- **Para** agregar o actualizar preguntas de forma masiva y eficiente.
- **Estado**: 📋 **Pendiente** (requiere implementación en app/admin/evalin/upload.tsx).

## Interfaz para Aprendices

### HU-FE-EVALIN-008: Visualizar Instructores a Evaluar
- **Como** Aprendiz
- **Quiero** poder visualizar la lista de instructores que me han impartido formación y que puedo evaluar
- **Para** seleccionar al instructor que deseo evaluar.
- **Estado**: 📋 **Pendiente** (requiere implementación en app/evalin/instructors.tsx).

### HU-FE-EVALIN-009: Responder Cuestionario de Evaluación
- **Como** Aprendiz
- **Quiero** poder responder el cuestionario de evaluación para un instructor específico, viendo su foto para fácil identificación
- **Para** proporcionar mi retroalimentación sobre su desempeño.
- **Estado**: 📋 **Pendiente** (requiere implementación en app/evalin/questionnaire/[instructorId].tsx).

### HU-FE-EVALIN-010: Enviar Evaluación Completada
- **Como** Aprendiz
- **Quiero** poder enviar mi evaluación una vez que haya respondido todas las preguntas del cuestionario
- **Para** que mis respuestas sean registradas en el sistema.
- **Estado**: 📋 **Pendiente** (requiere implementación en componentes/EvaluationSubmitButton.tsx).

### HU-FE-EVALIN-011: Visualizar Resumen de Evaluaciones Enviadas
- **Como** Aprendiz
- **Quiero** poder visualizar un resumen o confirmación de las evaluaciones que he enviado
- **Para** tener un registro personal de mis evaluaciones completadas.
- **Estado**: 📋 **Pendiente** (requiere implementación en app/evalin/my-evaluations.tsx).

## Interfaz para Instructores

### HU-FE-EVALIN-012: Visualizar Resultados Consolidados de Evaluaciones
- **Como** Instructor
- **Quiero** poder visualizar los resultados consolidados y anonimizados de mis evaluaciones
- **Para** conocer la percepción de los aprendices sobre mi desempeño e identificar áreas de mejora.
- **Estado**: 📋 **Pendiente** (requiere implementación en app/instructor/evalin/results.tsx).

### HU-FE-EVALIN-013: Visualizar Comentarios Cualitativos Anonimizados
- **Como** Instructor
- **Quiero** poder visualizar los comentarios cualitativos de forma anonimizada
- **Para** obtener retroalimentación más detallada y específica de los aprendices.
- **Estado**: 📋 **Pendiente** (requiere implementación en app/instructor/evalin/comments.tsx).

### HU-FE-EVALIN-014: Cargar Foto de Perfil
- **Como** Instructor
- **Quiero** poder cargar o actualizar mi foto de perfil en el sistema
- **Para** que los aprendices puedan identificarme fácilmente al momento de seleccionarme para la evaluación.
- **Estado**: 📋 **Pendiente** (requiere implementación en app/profile/photo.tsx).

## Notificaciones y Recordatorios

### HU-FE-EVALIN-015: Recibir Notificaciones de Periodos de Evaluación
- **Como** Aprendiz
- **Quiero** recibir notificaciones en la aplicación cuando se abran nuevos periodos de evaluación
- **Para** estar informado y no olvidar realizar las evaluaciones.
- **Estado**: 📋 **Pendiente** (requiere implementación en componentes/NotificationSystem.tsx).

### HU-FE-EVALIN-016: Recibir Recordatorios de Evaluación
- **Como** Aprendiz
- **Quiero** recibir notificaciones de recordatorio antes de que finalice un periodo de evaluación
- **Para** asegurar mi participación en el proceso.
- **Estado**: 📋 **Pendiente** (requiere implementación en componentes/NotificationSystem.tsx).

### HU-FE-EVALIN-017: Enviar Recordatorios Manuales
- **Como** Administrador o Director de Grupo
- **Quiero** poder enviar recordatorios manuales a los aprendices que no han completado sus evaluaciones
- **Para** aumentar la participación en el proceso de evaluación.
- **Estado**: 📋 **Pendiente** (requiere implementación en app/admin/evalin/send-reminders.tsx).

## 📊 Resumen de Estado

### 📋 Funcionalidades Pendientes (17)

- 📋 Panel de administración completo para gestión de preguntas, cuestionarios y periodos
- 📋 Reportes y configuración del módulo de evaluación
- 📋 Interfaz para que los aprendices realicen evaluaciones
- 📋 Visualización de resultados para instructores
- 📋 Sistema de notificaciones y recordatorios

**Total de Historias:** 17  
**Progreso:** 0% implementado, 0% en desarrollo, 100% pendiente