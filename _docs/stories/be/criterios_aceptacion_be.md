# Criterios de Aceptación - Historias de Usuario Backend

**Actualizado: 1 de junio de 2025**

Este documento define los criterios de aceptación detallados para las historias de usuario
del backend, proporcionando una guía clara para la implementación y verificación de cada
funcionalidad.

## 📋 Documentación de Referencia

- **[Historias de Usuario Backend](historias_usuario_be.md)**: Especifica
  las funcionalidades desde la perspectiva del consumidor de la API.
- **[Historias de Usuario KB Service](historias_usuario_be_kbservice.md)
  **: Especifica las funcionalidades del servicio de Knowledge Base.
- **[Requisitos Funcionales](../../general/rf.md)**: Contexto y requisitos generales del
  sistema.
- **[Requisitos Funcionales KB](../../general/rf_kb.md)**: Requisitos específicos del
  Knowledge Base Service.
- - \*[Historias de Usuario EVALIN Service](historias_usuario_be_evalinservice.md)
    \*\*: Especifica las funcionalidades del servicio de Evaluación de Instructores.

## 🏷️ Estados de Implementación

- ✅ **Implementado**: Funcionalidad completamente desarrollada y verificada
- 🚧 **En desarrollo**: Funcionalidad parcialmente implementada o en progreso
- 📋 **Pendiente**: Funcionalidad planificada pero aún no desarrollada
- ❌ **Bloqueado**: Requiere dependencias o revisión de diseño

## 🔐 Autenticación y Usuarios (User Service)

### Autenticación

✅ **HU-BE-001: Registro de Usuario**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/auth/register` debe validar todos los campos requeridos (
   nombre, apellido, email, documento, contraseña) y retornar errores específicos para
   cada campo inválido.
2. El sistema debe verificar que el email y documento no existan previamente en la base de
   datos, retornando un error específico si ya están registrados.
3. La contraseña debe cumplir con los requisitos de seguridad (mínimo 10 caracteres, al
   menos una mayúscula, una minúscula, un dígito y un símbolo).
4. El sistema debe almacenar la contraseña utilizando un algoritmo de hash seguro (
   bcrypt).
5. Al registrarse exitosamente, el sistema debe retornar un código 201 (Created) con los
   datos del usuario creado (sin la contraseña).
6. El sistema debe establecer el flag `must_change_password` en `true` para usuarios
   creados mediante este endpoint.
7. El sistema debe asignar automáticamente el rol por defecto (aprendiz) a menos que se
   especifique otro rol y el usuario tenga permisos para asignarlo.

✅ **HU-BE-002: Login de Usuario**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/auth/login` debe validar las credenciales (email/documento y
   contraseña) y retornar un error específico si son inválidas.
2. Si las credenciales son válidas, el sistema debe generar un token de acceso JWT con
   expiración de 1 hora.
3. El sistema debe generar un token de refresco con expiración más larga (7 días).
4. La respuesta debe incluir ambos tokens, información completa del usuario (sin
   contraseña) y enlaces HATEOAS para operaciones relacionadas.
5. El sistema debe actualizar el campo `last_login` del usuario con la fecha y hora
   actual.
6. Si el usuario tiene el flag `must_change_password` en `true`, la respuesta debe incluir
   esta información para que el frontend redirija al usuario a la pantalla de cambio de
   contraseña.
7. El sistema debe registrar el intento de login (exitoso o fallido) en los logs de
   seguridad.

✅ **HU-BE-003: Refresco de Token**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/auth/refresh` debe validar que el token de refresco sea
   válido y no esté expirado o revocado.
2. Si el token es válido, el sistema debe generar un nuevo token de acceso con expiración
   de 1 hora.
3. El sistema debe actualizar el campo `last_login` del usuario con la fecha y hora
   actual.
4. La respuesta debe incluir el nuevo token de acceso, manteniendo el mismo token de
   refresco.
5. Si el token de refresco es inválido, expirado o ha sido revocado, el sistema debe
   retornar un error 401 (Unauthorized).
6. El sistema debe registrar la operación de refresco en los logs de seguridad.

✅ **HU-BE-004: Cerrar Sesión**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/auth/logout` debe requerir un token de acceso válido.
2. El sistema debe invalidar el token de refresco asociado al usuario, agregándolo a una
   lista de tokens revocados.
3. La respuesta debe tener un código 200 (OK) con un mensaje de confirmación.
4. El sistema debe registrar la operación de logout en los logs de seguridad.
5. Si se intenta usar un token de refresco revocado, el sistema debe rechazar la solicitud
   con un error 401 (Unauthorized).

✅ **HU-BE-005: Solicitar Restablecimiento de Contraseña**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/auth/forgot-password` debe validar que el email proporcionado
   exista en la base de datos.
2. El sistema debe generar un token seguro con expiración de 24 horas.
3. El sistema debe almacenar el token en la base de datos, asociado al usuario.
4. El sistema debe invalidar cualquier token de restablecimiento previo para ese usuario.
5. El sistema debe enviar un email al usuario con un enlace que incluya el token para
   restablecer la contraseña.
6. La respuesta debe tener un código 200 (OK) incluso si el email no existe (por
   seguridad).
7. El sistema debe registrar la solicitud en los logs de seguridad.

✅ **HU-BE-006: Restablecer Contraseña**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/auth/reset-password` debe validar que el token proporcionado
   sea válido, exista en la base de datos y no haya expirado.
2. El sistema debe validar que la nueva contraseña cumpla con los requisitos de seguridad.
3. Si el token y la contraseña son válidos, el sistema debe actualizar la contraseña del
   usuario utilizando un algoritmo de hash seguro.
4. El sistema debe invalidar el token utilizado para evitar su reutilización.
5. El sistema debe invalidar todos los tokens de refresco existentes para ese usuario.
6. La respuesta debe tener un código 200 (OK) con un mensaje de confirmación.
7. El sistema debe registrar la operación en los logs de seguridad.

✅ **HU-BE-007: Cambio Forzado de Contraseña**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/auth/force-change-password` debe requerir un token de acceso
   válido.
2. El sistema debe verificar que el usuario tenga el flag `must_change_password` en
   `true`.
3. El sistema debe validar que la nueva contraseña cumpla con los requisitos de seguridad.
4. El sistema debe validar que la nueva contraseña sea diferente a la contraseña actual.
5. Si la validación es exitosa, el sistema debe actualizar la contraseña y establecer el
   flag `must_change_password` en `false`.
6. El sistema debe invalidar todos los tokens de refresco existentes excepto el actual.
7. La respuesta debe tener un código 200 (OK) con un mensaje de confirmación.

### Gestión de Perfil de Usuario

✅ **HU-BE-008: Obtener Perfil de Usuario**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/users/profile` debe requerir un token de acceso válido.
2. El sistema debe retornar la información completa del usuario autenticado (sin la
   contraseña).
3. La respuesta debe incluir todos los campos relevantes: id, nombre, apellido, email,
   documento, rol, fecha de creación, última actualización, último login.
4. La respuesta debe incluir enlaces HATEOAS para operaciones relacionadas con el perfil.
5. La respuesta debe tener un código 200 (OK).

✅ **HU-BE-009: Actualizar Perfil de Usuario**

**Criterios de Aceptación:**

1. El endpoint `PUT /api/v1/users/profile` debe requerir un token de acceso válido.
2. El sistema debe validar los campos editables (nombre, apellido, email, teléfono).
3. Si se actualiza el email, el sistema debe verificar que no exista previamente para otro
   usuario.
4. El sistema debe rechazar intentos de modificar campos no editables por el usuario (
   documento, rol, flags de sistema).
5. Si la validación es exitosa, el sistema debe actualizar la información del usuario y el
   campo `updated_at`.
6. La respuesta debe incluir la información actualizada del usuario.
7. La respuesta debe tener un código 200 (OK).

✅ **HU-BE-010: Cambiar Contraseña (Usuario Autenticado)**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/users/change-password` debe requerir un token de acceso
   válido.
2. El sistema debe validar que la contraseña actual proporcionada sea correcta.
3. El sistema debe validar que la nueva contraseña cumpla con los requisitos de seguridad.
4. El sistema debe validar que la nueva contraseña sea diferente a la contraseña actual.
5. Si la validación es exitosa, el sistema debe actualizar la contraseña utilizando un
   algoritmo de hash seguro.
6. El sistema debe invalidar todos los tokens de refresco existentes excepto el actual.
7. La respuesta debe tener un código 200 (OK) con un mensaje de confirmación.

## 👥 Administración de Usuarios (Admin Service)

### Gestión CRUD de Usuarios

**HU-BE-011: Listar Usuarios (Admin)**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/users/` debe requerir un token de acceso válido con rol de
   administrador.
2. El sistema debe retornar una lista paginada de usuarios ordenados por ID de forma
   descendente por defecto.
3. El sistema debe permitir filtrar por rol, estado (activo/inactivo) y término de
   búsqueda (nombre, apellido, email, documento).
4. El sistema debe permitir cambiar el ordenamiento por diferentes campos y dirección (
   asc/desc).
5. La respuesta debe incluir metadatos de paginación (total de registros, página actual,
   total de páginas).
6. Cada usuario en la lista debe incluir información básica (sin contraseña) y enlaces
   HATEOAS para operaciones relacionadas.
7. La respuesta debe tener un código 200 (OK).

**HU-BE-012: Crear Usuario (Admin)**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/admin/users` debe requerir un token de acceso válido con rol
   de administrador.
2. El sistema debe validar todos los campos requeridos y retornar errores específicos para
   cada campo inválido.
3. El sistema debe verificar que el email y documento no existan previamente en la base de
   datos.
4. El sistema debe permitir asignar cualquier rol válido al nuevo usuario.
5. El sistema debe generar una contraseña inicial igual al número de documento y
   establecer el flag `must_change_password` en `true`.
6. El sistema debe almacenar la contraseña utilizando un algoritmo de hash seguro.
7. La respuesta debe incluir los datos del usuario creado (sin la contraseña) y tener un
   código 201 (Created).

**HU-BE-013: Obtener Usuario Específico (Admin)**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/admin/users/:id` debe requerir un token de acceso válido con
   rol de administrador.
2. El sistema debe validar que el ID proporcionado exista en la base de datos.
3. El sistema debe retornar la información completa del usuario (sin la contraseña).
4. La respuesta debe incluir todos los campos relevantes, incluyendo flags del sistema y
   timestamps.
5. La respuesta debe incluir enlaces HATEOAS para operaciones relacionadas con el usuario.
6. Si el ID no existe, el sistema debe retornar un error 404 (Not Found).
7. La respuesta debe tener un código 200 (OK) si el usuario existe.

**HU-BE-014: Actualizar Usuario (Admin)**

**Criterios de Aceptación:**

1. El endpoint `PUT /api/v1/admin/users/:id` debe requerir un token de acceso válido con
   rol de administrador.
2. El sistema debe validar que el ID proporcionado exista en la base de datos.
3. El sistema debe validar todos los campos editables y retornar errores específicos para
   cada campo inválido.
4. Si se actualiza el email, el sistema debe verificar que no exista previamente para otro
   usuario.
5. El sistema debe permitir actualizar el rol del usuario.
6. El sistema debe actualizar automáticamente el campo `updated_at`.
7. La respuesta debe incluir la información actualizada del usuario y tener un código
   200 (OK).

**HU-BE-015: Eliminar/Desactivar Usuario (Admin)**

**Criterios de Aceptación:**

1. El endpoint `DELETE /api/v1/admin/users/:id` debe requerir un token de acceso válido
   con rol de administrador.
2. El sistema debe validar que el ID proporcionado exista en la base de datos.
3. El sistema debe implementar un "soft delete", estableciendo el flag `is_active` en
   `false` y actualizando el campo `deleted_at`.
4. El sistema debe preservar todas las relaciones y datos históricos del usuario.
5. El sistema debe revocar todos los tokens de acceso y refresco del usuario desactivado.
6. La respuesta debe tener un código 200 (OK) con un mensaje de confirmación.
7. El sistema debe impedir que un administrador se elimine a sí mismo.

### Carga Masiva de Datos

**HU-BE-016: Carga Masiva de Usuarios (Admin)**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/admin/users/upload` debe requerir un token de acceso válido
   con rol de administrador.
2. El sistema debe aceptar un archivo CSV con un formato específico (encabezados
   definidos).
3. El sistema debe validar cada fila del CSV según las mismas reglas de validación que la
   creación individual.
4. El sistema debe procesar el archivo por lotes para manejar grandes volúmenes de datos
   eficientemente.
5. El sistema debe generar un reporte detallado de la operación, incluyendo filas
   procesadas exitosamente y errores específicos por fila.
6. Para cada usuario creado exitosamente, el sistema debe generar una contraseña inicial
   igual al número de documento y establecer el flag `must_change_password` en `true`.
7. La respuesta debe incluir estadísticas del proceso (total procesado, exitosos,
   fallidos) y tener un código 200 (OK).

## 📅 Gestión de Horarios (Schedule Service)

**HU-BE-017: Obtener Horarios**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/schedule` debe requerir un token de acceso válido.
2. El sistema debe permitir filtrar horarios por fecha (desde/hasta), ficha, instructor y
   jornada.
3. El sistema debe retornar horarios según el rol del usuario:

- Administradores: todos los horarios según filtros
- Instructores: solo sus horarios asignados
- Aprendices: solo los horarios de su ficha

4. Cada entrada de horario debe incluir información completa: ficha, programa, instructor,
   ambiente, sede, bloque horario, fecha.
5. La respuesta debe estar paginada e incluir metadatos de paginación.
6. La respuesta debe incluir enlaces HATEOAS para operaciones relacionadas.
7. La respuesta debe tener un código 200 (OK).

**HU-BE-018: Gestión CRUD de Horarios (Admin)**

**Criterios de Aceptación:**

1. Los endpoints CRUD de horarios deben requerir un token de acceso válido con rol de
   administrador.
2. El sistema debe implementar los siguientes endpoints:

- `POST /api/v1/admin/schedule` para crear horarios
- `GET /api/v1/admin/schedule/:id` para obtener un horario específico
- `PUT /api/v1/admin/schedule/:id` para actualizar un horario
- `DELETE /api/v1/admin/schedule/:id` para eliminar un horario

3. El sistema debe validar que no existan conflictos de horarios para instructores,
   ambientes o fichas.
4. El sistema debe validar que los instructores, ambientes, fichas y programas existan en
   la base de datos.
5. El sistema debe validar que los bloques horarios sean válidos según la jornada.
6. Las respuestas deben incluir información completa del horario y enlaces HATEOAS.
7. Las operaciones de creación y actualización deben registrar quién realizó el cambio y
   cuándo.

**HU-BE-019: Carga Masiva de Horarios (Admin)**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/admin/schedule/upload` debe requerir un token de acceso
   válido con rol de administrador.
2. El sistema debe aceptar un archivo CSV con un formato específico (encabezados
   definidos).
3. El sistema debe validar cada fila del CSV según las mismas reglas de validación que la
   creación individual.
4. El sistema debe verificar que no existan conflictos de horarios para instructores,
   ambientes o fichas.
5. El sistema debe procesar el archivo por lotes para manejar grandes volúmenes de datos
   eficientemente.
6. El sistema debe generar un reporte detallado de la operación, incluyendo filas
   procesadas exitosamente y errores específicos por fila.
7. La respuesta debe incluir estadísticas del proceso (total procesado, exitosos,
   fallidos) y tener un código 200 (OK).

**HU-BE-020: Gestión de Entidades Maestras (Admin)**

**Criterios de Aceptación:**

1. El sistema debe implementar endpoints CRUD para las siguientes entidades maestras:

- Fichas: `POST/GET/PUT/DELETE /api/v1/admin/master/fichas`
- Programas: `POST/GET/PUT/DELETE /api/v1/admin/master/programas`
- Sedes: `POST/GET/PUT/DELETE /api/v1/admin/master/sedes`
- Ambientes: `POST/GET/PUT/DELETE /api/v1/admin/master/ambientes`

2. Todos los endpoints deben requerir un token de acceso válido con rol de administrador.
3. El sistema debe validar las relaciones entre entidades (ej. un ambiente pertenece a una
   sede).
4. El sistema debe implementar soft delete para preservar la integridad referencial
   histórica.
5. Las respuestas deben incluir información completa de cada entidad y enlaces HATEOAS.
6. El sistema debe permitir filtrar y paginar las listas de entidades.
7. Las operaciones de creación y actualización deben registrar quién realizó el cambio y
   cuándo.

## 📊 Control de Asistencia (Attendance Service)

**HU-BE-021: Registrar Asistencia (Instructor)**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/attendance` debe requerir un token de acceso válido con rol
   de instructor.
2. El sistema debe validar que el instructor esté asignado a la ficha y bloque horario
   para el que registra asistencia.
3. El sistema debe aceptar un código QR válido que se renueva cada 15 segundos.
4. El sistema debe validar que el aprendiz pertenezca a la ficha para la que se registra
   asistencia.
5. El sistema debe impedir registrar asistencia para fechas futuras.
6. El sistema debe permitir actualizar la asistencia dentro del mismo día.
7. La respuesta debe incluir confirmación del registro y tener un código 201 (Created) o
   200 (OK) si es actualización.

**HU-BE-022: Obtener Resumen de Asistencia**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/attendance/summary` debe requerir un token de acceso válido.
2. El sistema debe permitir filtrar por período (desde/hasta), ficha, instructor y
   aprendiz.
3. El sistema debe retornar estadísticas según el rol del usuario:

- Administradores: estadísticas globales o filtradas
- Instructores: estadísticas de sus fichas asignadas
- Aprendices: solo sus estadísticas personales

4. El resumen debe incluir porcentajes de asistencia, ausencias justificadas y no
   justificadas.
5. Para administradores e instructores, el resumen debe incluir listas de aprendices con
   mayor inasistencia.
6. La respuesta debe incluir enlaces HATEOAS para operaciones relacionadas.
7. La respuesta debe tener un código 200 (OK).

**HU-BE-023: Obtener Historial de Asistencia**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/attendance/history` debe requerir un token de acceso válido.
2. El sistema debe permitir filtrar por período (desde/hasta), ficha, instructor, aprendiz
   y estado (presente/ausente/justificado).
3. El sistema debe retornar registros según el rol del usuario:

- Administradores: todos los registros según filtros
- Instructores: solo registros de sus fichas asignadas
- Aprendices: solo sus registros personales

4. Cada registro debe incluir información completa: fecha, bloque horario, ficha,
   instructor, aprendiz, estado.
5. La respuesta debe estar paginada e incluir metadatos de paginación.
6. La respuesta debe incluir enlaces HATEOAS para operaciones relacionadas.
7. La respuesta debe tener un código 200 (OK).

**HU-BE-024: Cargar Justificación (Aprendiz)**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/attendance/justification` debe requerir un token de acceso
   válido con rol de aprendiz.
2. El sistema debe permitir adjuntar un archivo PDF con la justificación.
3. El sistema debe validar que el archivo no exceda un tamaño máximo (5MB).
4. El sistema debe validar que la inasistencia exista y pertenezca al aprendiz
   autenticado.
5. El sistema debe registrar la fecha de carga de la justificación y establecer su estado
   como "pendiente".
6. El sistema debe almacenar el archivo en un sistema de archivos seguro con nombre único.
7. La respuesta debe incluir confirmación del registro y tener un código 201 (Created).

**HU-BE-025: Gestionar Justificaciones (Instructor)**

**Criterios de Aceptación:**

1. El endpoint `PUT /api/v1/attendance/justification/:id` debe requerir un token de acceso
   válido con rol de instructor.
2. El sistema debe validar que el ID proporcionado exista y corresponda a una
   justificación de un aprendiz en una ficha asignada al instructor.
3. El sistema debe permitir actualizar el estado de la justificación a "aprobada" o "
   rechazada".
4. El sistema debe requerir un comentario obligatorio en caso de rechazo.
5. El sistema debe registrar quién aprobó/rechazó la justificación y cuándo.
6. Si se aprueba, el sistema debe actualizar automáticamente el registro de asistencia
   correspondiente a "justificado".
7. La respuesta debe incluir la información actualizada de la justificación y tener un
   código 200 (OK).

**HU-BE-026: Obtener Alertas de Asistencia**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/attendance/alerts` debe requerir un token de acceso válido.
2. El sistema debe identificar casos críticos según reglas predefinidas:

- Aprendices con 3 o más inasistencias consecutivas
- Aprendices con menos del 80% de asistencia en el último mes
- Aprendices en riesgo de deserción según patrones históricos

3. El sistema debe retornar alertas según el rol del usuario:

- Administradores: todas las alertas
- Instructores: solo alertas de sus fichas asignadas
- Aprendices: solo sus alertas personales

4. Cada alerta debe incluir información detallada del caso y recomendaciones de acción.
5. La respuesta debe estar categorizada por nivel de criticidad (alta, media, baja).
6. La respuesta debe incluir enlaces HATEOAS para operaciones relacionadas.
7. La respuesta debe tener un código 200 (OK).

**HU-BE-027: Alertas de Instructores sin Registro (Admin)**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/attendance/alerts/admin/instructors/no-attendance` debe
   requerir un token de acceso válido con rol de administrador.
2. El sistema debe identificar instructores que no registraron asistencia el día anterior
   cuando tenían horario asignado.
3. El sistema debe permitir filtrar por sede, programa o ficha.
4. Cada alerta debe incluir información del instructor, ficha, bloque horario y ambiente
   donde no se registró asistencia.
5. La respuesta debe estar ordenada por instructor y hora.
6. La respuesta debe incluir enlaces HATEOAS para operaciones relacionadas.
7. La respuesta debe tener un código 200 (OK).

## 🤖 Inteligencia Artificial (AI Service)

### Análisis Predictivo

**HU-BE-028: Dashboard Predictivo de Deserción**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/ai/desertion/predictions` debe requerir un token de acceso válido con rol de administrador o instructor.
2. El sistema debe analizar patrones históricos de asistencia para identificar aprendices en riesgo de deserción.
3. El sistema debe calcular un "score de riesgo" para cada aprendiz basado en múltiples factores:

- Porcentaje de asistencia global
- Tendencia reciente de asistencia (mejorando/empeorando)
- Patrones de inasistencia (días específicos, bloques específicos)
- Comparación con patrones históricos de deserción

4. La respuesta debe incluir una lista de aprendices en riesgo, ordenados por nivel de riesgo.
5. Cada entrada debe incluir el score de riesgo, factores contribuyentes y recomendaciones de intervención.
6. El sistema debe permitir filtrar por ficha, programa o nivel de riesgo.
7. La respuesta debe tener un código 200 (OK).

**HU-BE-029: Optimizador de Horarios**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/ai/schedule/optimization` debe requerir un token de acceso válido con rol de administrador.
2. El sistema debe analizar patrones históricos de asistencia para identificar bloques horarios con mayor/menor asistencia.
3. El sistema debe generar recomendaciones para optimizar la distribución horaria basadas en:

- Patrones de asistencia por bloque horario
- Disponibilidad de ambientes
- Preferencias de instructores (si están registradas)
- Características de las fichas (programa, jornada)

4. Las recomendaciones deben incluir sugerencias específicas de cambios con justificación.
5. El sistema debe permitir simular el impacto esperado de los cambios propuestos.
6. La respuesta debe incluir métricas comparativas entre la distribución actual y la optimizada.
7. La respuesta debe tener un código 200 (OK).

**HU-BE-030: Análisis con Procesamiento de Lenguaje Natural**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/ai/insights/query` debe requerir un token de acceso válido con rol de administrador o instructor.
2. El sistema debe aceptar consultas en lenguaje natural sobre datos de asistencia y horarios.
3. El sistema debe interpretar la intención de la consulta y traducirla a operaciones de análisis de datos.
4. El sistema debe soportar al menos los siguientes tipos de consultas:

- Comparativas ("¿Cómo es la asistencia de la ficha X comparada con la Y?")
- Tendencias ("¿Cómo ha evolucionado la asistencia en el último trimestre?")
- Correlaciones ("¿Hay relación entre el ambiente y la asistencia?")
- Anomalías ("¿Qué días tuvieron asistencia inusualmente baja?")

5. La respuesta debe incluir datos estructurados y una interpretación en lenguaje natural.
6. El sistema debe manejar consultas ambiguas solicitando clarificación.
7. La respuesta debe tener un código 200 (OK).

### Validación y Asistencia Inteligente

**HU-BE-031: Validador Inteligente de CSV**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/ai/validate/csv` debe requerir un token de acceso válido con rol de administrador.
2. El sistema debe aceptar un archivo CSV y su tipo (usuarios, horarios, etc.).
3. El sistema debe realizar validaciones básicas (formato, encabezados, tipos de datos).
4. El sistema debe detectar anomalías potenciales como:

- Valores atípicos o estadísticamente improbables
- Inconsistencias internas (ej. horarios imposibles)
- Conflictos potenciales con datos existentes
- Patrones sospechosos (duplicados casi idénticos)

5. El sistema debe generar un reporte detallado con hallazgos categorizados por severidad.
6. El sistema debe proporcionar recomendaciones específicas para corregir problemas.
7. La respuesta debe tener un código 200 (OK).

**HU-BE-032: Asistente de Gestión Proactiva**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/ai/attendance/insights` debe requerir un token de acceso válido con rol de instructor.
2. El sistema debe analizar los datos de asistencia de las fichas asignadas al instructor.
3. El sistema debe generar insights personalizados como:

- Aprendices que requieren atención inmediata
- Patrones emergentes de inasistencia
- Comparación con el rendimiento histórico de la ficha
- Recomendaciones específicas de intervención

4. Los insights deben estar priorizados por relevancia y urgencia.
5. El sistema debe adaptar las recomendaciones según las acciones previas del instructor.
6. La respuesta debe incluir enlaces a recursos relevantes (procedimientos, contactos).
7. La respuesta debe tener un código 200 (OK).

**HU-BE-033: Analizador de Justificaciones**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/ai/justifications/analyze/:id` debe requerir un token de acceso válido con rol de instructor.
2. El sistema debe validar que el ID proporcionado exista y corresponda a una justificación pendiente en una ficha asignada al instructor.
3. El sistema debe analizar el documento PDF adjunto utilizando OCR y procesamiento de lenguaje natural.
4. El sistema debe extraer información clave como:

- Tipo de justificación (médica, familiar, etc.)
- Fechas mencionadas
- Entidades emisoras (hospital, institución)
- Firmas o sellos detectados

5. El sistema debe verificar la consistencia interna del documento y detectar posibles anomalías.
6. La respuesta debe incluir la información extraída y una recomendación preliminar.
7. La respuesta debe tener un código 200 (OK).

### Chatbot de Reglamento

**HU-BE-034: Consulta al Chatbot de Reglamento**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/ai/chatbot/query` debe requerir un token de acceso válido.
2. El sistema debe aceptar consultas en lenguaje natural sobre el reglamento académico.
3. El sistema debe analizar la consulta y buscar información relevante en la base de conocimiento del reglamento.
4. La respuesta debe incluir:

- Respuesta directa a la consulta
- Citas textuales del reglamento con referencias precisas (artículo, página)
- Enlaces a documentos completos relevantes
- Sugerencias de consultas relacionadas

5. El sistema debe adaptar el nivel de detalle según el rol del usuario (admin, instructor, aprendiz).
6. El sistema debe mantener contexto de la conversación para consultas de seguimiento.
7. La respuesta debe tener un código 200 (OK).

**HU-BE-035: Obtener Reglamentos Disponibles**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/ai/chatbot/agreements` debe requerir un token de acceso válido.
2. El sistema debe retornar una lista de todos los acuerdos y reglamentos disponibles para consulta.
3. Cada entrada debe incluir:

- Identificador único
- Título completo
- Fecha de emisión
- Breve descripción
- Enlace al documento completo
- Categorías o etiquetas

4. El sistema debe permitir filtrar por categoría, fecha o término de búsqueda.
5. La respuesta debe estar organizada jerárquicamente (por tipo de documento y fecha).
6. La respuesta debe incluir enlaces HATEOAS para operaciones relacionadas.
7. La respuesta debe tener un código 200 (OK).

## 🌐 API Gateway y Seguridad

**HU-BE-036: Enrutamiento de Microservicios**

**Criterios de Aceptación:**

1. La API Gateway debe enrutar correctamente todas las peticiones a `/api/v1/...` al microservicio correspondiente.
2. El enrutamiento debe ser transparente para el cliente, que no necesita conocer la topología interna.
3. La API Gateway debe manejar correctamente los timeouts y reintentos en caso de fallos temporales.
4. La API Gateway debe mantener un registro de todas las peticiones enrutadas.
5. El sistema debe soportar balanceo de carga si hay múltiples instancias de un microservicio.
6. La configuración de enrutamiento debe ser dinámica y actualizable sin reiniciar el servicio.
7. El sistema debe proporcionar métricas de rendimiento por ruta y microservicio.

**HU-BE-037: Autenticación Centralizada**

**Criterios de Aceptación:**

1. La API Gateway debe validar automáticamente los tokens JWT en todas las rutas protegidas.
2. El sistema debe verificar la firma, expiración y revocación de los tokens.
3. El sistema debe rechazar peticiones con tokens inválidos con un error 401 (Unauthorized).
4. El sistema debe extraer la información del usuario del token y pasarla a los microservicios.
5. La API Gateway debe manejar correctamente las rutas públicas que no requieren autenticación.
6. El sistema debe registrar todos los intentos de acceso no autorizados.
7. La validación debe ser eficiente y no introducir latencia significativa.

**HU-BE-038: Control de Acceso por Roles**

**Criterios de Aceptación:**

1. La API Gateway debe verificar que el usuario tenga el rol requerido para acceder a cada endpoint.
2. El sistema debe rechazar peticiones a endpoints restringidos con un error 403 (Forbidden).
3. La configuración de roles debe ser flexible y permitir múltiples roles por endpoint.
4. El sistema debe soportar permisos granulares además de roles generales.
5. La API Gateway debe pasar la información de roles a los microservicios para validaciones adicionales.
6. El sistema debe registrar todos los intentos de acceso no autorizados con detalles del usuario y recurso.
7. La verificación debe ser eficiente y no introducir latencia significativa.

**HU-BE-039: Gestión de CORS**

**Criterios de Aceptación:**

1. La API Gateway debe implementar correctamente las cabeceras CORS para todas las respuestas.
2. El sistema debe permitir configurar dominios permitidos para solicitudes cross-origin.
3. El sistema debe manejar correctamente las solicitudes preflight (OPTIONS).
4. La configuración debe permitir especificar métodos, cabeceras y credenciales permitidas.
5. La API Gateway debe implementar diferentes políticas CORS según el entorno (desarrollo, producción).
6. El sistema debe registrar intentos de acceso desde dominios no permitidos.
7. La implementación debe seguir las mejores prácticas de seguridad para CORS.

**HU-BE-040: Logging Centralizado**

**Criterios de Aceptación:**

1. La API Gateway debe registrar todas las peticiones entrantes con información detallada.
2. El registro debe incluir: timestamp, método, ruta, IP, usuario, tiempo de respuesta, código de estado.
3. El sistema debe permitir configurar diferentes niveles de detalle según el entorno.
4. Los logs deben estar en un formato estructurado (JSON) para facilitar el análisis.
5. El sistema debe implementar rotación de logs para evitar archivos demasiado grandes.
6. La API Gateway debe proporcionar endpoints para consultar logs filtrados (solo admin).
7. El logging debe ser eficiente y no impactar significativamente el rendimiento.

**HU-BE-041: Manejo Unificado de Errores**

**Criterios de Aceptación:**

1. La API Gateway debe transformar todos los errores de los microservicios a un formato JSON consistente.
2. El formato de error debe incluir: código de error, mensaje amigable, detalles técnicos (solo en desarrollo).
3. El sistema debe manejar correctamente errores de timeout, conexión y otros fallos de infraestructura.
4. La API Gateway debe asignar códigos HTTP apropiados según el tipo de error.
5. El sistema debe incluir enlaces HATEOAS relevantes en las respuestas de error.
6. Los mensajes de error deben ser claros, informativos y no revelar detalles de implementación.
7. El sistema debe registrar todos los errores con información de contexto para
   diagnóstico.

## 💾 Respaldo y Recuperación

**HU-BE-042: Respaldo Automático de BD**

**Criterios de Aceptación:**

1. El sistema debe realizar respaldos automáticos diarios de todas las bases de datos.
2. Los respaldos deben ejecutarse en horarios de baja carga (preferiblemente 3:00 AM).
3. El sistema debe comprimir los respaldos para optimizar el almacenamiento.
4. Los respaldos deben almacenarse en una ubicación segura y redundante.
5. El sistema debe implementar una política de retención (7 diarios, 4 semanales, 12 mensuales).
6. El sistema debe verificar la integridad de cada respaldo generado.
7. El sistema debe notificar a los administradores sobre el resultado de cada operación de respaldo.

**HU-BE-043: Restauración por Servicio**

**Criterios de Aceptación:**

1. El sistema debe proporcionar scripts para restaurar bases de datos individuales desde respaldos.
2. Los scripts deben validar la integridad del respaldo antes de iniciar la restauración.
3. El sistema debe permitir restaurar a un entorno de prueba sin afectar la producción.
4. El proceso de restauración debe incluir validación de esquema y datos.
5. El sistema debe notificar a los administradores sobre el resultado de cada operación de restauración.
6. Los scripts deben manejar correctamente dependencias entre servicios.
7. El sistema debe proporcionar estimaciones de tiempo para operaciones de restauración grandes.

**HU-BE-044: Verificación de Integridad**

**Criterios de Aceptación:**

1. El sistema debe verificar automáticamente la integridad de cada respaldo generado.
2. La verificación debe incluir validación de estructura, checksums y pruebas de restauración parcial.
3. El sistema debe generar un reporte detallado de cada verificación.
4. El sistema debe notificar inmediatamente a los administradores sobre cualquier problema detectado.
5. El reporte debe incluir métricas como tamaño, tiempo de generación y resultado de las pruebas.
6. El sistema debe mantener un historial de verificaciones para análisis de tendencias.
7. La verificación debe ser eficiente y no impactar significativamente el rendimiento del sistema.

**HU-BE-045: Respaldo Incremental**

**Criterios de Aceptación:**

1. El sistema debe realizar respaldos incrementales cada 6 horas además de los completos diarios.
2. Los respaldos incrementales deben capturar solo los cambios desde el último respaldo.
3. El sistema debe optimizar el almacenamiento combinando respaldos incrementales cuando sea apropiado.
4. El sistema debe permitir reconstruir el estado de la base de datos a cualquier punto usando la combinación de respaldos completos e incrementales.
5. El sistema debe verificar la integridad de cada respaldo incremental.
6. El sistema debe notificar a los administradores sobre el resultado de cada operación.
7. La implementación debe minimizar el impacto en el rendimiento durante las horas de operación.

**HU-BE-046: Recuperación Point-in-Time**

**Criterios de Aceptación:**

1. El sistema debe permitir restaurar las bases de datos a un momento específico en el tiempo.
2. La recuperación debe combinar respaldos completos, incrementales y logs de transacciones.
3. El sistema debe proporcionar una interfaz para seleccionar el punto exacto de recuperación.
4. El proceso debe validar la viabilidad de la recuperación antes de iniciarla.
5. El sistema debe permitir recuperar a un entorno de prueba sin afectar la producción.
6. El sistema debe notificar a los administradores sobre el progreso y resultado de la operación.
7. La implementación debe incluir validación post-recuperación para verificar la integridad de los datos.

## 🧠 Knowledge Base Service (kbservice)

### Gestión de Contenido de Conocimiento

**HU-BE-KB-001: Crear Elemento de Conocimiento**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/kb/items` debe requerir un token de acceso válido con rol de administrador.
2. El sistema debe validar todos los campos requeridos: título, contenido, tipo, categoría, audiencia objetivo.
3. El sistema debe generar automáticamente embeddings vectoriales para el contenido utilizando un modelo de IA apropiado.
4. El sistema debe almacenar tanto el contenido original como los embeddings en la base de datos.
5. El sistema debe asignar un identificador único al elemento y registrar metadatos como fecha de creación y autor.
6. La respuesta debe incluir el elemento creado con todos sus metadatos y tener un código 201 (Created).
7. El sistema debe indexar el nuevo elemento para búsquedas de texto completo y semánticas.

**HU-BE-KB-002: Obtener Elemento de Conocimiento**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/kb/items/{id}` debe requerir un token de acceso válido.
2. El sistema debe validar que el ID proporcionado exista en la base de datos.
3. El sistema debe verificar que el usuario tenga permiso para acceder al elemento según su rol y la audiencia objetivo del elemento.
4. La respuesta debe incluir todos los campos del elemento excepto los embeddings vectoriales.
5. La respuesta debe incluir enlaces HATEOAS para operaciones relacionadas con el elemento.
6. Si el ID no existe, el sistema debe retornar un error 404 (Not Found).
7. La respuesta debe tener un código 200 (OK) si el elemento existe y es accesible.

**HU-BE-KB-003: Actualizar Elemento de Conocimiento**

**Criterios de Aceptación:**

1. El endpoint `PUT /api/v1/kb/items/{id}` debe requerir un token de acceso válido con rol de administrador.
2. El sistema debe validar que el ID proporcionado exista en la base de datos.
3. El sistema debe validar todos los campos editables y retornar errores específicos para cada campo inválido.
4. Si se actualiza el contenido, el sistema debe regenerar automáticamente los embeddings vectoriales.
5. El sistema debe mantener un historial de versiones del elemento, registrando quién realizó cada cambio y cuándo.
6. La respuesta debe incluir el elemento actualizado con todos sus metadatos.
7. La respuesta debe tener un código 200 (OK).

**HU-BE-KB-004: Eliminar Elemento de Conocimiento**

**Criterios de Aceptación:**

1. El endpoint `DELETE /api/v1/kb/items/{id}` debe requerir un token de acceso válido con rol de administrador.
2. El sistema debe validar que el ID proporcionado exista en la base de datos.
3. El sistema debe implementar un "soft delete", manteniendo el elemento en la base de datos pero marcándolo como eliminado.
4. El sistema debe registrar quién eliminó el elemento y cuándo.
5. El sistema debe actualizar los índices de búsqueda para excluir el elemento eliminado.
6. La respuesta debe tener un código 200 (OK) con un mensaje de confirmación.
7. El sistema debe proporcionar un mecanismo para restaurar elementos eliminados (solo administradores).

**HU-BE-KB-005: Listar Elementos de Conocimiento**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/kb/items` debe requerir un token de acceso válido.
2. El sistema debe permitir filtrar por categoría, tipo, audiencia objetivo y fecha de creación/actualización.
3. El sistema debe permitir ordenar por diferentes campos (título, fecha, relevancia).
4. El sistema debe retornar solo elementos accesibles según el rol del usuario.
5. La respuesta debe estar paginada e incluir metadatos de paginación.
6. Cada elemento en la lista debe incluir información básica y enlaces HATEOAS.
7. La respuesta debe tener un código 200 (OK).

**HU-BE-KB-006: Filtrar Elementos por Tipo de Usuario**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/kb/items?user_type={type}` debe requerir un token de acceso válido.
2. El sistema debe validar que el tipo de usuario proporcionado sea válido (admin, instructor, aprendiz).
3. El sistema debe retornar solo elementos relevantes para el tipo de usuario especificado.
4. La relevancia debe determinarse por la audiencia objetivo explícita del elemento y por análisis de contenido.
5. La respuesta debe estar ordenada por relevancia para el tipo de usuario especificado.
6. La respuesta debe estar paginada e incluir metadatos de paginación.
7. La respuesta debe tener un código 200 (OK).

### Búsqueda y Consulta de Conocimiento

**HU-BE-KB-007: Búsqueda de Texto Tradicional**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/kb/search?query={text}` debe requerir un token de acceso válido.
2. El sistema debe utilizar capacidades de búsqueda de texto completo de PostgreSQL (tsvector, tsquery).
3. La búsqueda debe incluir título, contenido y metadatos de los elementos.
4. El sistema debe implementar stemming, manejo de sinónimos y ranking de relevancia.
5. Los resultados deben incluir solo elementos accesibles según el rol del usuario.
6. La respuesta debe estar ordenada por relevancia y paginada.
7. La respuesta debe incluir fragmentos de texto (snippets) que muestren el contexto de las coincidencias.

**HU-BE-KB-008: Búsqueda Semántica**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/kb/semantic-search?query={text}` debe requerir un token de acceso válido.
2. El sistema debe convertir la consulta en un vector de embedding utilizando el mismo modelo que para los elementos.
3. El sistema debe realizar una búsqueda de similitud vectorial utilizando pgvector.
4. La búsqueda debe encontrar elementos conceptualmente similares aunque usen palabras diferentes.
5. Los resultados deben incluir solo elementos accesibles según el rol del usuario.
6. La respuesta debe incluir un score de similitud para cada resultado.
7. La respuesta debe estar ordenada por similitud y paginada.

**HU-BE-KB-009: Consulta Inteligente**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/kb/query` debe requerir un token de acceso válido.
2. El sistema debe analizar la consulta utilizando NLP para determinar la intención y entidades.
3. El sistema debe seleccionar la estrategia de búsqueda óptima (texto, semántica o híbrida) según la consulta.
4. El sistema debe combinar resultados de múltiples fuentes cuando sea apropiado.
5. La respuesta debe incluir una respuesta directa generada a partir de los resultados más relevantes.
6. La respuesta debe incluir referencias a las fuentes utilizadas para generar la respuesta.
7. El sistema debe adaptar el formato y nivel de detalle de la respuesta según el rol del usuario.

**HU-BE-KB-010: Consulta con Contexto de Usuario**

**Criterios de Aceptación:**

1. El endpoint debe aceptar información de contexto del usuario además de la consulta.
2. El contexto puede incluir: rol, historial de consultas, preferencias, ficha/programa (para aprendices).
3. El sistema debe utilizar este contexto para personalizar los resultados y la respuesta.
4. La personalización debe considerar el nivel de experiencia, área de interés y necesidades específicas.
5. El sistema debe priorizar elementos más relevantes para el contexto específico del usuario.
6. La respuesta debe incluir recomendaciones personalizadas basadas en el contexto.
7. El sistema debe aprender de las interacciones para mejorar la personalización con el tiempo.

### Integración con Chatbot de Reglamento

**HU-BE-KB-011: Routing Inteligente al Chatbot**

**Criterios de Aceptación:**

1. El sistema debe analizar cada consulta para determinar si está relacionada con el reglamento académico.
2. La clasificación debe utilizar un modelo de NLP entrenado específicamente para este propósito.
3. El sistema debe identificar correctamente consultas como "¿Cuántas faltas puedo tener?" como relacionadas con el reglamento.
4. Para consultas relacionadas con el reglamento, el sistema debe enrutar la consulta al chatbot especializado.
5. El sistema debe mantener el contexto de la conversación al enrutar entre servicios.
6. El sistema debe registrar métricas de precisión del routing para mejora continua.
7. El mecanismo de routing debe ser eficiente y no introducir latencia significativa.

**HU-BE-KB-012: Consulta Híbrida**

**Criterios de Aceptación:**

1. Para consultas que requieren información tanto del reglamento como de procedimientos, el sistema debe consultar ambas fuentes.
2. El sistema debe combinar las respuestas de manera coherente y sin duplicaciones.
3. La respuesta combinada debe indicar claramente qué partes provienen de cada fuente.
4. El sistema debe priorizar información oficial del reglamento cuando haya conflictos.
5. La respuesta debe incluir enlaces a documentos completos de ambas fuentes cuando sea relevante.
6. El sistema debe mantener un registro de consultas híbridas para análisis y mejora.
7. La combinación debe ser semánticamente coherente, no una simple concatenación.

**HU-BE-KB-013: Fallback Automático**

**Criterios de Aceptación:**

1. Si el chatbot de reglamento no está disponible, el sistema debe recurrir a la base de conocimiento general.
2. Si la base de conocimiento no tiene información relevante, el sistema debe indicarlo claramente.
3. El sistema debe implementar un timeout apropiado para detectar servicios no disponibles.
4. El sistema debe registrar todos los casos de fallback para análisis y mejora.
5. La respuesta debe indicar que se está utilizando una fuente alternativa.
6. El sistema debe proporcionar opciones alternativas cuando ninguna fuente tenga la respuesta.
7. El mecanismo de fallback debe ser eficiente y no degradar significativamente el tiempo de respuesta.

### Gestión de Embeddings y Vectores

**HU-BE-KB-014: Generación de Embeddings**

**Criterios de Aceptación:**

1. El sistema debe generar embeddings vectoriales para todo el contenido de conocimiento.
2. Los embeddings deben utilizar un modelo apropiado para contenido educativo en español.
3. El sistema debe implementar pre-procesamiento específico para terminología académica.
4. Los embeddings deben almacenarse eficientemente en la base de datos utilizando pgvector.
5. El sistema debe manejar correctamente contenido largo dividiéndolo en chunks apropiados.
6. El proceso de generación debe ser asíncrono para no bloquear operaciones CRUD.
7. El sistema debe registrar métricas del proceso de generación para optimización.

**HU-BE-KB-015: Regeneración de Embeddings**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/kb/admin/regenerate-embeddings` debe requerir un token de acceso válido con rol de administrador.
2. El sistema debe permitir regenerar embeddings para todo el contenido o un subconjunto específico.
3. El proceso debe ser ejecutado en background y reportar progreso.
4. El sistema debe mantener la funcionalidad de búsqueda durante la regeneración.
5. El sistema debe validar cada embedding generado antes de actualizar la base de datos.
6. El sistema debe generar un reporte detallado al finalizar el proceso.
7. La regeneración debe ser idempotente y segura para ejecutar múltiples veces.

**HU-BE-KB-016: Optimización de Índices Vectoriales**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/kb/admin/optimize-indices` debe requerir un token de acceso válido con rol de administrador.
2. El sistema debe optimizar los índices HNSW de pgvector para mejorar el rendimiento de búsqueda.
3. El sistema debe permitir configurar parámetros como `m` (número de conexiones) y `ef_construction` (precisión).
4. El proceso debe ejecutarse en background sin afectar la disponibilidad del servicio.
5. El sistema debe realizar pruebas de rendimiento antes y después para medir la mejora.
6. El sistema debe generar un reporte detallado con métricas de rendimiento.
7. La optimización debe ser idempotente y segura para ejecutar múltiples veces.

### Análisis y Métricas

**HU-BE-KB-017: Registro de Consultas**

**Criterios de Aceptación:**

1. El sistema debe registrar todas las consultas y sus resultados en un formato estructurado.
2. El registro debe incluir: consulta, tipo de búsqueda utilizada, resultados retornados, feedback del usuario.
3. El sistema debe implementar anonimización apropiada para proteger la privacidad de los usuarios.
4. Los logs deben almacenarse eficientemente para permitir análisis a largo plazo.
5. El sistema debe implementar rotación y archivado de logs antiguos.
6. El registro no debe impactar significativamente el rendimiento del servicio.
7. El sistema debe proporcionar herramientas para analizar los logs (solo administradores).

**HU-BE-KB-018: Métricas de Rendimiento**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/kb/admin/metrics` debe requerir un token de acceso válido con rol de administrador.
2. El sistema debe recopilar y proporcionar métricas detalladas sobre el rendimiento del servicio.
3. Las métricas deben incluir: tiempo de respuesta promedio, tasa de consultas, precisión de búsqueda, uso de recursos.
4. El sistema debe permitir filtrar métricas por período, tipo de consulta y origen.
5. Las métricas deben presentarse en formato tabular y gráfico.
6. El sistema debe identificar automáticamente tendencias y anomalías en las métricas.
7. La recopilación de métricas debe tener un impacto mínimo en el rendimiento del servicio.

**HU-BE-KB-019: Análisis de Patrones de Consulta**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/kb/admin/query-patterns` debe requerir un token de acceso válido con rol de administrador.
2. El sistema debe analizar los logs de consultas para identificar patrones significativos.
3. El análisis debe identificar: consultas frecuentes, consultas sin resultados satisfactorios, tendencias temporales.
4. El sistema debe agrupar consultas semánticamente similares para identificar temas comunes.
5. El análisis debe proporcionar recomendaciones para mejorar la base de conocimiento.
6. El sistema debe identificar áreas donde falta contenido basándose en consultas sin resultados.
7. La respuesta debe incluir visualizaciones para facilitar la interpretación de los patrones.

**HU-BE-KB-020: Feedback de Usuarios**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/kb/feedback` debe requerir un token de acceso válido.
2. El sistema debe permitir a los usuarios calificar la utilidad de las respuestas (1-5 estrellas).
3. El sistema debe permitir comentarios opcionales sobre la respuesta.
4. El feedback debe asociarse con la consulta y respuesta específicas.
5. El sistema debe agregar el feedback para generar métricas de satisfacción por tipo de consulta.
6. El sistema debe identificar patrones en el feedback negativo para mejora continua.
7. El sistema debe proporcionar un dashboard de feedback para administradores.

### Caché y Optimización

**HU-BE-KB-021: Caché de Respuestas Frecuentes**

**Criterios de Aceptación:**

1. El sistema debe implementar un mecanismo de caché para consultas frecuentes utilizando Redis.
2. El sistema debe identificar automáticamente consultas candidatas para caché basándose en frecuencia y estabilidad de respuesta.
3. Las entradas en caché deben tener un TTL (time-to-live) apropiado según el tipo de contenido.
4. El sistema debe implementar invalidación inteligente cuando el contenido relacionado se actualiza.
5. El sistema debe mantener versiones de caché separadas por rol de usuario cuando sea necesario.
6. El sistema debe proporcionar métricas sobre la efectividad del caché (hit rate, latencia).
7. El mecanismo de caché debe ser transparente para los clientes de la API.

**HU-BE-KB-022: Caché de Embeddings**

**Criterios de Aceptación:**

1. El sistema debe implementar un caché para embeddings de consultas recientes.
2. El caché debe almacenar el vector generado junto con la consulta original.
3. El sistema debe utilizar una estrategia LRU (Least Recently Used) para gestionar el tamaño del caché.
4. El sistema debe implementar una política de expiración basada en tiempo y uso.
5. El caché debe ser persistente para sobrevivir reinicios del servicio.
6. El sistema debe proporcionar métricas sobre la efectividad del caché.
7. El caché debe reducir significativamente el tiempo de procesamiento para consultas repetidas o similares.

**HU-BE-KB-023: Optimización de Consultas Complejas**

**Criterios de Aceptación:**

1. El sistema debe optimizar consultas que combinan búsqueda vectorial y filtros tradicionales.
2. La optimización debe incluir estrategias como: pre-filtrado, índices compuestos, ejecución paralela.
3. El sistema debe adaptar dinámicamente la estrategia de ejecución según las características de la consulta.
4. El sistema debe implementar timeouts apropiados para consultas potencialmente costosas.
5. El sistema debe proporcionar explicaciones de plan de ejecución para administradores.
6. Las optimizaciones deben mantener la precisión de los resultados.
7. El sistema debe monitorear y registrar el rendimiento de consultas complejas para mejora continua.

### Administración del Sistema

**HU-BE-KB-024: Configuración del Servicio**

**Criterios de Aceptación:**

1. El endpoint `PUT /api/v1/kb/admin/config` debe requerir un token de acceso válido con rol de administrador.
2. El sistema debe permitir configurar parámetros operativos sin requerir redeployment.
3. Los parámetros configurables deben incluir: límites de recursos, umbrales de caché, parámetros de búsqueda.
4. El sistema debe validar cada parámetro para asegurar valores dentro de rangos seguros.
5. El sistema debe mantener un historial de cambios de configuración con autor y timestamp.
6. Los cambios de configuración deben aplicarse sin interrumpir el servicio.
7. El sistema debe proporcionar valores predeterminados sensatos para todos los parámetros.

**HU-BE-KB-025: Monitoreo de Salud del Servicio**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/kb/admin/health` debe requerir un token de acceso válido con rol de administrador.
2. El sistema debe verificar el estado de todos los componentes críticos: base de datos, caché, servicios externos.
3. El sistema debe proporcionar métricas de salud detalladas: uso de CPU/memoria, latencia, errores recientes.
4. El sistema debe implementar health checks automáticos periódicos.
5. El sistema debe alertar automáticamente a los administradores sobre problemas críticos.
6. La respuesta debe incluir recomendaciones específicas para resolver problemas detectados.
7. El endpoint debe tener una versión pública simplificada para monitoreo externo.

**HU-BE-KB-026: Backup y Restauración**

**Criterios de Aceptación:**

1. El sistema debe proporcionar mecanismos para realizar backups completos de la base de conocimiento.
2. Los backups deben incluir tanto el contenido como los embeddings vectoriales.
3. El sistema debe permitir backups programados y bajo demanda.
4. El sistema debe proporcionar herramientas para restaurar desde un backup.
5. El proceso de restauración debe validar la integridad de los datos antes y después.
6. El sistema debe permitir restaurar a un entorno de prueba sin afectar la producción.
7. El sistema debe mantener metadatos de cada backup para facilitar la selección durante la restauración.

**HU-BE-KB-027: Gestión de Versiones de Contenido**

**Criterios de Aceptación:**

1. El sistema debe mantener un historial completo de versiones para cada elemento de conocimiento.
2. Cada versión debe incluir: contenido completo, metadatos, autor del cambio, timestamp, comentario opcional.
3. El sistema debe proporcionar endpoints para listar versiones de un elemento.
4. El sistema debe permitir ver y comparar versiones específicas.
5. El sistema debe permitir revertir a una versión anterior si es necesario.
6. El sistema debe implementar una política de retención para versiones antiguas.
7. El historial de versiones debe ser accesible solo para administradores.

## 📊 Evaluación de Instructores (EVALIN Service)

### 👨‍💼 Gestión de Preguntas y Cuestionarios

**HU-BE-EVALIN-001: Gestión de Preguntas de Evaluación**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/evalin/questions` debe validar todos los campos requeridos (
   texto, tipo, dimensión/categoría, opciones si aplica) y retornar errores específicos
   para cada campo inválido.
2. El endpoint `GET /api/v1/evalin/questions` debe soportar paginación, filtrado por
   dimensión/categoría y ordenamiento.
3. El endpoint `GET /api/v1/evalin/questions/{id}` debe retornar todos los detalles de una
   pregunta específica, incluyendo sus opciones si es de selección.
4. El endpoint `PUT /api/v1/evalin/questions/{id}` debe validar todos los campos y
   actualizar solo los proporcionados, manteniendo los demás sin cambios.
5. El endpoint `DELETE /api/v1/evalin/questions/{id}` debe verificar que la pregunta no
   esté asociada a ningún cuestionario activo antes de eliminarla.
6. Todos los endpoints deben verificar que el usuario tenga rol de administrador antes de
   procesar la solicitud.
7. Las respuestas deben incluir códigos HTTP apropiados (201 para creación, 200 para
   lectura/actualización, 204 para eliminación).

**HU-BE-EVALIN-002: Agrupar Preguntas en Cuestionarios**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/evalin/questionnaires` debe validar los campos requeridos (
   título, descripción, estado) y crear un cuestionario vacío.
2. El endpoint `GET /api/v1/evalin/questionnaires` debe soportar paginación, filtrado por
   estado y ordenamiento.
3. El endpoint `GET /api/v1/evalin/questionnaires/{id}` debe retornar todos los detalles
   del cuestionario, incluyendo la lista de preguntas asociadas con su orden.
4. El endpoint `PUT /api/v1/evalin/questionnaires/{id}` debe validar todos los campos y
   actualizar solo los proporcionados.
5. El endpoint `DELETE /api/v1/evalin/questionnaires/{id}` debe verificar que el
   cuestionario no esté asociado a ningún periodo de evaluación activo antes de
   eliminarlo.
6. El endpoint `POST /api/v1/evalin/questionnaires/{id}/questions` debe validar que las
   preguntas existan y no estén duplicadas en el cuestionario, permitiendo especificar el
   orden.
7. El endpoint `DELETE /api/v1/evalin/questionnaires/{id}/questions/{questionId}` debe
   eliminar la asociación entre la pregunta y el cuestionario sin eliminar la pregunta.

**HU-BE-EVALIN-003: Definir Periodos de Evaluación**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/evalin/periods` debe validar los campos requeridos (título,
   fecha inicio, fecha fin, cuestionario asociado, fichas/programas aplicables).
2. El sistema debe validar que las fechas de inicio y fin sean coherentes (inicio anterior
   a fin) y que no se solapen con otros periodos activos para las mismas fichas.
3. El endpoint `GET /api/v1/evalin/periods` debe soportar paginación, filtrado por
   estado (activo/inactivo/futuro) y ordenamiento por fechas.
4. El endpoint `GET /api/v1/evalin/periods/{id}` debe retornar todos los detalles del
   periodo, incluyendo estadísticas de participación si ya ha iniciado.
5. El endpoint `PUT /api/v1/evalin/periods/{id}` debe validar todos los campos y
   actualizar solo los proporcionados, con restricciones especiales para periodos ya
   iniciados.
6. El endpoint `DELETE /api/v1/evalin/periods/{id}` debe verificar que el periodo no haya
   iniciado antes de permitir su eliminación.
7. Los endpoints `POST /api/v1/evalin/periods/{id}/activate` y
   `POST /api/v1/evalin/periods/{id}/deactivate` deben cambiar el estado del periodo y
   enviar notificaciones automáticas a los aprendices afectados.

**HU-BE-EVALIN-004: Cargar Preguntas desde CSV**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/evalin/questions/upload` debe aceptar un archivo CSV con un
   formato específico y validado.
2. El sistema debe validar la estructura del CSV (encabezados correctos, tipos de datos)
   antes de procesar su contenido.
3. El sistema debe validar cada fila del CSV según las mismas reglas que se aplican a la
   creación manual de preguntas.
4. El sistema debe manejar preguntas nuevas (inserción) y existentes (actualización)
   basándose en un identificador o texto exacto.
5. La respuesta debe incluir un resumen del procesamiento: total de filas, filas
   procesadas exitosamente, filas con errores.
6. Para las filas con errores, la respuesta debe incluir detalles específicos (número de
   fila, campo problemático, descripción del error).
7. El proceso debe ser transaccional: si hay errores críticos, ninguna pregunta debe ser
   creada o actualizada.

### 📝 Gestión de Evaluaciones

**HU-BE-EVALIN-005: Obtener Instructores a Evaluar**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/evalin/instructors-to-evaluate` debe retornar la lista de
   instructores que el aprendiz autenticado puede evaluar.
2. El sistema debe filtrar los instructores basándose en las fichas activas del aprendiz y
   los periodos de evaluación abiertos.
3. La respuesta debe incluir información básica de cada instructor (ID, nombre, apellido,
   foto si está disponible).
4. La respuesta debe indicar para cada instructor si ya ha sido evaluado por el aprendiz
   en el periodo actual.
5. El sistema debe manejar correctamente el caso de múltiples periodos activos,
   priorizando los que están próximos a vencer.
6. La respuesta debe incluir metadatos sobre los periodos de evaluación aplicables (fechas
   de inicio/fin, días restantes).
7. El endpoint debe ser accesible solo para usuarios con rol de aprendiz.

**HU-BE-EVALIN-006: Obtener Cuestionario para Evaluación**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/evalin/questionnaires/for-instructor/{instructorId}` debe
   retornar el cuestionario aplicable para evaluar al instructor especificado.
2. El sistema debe verificar que el instructor sea evaluable por el aprendiz autenticado
   en un periodo activo.
3. El sistema debe seleccionar el cuestionario correcto basándose en el periodo de
   evaluación activo.
4. La respuesta debe incluir todas las preguntas del cuestionario, organizadas según el
   orden definido.
5. Para preguntas de selección, la respuesta debe incluir todas las opciones posibles.
6. El sistema debe manejar correctamente el caso de que el instructor ya haya sido
   evaluado, retornando un error apropiado.
7. La respuesta debe incluir metadatos sobre el periodo de evaluación (ID, fechas, días
   restantes).

**HU-BE-EVALIN-007: Enviar Evaluación Completada**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/evalin/evaluations` debe validar que todos los campos
   requeridos estén presentes (ID instructor, ID periodo, respuestas a todas las
   preguntas).
2. El sistema debe verificar que el instructor sea evaluable por el aprendiz autenticado
   en el periodo especificado.
3. El sistema debe validar que todas las preguntas del cuestionario tengan una respuesta
   válida según su tipo.
4. El sistema debe verificar que el instructor no haya sido evaluado previamente por el
   mismo aprendiz en el mismo periodo.
5. El sistema debe almacenar las respuestas de forma anonimizada, manteniendo solo
   metadatos estadísticos sobre el aprendiz.
6. La respuesta debe incluir una confirmación de éxito y un resumen de la evaluación
   enviada.
7. El sistema debe actualizar las estadísticas de participación del periodo de evaluación.

**HU-BE-EVALIN-008: Verificar Estado de Evaluaciones**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/evalin/my-evaluations` debe retornar la lista de evaluaciones
   completadas por el aprendiz autenticado.
2. La respuesta debe incluir información básica de cada evaluación (instructor, fecha de
   envío, periodo).
3. El sistema debe permitir filtrar por periodo de evaluación y estado (
   completada/pendiente).
4. La respuesta debe incluir metadatos sobre los periodos de evaluación aplicables.
5. El sistema debe manejar correctamente el caso de múltiples periodos activos.
6. La respuesta no debe incluir las respuestas específicas dadas en cada evaluación, solo
   su estado.
7. El endpoint debe ser accesible solo para usuarios con rol de aprendiz.

### 📊 Reportes y Visualización

**HU-BE-EVALIN-009: Obtener Resultados Consolidados**

**Criterios de Aceptación:**

1. Los endpoints de reportes deben verificar que el usuario tenga permisos adecuados (administrador o instructor autorizado para sus propios datos).
2. Para `GET /api/v1/evalin/reports/instructor/{instructorId}`, el sistema debe agregar todas las evaluaciones del instructor especificado.
3. Para `GET /api/v1/evalin/repnorts/program/{programId}`, el sistema debe agregar evaluaciones de todos los instructores del programa.
4. Para `GET /api/v1/evalin/reports/ficha/{fichaId}`, el sistema debe agregar evaluaciones de todos los instructores de la ficha.
5. Los reportes deben incluir estadísticas por dimensión/categoría y por pregunta individual.
6. Los reportes deben incluir métricas como promedio, mediana, desviación estándar y distribución de respuestas.
7. El sistema debe aplicar reglas de anonimización, mostrando resultados solo cuando hay un mínimo de respuestas (configurable).

**HU-BE-EVALIN-010: Obtener Comentarios Cualitativos**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/evalin/reports/comments/{instructorId}` debe retornar comentarios cualitativos anonimizados para el instructor especificado.
2. El sistema debe verificar que el usuario tenga permisos adecuados (administrador o el instructor mismo si está autorizado).
3. El sistema debe aplicar técnicas de anonimización robustas para eliminar información que pueda identificar al aprendiz.
4. El sistema debe filtrar contenido inapropiado o ofensivo antes de retornar los comentarios.
5. La respuesta debe incluir metadatos como fecha del comentario y periodo de evaluación, sin revelar la identidad del aprendiz.
6. El sistema debe aplicar reglas de visualización, mostrando comentarios solo cuando hay un mínimo de evaluaciones (configurable).
7. La respuesta debe soportar paginación y filtrado por periodo de evaluación.

**HU-BE-EVALIN-011: Obtener Estado de Participación**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/evalin/reports/participation/{fichaId}` debe retornar estadísticas de participación para la ficha especificada.
2. El sistema debe verificar que el usuario tenga permisos adecuados (administrador o director de grupo de la ficha).
3. La respuesta debe incluir el porcentaje total de participación y desglose por aprendiz (completado/pendiente).
4. Para directores de grupo, la respuesta debe incluir información de contacto de los aprendices para facilitar recordatorios.
5. El sistema debe permitir filtrar por periodo de evaluación e instructor específico.
6. La respuesta debe incluir tendencias de participación si hay datos históricos disponibles.
7. El sistema debe actualizar estas estadísticas en tiempo real cuando se envían nuevas evaluaciones.

### ⚙️ Configuración y Notificaciones

**HU-BE-EVALIN-012: Gestionar Configuración del Módulo**

**Criterios de Aceptación:**

1. El endpoint `GET /api/v1/evalin/config` debe retornar la configuración actual del módulo EVALIN.
2. El endpoint `PUT /api/v1/evalin/config` debe validar y actualizar los parámetros de configuración proporcionados.
3. La configuración debe incluir parámetros como: número mínimo de respuestas para mostrar resultados, habilitar/deshabilitar comentarios cualitativos, umbral de anonimización.
4. El sistema debe proporcionar valores por defecto para todos los parámetros de configuración.
5. El sistema debe validar que los valores proporcionados estén dentro de rangos aceptables.
6. Los cambios en la configuración deben aplicarse inmediatamente a todas las operaciones subsecuentes.
7. Solo usuarios con rol de administrador deben poder ver y modificar la configuración.

**HU-BE-EVALIN-013: Enviar Notificaciones de Periodos**

**Criterios de Aceptación:**

1. El sistema debe enviar notificaciones automáticas cuando se active un nuevo periodo de evaluación.
2. Las notificaciones deben enviarse a todos los aprendices afectados por el periodo (según las fichas asociadas).
3. El contenido de la notificación debe incluir información sobre el periodo (fechas, instructores a evaluar).
4. El sistema debe registrar el envío de notificaciones y evitar duplicados.
5. El sistema debe manejar correctamente errores en el envío, implementando reintentos y logging.
6. Las notificaciones deben enviarse a través del sistema de notificaciones general de la plataforma.
7. El sistema debe proporcionar un endpoint para verificar el estado de las notificaciones enviadas.

**HU-BE-EVALIN-014: Enviar Recordatorios de Evaluación**

**Criterios de Aceptación:**

1. El endpoint `POST /api/v1/evalin/notifications/reminder/{fichaId}` debe enviar recordatorios a los aprendices de la ficha especificada.
2. El sistema debe verificar que el usuario tenga permisos adecuados (administrador o director de grupo de la ficha).
3. El sistema debe filtrar los destinatarios para incluir solo aprendices que no han completado todas sus evaluaciones.
4. La solicitud debe permitir personalizar el mensaje del recordatorio o usar una plantilla predefinida.
5. El sistema debe registrar el envío de recordatorios para evitar spam (limitando la frecuencia).
6. La respuesta debe incluir un resumen del envío: total de destinatarios, envíos exitosos, envíos fallidos.
7. El sistema debe proporcionar opciones para enviar recordatorios selectivos (a aprendices específicos) o masivos (a toda la ficha).

---

## 🏗️ Arquitectura y Calidad de Código

**HU-BE-047: Implementar Domain Layer**

**Criterios de Aceptación:**

1. Cada microservicio debe tener una carpeta `domain/` que contenga entidades, objetos de valor y reglas de negocio.
2. Las entidades del dominio deben ser independientes de frameworks específicos (sin dependencias de FastAPI, SQLAlchemy, etc.).
3. La lógica de negocio debe estar encapsulada en métodos de las entidades o servicios de dominio.
4. Las entidades deben validar su consistencia interna y lanzar excepciones de dominio apropiadas.
5. Los objetos de valor deben ser inmutables y contener validaciones específicas del dominio.
6. La capa de dominio no debe depender de ninguna capa externa (infraestructura, aplicación).
7. Todas las reglas de negocio críticas deben estar implementadas en la capa de dominio.

**HU-BE-048: Implementar Application Layer**

**Criterios de Aceptación:**

1. Cada microservicio debe tener una carpeta `application/` que contenga casos de uso y DTOs.
2. Los casos de uso deben orquestar las operaciones del dominio sin contener lógica de negocio.
3. Los casos de uso deben ser independientes de la capa de infraestructura usando interfaces (puertos).
4. Cada endpoint debe corresponder a un caso de uso específico en la capa de aplicación.
5. Los DTOs (Data Transfer Objects) deben manejar la transformación entre capas.
6. Los casos de uso deben manejar transacciones y coordinación entre múltiples entidades.
7. La capa de aplicación debe implementar validaciones de entrada y manejo de errores específicos.

**HU-BE-049: Implementar Infrastructure Layer**

**Criterios de Aceptación:**

1. Cada microservicio debe tener una carpeta `infrastructure/` que contenga adaptadores y configuraciones.
2. Los repositorios deben implementar interfaces definidas en la capa de dominio.
3. Las configuraciones de base de datos, APIs externas y servicios deben estar en esta capa.
4. Los adaptadores deben transformar datos entre el formato externo y las entidades de dominio.
5. La capa de infraestructura debe ser la única que contenga dependencias específicas del framework.
6. Los modelos de base de datos (SQLAlchemy) deben estar separados de las entidades de dominio.
7. La inyección de dependencias debe configurarse en esta capa.

**HU-BE-050: Refactorizar Microservicios Existentes**

**Criterios de Aceptación:**

1. La migración debe realizarse gradualmente, manteniendo la funcionalidad existente operativa.
2. Todos los tests existentes deben seguir pasando durante y después de la refactorización.
3. Los endpoints públicos no deben cambiar su contrato durante la migración.
4. Cada microservicio migrado debe mantener la misma performance o mejorarla.
5. El proceso de migración debe documentarse paso a paso para otros equipos.
6. Los microservicios migrados deben tener una estructura de carpetas consistente.
7. La migración debe completarse servicio por servicio, no todo el sistema simultáneamente.

**HU-BE-051: Implementar Unit Testing Completo**

**Criterios de Aceptación:**

1. Cada microservicio debe alcanzar al menos 90% de cobertura de código en tests unitarios.
2. Todos los casos de uso de la capa de aplicación deben tener tests unitarios.
3. Todas las entidades de dominio y su lógica de negocio deben estar completamente testeadas.
4. Los tests deben usar mocks para todas las dependencias externas.
5. Los tests unitarios deben ejecutarse en menos de 30 segundos por microservicio.
6. Cada test debe ser independiente y poder ejecutarse en cualquier orden.
7. Los tests deben seguir convenciones de naming claras (Arrange, Act, Assert).

**HU-BE-052: Implementar Integration Testing**

**Criterios de Aceptación:**

1. Cada endpoint público debe tener al menos un test de integración completo.
2. Los tests de integración deben validar el flujo completo desde HTTP hasta base de datos.
3. Los tests deben usar una base de datos de prueba aislada (TestContainers o similar).
4. Los tests de integración deben validar tanto casos exitosos como de error.
5. Los tests deben verificar la correcta serialización/deserialización de respuestas JSON.
6. Los tests de integración deben ejecutarse en menos de 2 minutos por microservicio.
7. Los tests deben incluir validación de headers, códigos de estado y estructura de respuesta.

**HU-BE-053: Implementar End-to-End Testing**

**Criterios de Aceptación:**

1. Los tests E2E deben validar flujos completos del usuario através múltiples microservicios.
2. Los tests deben incluir escenarios de autenticación y autorización completos.
3. Los tests E2E deben validar la comunicación entre API Gateway y microservicios.
4. Los tests deben simular cargas reales de trabajo con múltiples usuarios concurrentes.
5. Los tests E2E deben incluir validación de logs y métricas del sistema.
6. Los tests deben ejecutarse contra un entorno que simule producción (docker-compose).
7. Los tests E2E deben incluir escenarios de fallo y recuperación del sistema.

**HU-BE-054: Configurar Pipeline de Testing**

**Criterios de Aceptación:**

1. El pipeline de CI/CD debe ejecutar automáticamente todos los tipos de tests (unit, integration, E2E).
2. El pipeline debe impedir merges a main si algún test falla.
3. El pipeline debe generar reportes de cobertura de código automáticamente.
4. Los tests deben ejecutarse en paralelo para minimizar el tiempo total.
5. El pipeline debe ejecutar tests específicos según los archivos modificados.
6. El pipeline debe incluir análisis estático de código (linting, security scanning).
7. Los resultados de tests deben integrarse con herramientas de notificación del equipo.

---

**Nota:** Estos criterios de aceptación están diseñados para asegurar una implementación robusta de Clean Architecture que mejore la mantenibilidad, testabilidad y escalabilidad del sistema, siguiendo las mejores prácticas de desarrollo de software.
