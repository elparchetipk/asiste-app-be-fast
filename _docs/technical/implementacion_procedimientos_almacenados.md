# Implementación de Procedimientos Almacenados en PostgreSQL

**Fecha:** 2 de junio de 2025  
**Autor:** Equipo de Desarrollo Backend  
**Versión:** 1.0

## 📋 Resumen Ejecutivo

Este documento describe la implementación de procedimientos almacenados en PostgreSQL para la API REST de Asiste App, siguiendo las recomendaciones del documento [Análisis sobre el Uso de Procedimientos Almacenados en API REST con PostgreSQL](procedimientos_almacenados_postgresql.md). Se han implementado tres procedimientos almacenados para optimizar operaciones complejas, garantizar la consistencia de datos y automatizar tareas de mantenimiento.

## 🎯 Procedimientos Implementados

### 1. Estadísticas de Asistencia (`get_attendance_statistics`)

**Historia de Usuario:** HU-BE-047

**Propósito:** Optimizar el cálculo de estadísticas de asistencia con múltiples consultas y lógica compleja.

**Implementación:**
- Archivo: `docker-entrypoint-initdb.d/02-stored-procedures.sql`
- Función: `get_attendance_statistics`
- Parámetros:
  - `p_aprendiz_id VARCHAR`: ID del aprendiz (opcional)
  - `p_ficha_id VARCHAR`: ID de la ficha (opcional)
  - `p_instructor_id VARCHAR`: ID del instructor (opcional)
  - `p_start_date DATE`: Fecha de inicio (opcional)
  - `p_end_date DATE`: Fecha de fin (opcional)
- Retorna: Tabla con estadísticas de asistencia (total de sesiones, asistencias, ausencias justificadas, ausencias injustificadas, tardanzas, porcentaje de asistencia)

**Integración en la Aplicación:**
- Archivo: `attendanceservice/app/crud.py`
- Función: `get_resumen_asistencia`
- Endpoint: `GET /api/v1/attendance/summary`

**Ventajas:**
- Reduce múltiples consultas a una sola, mejorando el rendimiento
- Centraliza la lógica de cálculo de estadísticas
- Facilita el mantenimiento al tener la lógica en un solo lugar

### 2. Validación de Horarios (`validate_schedule_conflicts`)

**Historia de Usuario:** HU-BE-048

**Propósito:** Verificar eficientemente conflictos en la programación de horarios.

**Implementación:**
- Archivo: `docker-entrypoint-initdb.d/02-stored-procedures.sql`
- Función: `validate_schedule_conflicts`
- Parámetros:
  - `p_instructor_id VARCHAR`: ID del instructor
  - `p_ambiente_id INTEGER`: ID del ambiente
  - `p_ficha_id INTEGER`: ID de la ficha
  - `p_dia_semana VARCHAR`: Día de la semana
  - `p_hora_inicio TIME`: Hora de inicio
  - `p_hora_fin TIME`: Hora de fin
  - `p_horario_id INTEGER`: ID del horario a excluir (opcional)
- Retorna: Tabla con conflictos encontrados (tipo de conflicto, ID del horario conflictivo, detalles del conflicto)

**Integración en la Aplicación:**
- Archivo: `scheduleservice/app/routers/schedule.py`
- Endpoints:
  - `POST /horarios/`: Creación de horarios
  - `PUT /horarios/{horario_id}`: Actualización de horarios

**Ventajas:**
- Garantiza la consistencia en la validación de horarios
- Detecta conflictos para instructores, ambientes y fichas
- Mejora la experiencia del usuario al proporcionar mensajes de error específicos

### 3. Limpieza Automática de Tokens (`cleanup_expired_tokens`)

**Historia de Usuario:** HU-BE-049

**Propósito:** Mejorar el rendimiento y mantenimiento de la base de datos mediante la limpieza automática de tokens expirados.

**Implementación:**
- Archivo: `docker-entrypoint-initdb.d/02-stored-procedures.sql`
- Función: `cleanup_expired_tokens`
- Parámetros: Ninguno
- Retorna: Número de tokens eliminados

**Integración en la Aplicación:**
- Script: `scripts/cleanup_tokens.sh`
- Configuración: Cron job para ejecución periódica (documentado en `scripts/README.md`)

**Ventajas:**
- Automatiza tareas de mantenimiento
- Mejora el rendimiento de la base de datos
- Reduce el tamaño de la base de datos

## 🔄 Cambios Realizados

### Archivos Creados

1. `docker-entrypoint-initdb.d/02-stored-procedures.sql`: Implementación de los procedimientos almacenados.
2. `scripts/cleanup_tokens.sh`: Script para ejecutar periódicamente la limpieza de tokens expirados.
3. `scripts/README.md`: Documentación sobre cómo configurar y ejecutar el script de limpieza de tokens.
4. `_docs/technical/implementacion_procedimientos_almacenados.md`: Este documento.

### Archivos Modificados

1. `attendanceservice/app/crud.py`: Actualización de la función `get_resumen_asistencia` para utilizar el procedimiento almacenado `get_attendance_statistics`.
2. `scheduleservice/app/routers/schedule.py`: Actualización de los endpoints de creación y actualización de horarios para utilizar el procedimiento almacenado `validate_schedule_conflicts`.

## 🧪 Pruebas Realizadas

### Estadísticas de Asistencia

Para probar el procedimiento `get_attendance_statistics`:

```sql
SELECT * FROM get_attendance_statistics(NULL, 'ficha123', NULL, '2025-01-01', '2025-01-31');
```

### Validación de Horarios

Para probar el procedimiento `validate_schedule_conflicts`:

```sql
SELECT * FROM validate_schedule_conflicts('instructor123', 1, 1, 'Lunes', '08:00:00', '10:00:00');
```

### Limpieza de Tokens

Para probar el procedimiento `cleanup_expired_tokens`:

```sql
SELECT cleanup_expired_tokens();
```

## 📝 Conclusiones

La implementación de procedimientos almacenados en PostgreSQL ha permitido optimizar operaciones complejas, garantizar la consistencia de datos y automatizar tareas de mantenimiento en la API REST de Asiste App. Se ha seguido un enfoque híbrido, manteniendo la mayoría de la lógica en el código de la aplicación y utilizando procedimientos almacenados solo para casos específicos donde ofrecen claras ventajas.

Los procedimientos implementados han mejorado el rendimiento, la seguridad y la consistencia de la aplicación, siguiendo las recomendaciones del documento de análisis y las historias de usuario definidas.

## 📚 Referencias

- [Análisis sobre el Uso de Procedimientos Almacenados en API REST con PostgreSQL](procedimientos_almacenados_postgresql.md)
- [Historias de Usuario - Procedimientos Almacenados PostgreSQL](../stories/be/historias_usuario_be_procedimientos.md)