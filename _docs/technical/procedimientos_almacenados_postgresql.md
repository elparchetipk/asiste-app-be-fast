# Análisis sobre el Uso de Procedimientos Almacenados en API REST con PostgreSQL

**Fecha:** 2 de junio de 2025  
**Autor:** Equipo de Desarrollo Backend  
**Versión:** 1.0

## 📋 Resumen Ejecutivo

Este documento analiza la adecuación y recomendaciones para el uso de procedimientos
almacenados en la API REST de Asiste App que utiliza PostgreSQL como base de datos. Se
evalúan casos de uso potenciales, ventajas, desventajas y se proporcionan recomendaciones
específicas basadas en la arquitectura actual de la aplicación.

## 🔍 Análisis de la Arquitectura Actual

### Patrón de Acceso a Datos

La aplicación actualmente utiliza:

- **Consultas SQL directas** desde el código Go mediante el paquete `database/sql`
- **Transacciones** para operaciones que requieren atomicidad
- **Funciones básicas de PostgreSQL** como triggers para actualización automática de
  timestamps

### Complejidad de Consultas

- La mayoría de las consultas son operaciones CRUD simples
- Algunas operaciones más complejas utilizan transacciones para mantener la integridad de
  los datos
- No se observan consultas analíticas complejas o procesamiento intensivo de datos

## 🎯 Casos de Uso Potenciales para Procedimientos Almacenados

### 1. Operaciones de Negocio Complejas

- **Gestión de asistencia**: Cálculo de estadísticas de asistencia que requieren múltiples
  consultas y lógica compleja
- **Procesamiento de carga masiva**: Validación y procesamiento de datos CSV con reglas de
  negocio complejas
- **Generación de reportes**: Consultas analíticas complejas con múltiples joins y
  agregaciones

### 2. Operaciones de Alta Concurrencia

- **Gestión de tokens**: Invalidación y limpieza de tokens expirados
- **Registro de asistencia**: Operaciones que requieren alta concurrencia y baja latencia

### 3. Validaciones Complejas

- **Validación de horarios**: Verificación de conflictos en la programación de horarios
- **Validación de reglas de negocio**: Reglas complejas que involucran múltiples tablas

## ✅ Ventajas de Usar Procedimientos Almacenados

### 1. Rendimiento

- **Reducción de viajes de red**: Toda la lógica se ejecuta en el servidor de base de
  datos
- **Ejecución optimizada**: PostgreSQL puede optimizar la ejecución de procedimientos
  almacenados
- **Caché de planes de ejecución**: Los planes de ejecución se pueden cachear para
  consultas frecuentes

### 2. Seguridad

- **Control de acceso granular**: Se puede restringir el acceso a tablas y permitir solo
  la ejecución de procedimientos específicos
- **Reducción de superficie de ataque**: Menor riesgo de inyección SQL si todas las
  consultas se realizan a través de procedimientos

### 3. Consistencia y Reutilización

- **Lógica centralizada**: Las reglas de negocio se definen una vez y se aplican
  consistentemente
- **Reutilización de código**: Los procedimientos pueden ser llamados desde diferentes
  partes de la aplicación
- **Mantenimiento simplificado**: Cambios en la lógica de negocio pueden implementarse en
  un solo lugar

## ❌ Desventajas de Usar Procedimientos Almacenados

### 1. Acoplamiento con la Base de Datos

- **Dependencia del proveedor**: Mayor acoplamiento con PostgreSQL, dificultando posibles
  migraciones
- **Dificultad de pruebas**: Las pruebas unitarias son más complejas para procedimientos
  almacenados
- **Versionado más complejo**: El versionado de procedimientos almacenados requiere
  estrategias adicionales

### 2. Desarrollo y Mantenimiento

- **Diferentes lenguajes**: Los desarrolladores deben dominar tanto Go como PL/pgSQL
- **Depuración más compleja**: La depuración de procedimientos almacenados es menos
  directa
- **Herramientas limitadas**: Menos herramientas de desarrollo y análisis estático para
  PL/pgSQL

### 3. Arquitectura de Microservicios

- **Encapsulación de datos**: En una arquitectura de microservicios, cada servicio debería
  tener control total sobre sus datos
- **Escalabilidad**: Puede limitar las opciones de escalabilidad horizontal si la lógica
  está en la base de datos

## 🔄 Impacto en Mantenibilidad, Escalabilidad y Rendimiento

### Mantenibilidad

- **Positivo**: Centralización de lógica compleja, reducción de código duplicado
- **Negativo**: Fragmentación de la lógica entre Go y PL/pgSQL, mayor curva de aprendizaje

### Escalabilidad

- **Positivo**: Mejor rendimiento para operaciones complejas, reducción de carga en la
  aplicación
- **Negativo**: Posible cuello de botella en la base de datos, limitaciones para escalar
  horizontalmente

### Rendimiento

- **Positivo**: Reducción de latencia para operaciones complejas, optimización de
  consultas
- **Negativo**: Posible sobrecarga para operaciones simples, mayor uso de recursos en la
  base de datos

## 🌟 Mejores Prácticas Actuales

### Enfoque Híbrido

La tendencia actual en aplicaciones modernas con Go y PostgreSQL es un enfoque híbrido:

1. **Lógica de aplicación en Go**: La mayoría de la lógica de negocio permanece en el
   código Go
2. **Procedimientos almacenados para casos específicos**: Utilizar procedimientos solo
   donde ofrecen claras ventajas

### Casos Recomendados para Procedimientos Almacenados

- Operaciones que requieren múltiples consultas y alta atomicidad
- Consultas analíticas complejas con múltiples joins y agregaciones
- Operaciones de alta concurrencia que se benefician de la reducción de viajes de red
- Validaciones complejas que involucran múltiples tablas

### Casos No Recomendados para Procedimientos Almacenados

- Operaciones CRUD simples
- Lógica de negocio que cambia frecuentemente
- Funcionalidades que podrían necesitar escalarse independientemente de la base de datos

## 📊 Recomendaciones para Asiste App

Basado en el análisis de la arquitectura actual y los patrones de acceso a datos,
recomendamos:

### 1. Uso Selectivo de Procedimientos Almacenados

Implementar procedimientos almacenados solo para casos específicos donde ofrezcan claras
ventajas:

- **Estadísticas de asistencia**: Cálculos complejos de porcentajes y tendencias
- **Validación de horarios**: Verificación de conflictos en la programación
- **Limpieza automática de datos**: Eliminación periódica de tokens expirados y datos
  temporales

### 2. Mantener la Lógica Principal en Go

- Continuar implementando la mayoría de la lógica de negocio en Go
- Utilizar transacciones para operaciones que requieren atomicidad
- Mantener las consultas SQL en el código Go para operaciones CRUD estándar

### 3. Implementar Funciones de Base de Datos para Operaciones Específicas

- Crear funciones PostgreSQL para operaciones comunes que se beneficien de la ejecución en
  la base de datos
- Documentar claramente estas funciones y su propósito
- Incluir pruebas específicas para estas funciones

### 4. Estrategia de Migración y Versionado

- Implementar un sistema robusto de migraciones que incluya versionado de procedimientos
  almacenados
- Documentar todos los procedimientos almacenados en la documentación del proyecto
- Incluir comentarios detallados en los procedimientos almacenados

## 🔧 Ejemplos de Implementación Recomendada

### Ejemplo 1: Función para Estadísticas de Asistencia

```sql
CREATE
OR REPLACE FUNCTION get_attendance_statistics(
    p_ficha_id INTEGER,
    p_start_date DATE,
    p_end_date DATE
)
RETURNS TABLE (
    total_sessions INTEGER,
    attended_sessions INTEGER,
    justified_absences INTEGER,
    unjustified_absences INTEGER,
    attendance_percentage NUMERIC
) AS $$
BEGIN
RETURN QUERY WITH stats AS (
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) AS present,
            SUM(CASE WHEN status = 'justified' THEN 1 ELSE 0 END) AS justified,
            SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) AS absent
        FROM attendance
        WHERE ficha_id = p_ficha_id
        AND DATE BETWEEN p_start_date AND p_end_date
    )
SELECT total     AS total_sessions,
       present   AS attended_sessions,
       justified AS justified_absences,
       absent    AS unjustified_absences,
       CASE
         WHEN total > 0 THEN
           ROUND((present::NUMERIC / total::NUMERIC) * 100, 2)
         ELSE
           0
         END     AS attendance_percentage
FROM stats;
END;
$$
LANGUAGE plpgsql;
```

### Ejemplo 2: Procedimiento para Validación de Horarios

```sql
CREATE
OR REPLACE FUNCTION validate_schedule_conflicts(
    p_instructor_id INTEGER,
    p_ambiente_id INTEGER,
    p_ficha_id INTEGER,
    p_date DATE,
    p_start_time TIME,
    p_end_time TIME,
    p_schedule_id INTEGER DEFAULT NULL
)
RETURNS TABLE (
    conflict_type TEXT,
    conflicting_id INTEGER,
    conflict_details TEXT
) AS $$
BEGIN
    -- Verificar conflictos de instructor
RETURN QUERY
SELECT 'instructor'::TEXT AS conflict_type, id AS conflicting_id,
       'El instructor ya tiene asignado otro horario en este periodo'::TEXT AS conflict_details
FROM schedule
WHERE instructor_id = p_instructor_id
  AND DATE = p_date
  AND (
    (start_time <= p_start_time
  AND end_time
    > p_start_time)
   OR
    (start_time
    < p_end_time
  AND end_time >= p_end_time)
   OR
    (start_time >= p_start_time
  AND end_time <= p_end_time)
  )
  AND (p_schedule_id IS NULL
   OR id != p_schedule_id);

-- Verificar conflictos de ambiente
RETURN QUERY
SELECT 'ambiente'::TEXT AS conflict_type, id AS conflicting_id,
       'El ambiente ya está ocupado en este periodo'::TEXT AS conflict_details
FROM schedule
WHERE ambiente_id = p_ambiente_id
  AND DATE = p_date
  AND (
    (start_time <= p_start_time
  AND end_time
    > p_start_time)
   OR
    (start_time
    < p_end_time
  AND end_time >= p_end_time)
   OR
    (start_time >= p_start_time
  AND end_time <= p_end_time)
  )
  AND (p_schedule_id IS NULL
   OR id != p_schedule_id);

-- Verificar conflictos de ficha
RETURN QUERY
SELECT 'ficha'::TEXT AS conflict_type, id AS conflicting_id,
       'La ficha ya tiene asignado otro horario en este periodo'::TEXT AS conflict_details
FROM schedule
WHERE ficha_id = p_ficha_id
  AND DATE = p_date
  AND (
    (start_time <= p_start_time
  AND end_time
    > p_start_time)
   OR
    (start_time
    < p_end_time
  AND end_time >= p_end_time)
   OR
    (start_time >= p_start_time
  AND end_time <= p_end_time)
  )
  AND (p_schedule_id IS NULL
   OR id != p_schedule_id);
END;
$$
LANGUAGE plpgsql;
```

## 📝 Conclusión

El uso de procedimientos almacenados en la API REST de Asiste App con PostgreSQL puede ser
beneficioso en casos específicos, pero debe ser implementado de manera selectiva y
estratégica. Recomendamos un enfoque híbrido que mantenga la mayoría de la lógica en el
código Go, utilizando procedimientos almacenados solo para operaciones donde ofrezcan
claras ventajas en términos de rendimiento, seguridad o consistencia.

La decisión de implementar procedimientos almacenados debe basarse en un análisis caso por
caso, considerando factores como la complejidad de la operación, la frecuencia de uso, los
requisitos de rendimiento y el impacto en la mantenibilidad y escalabilidad de la
aplicación.