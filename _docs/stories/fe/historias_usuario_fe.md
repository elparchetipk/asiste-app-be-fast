Historias de Usuario - Frontend (FE)

Actualizado: 13 de mayo de 2025

Estas historias describen las funcionalidades del frontend desde la perspectiva del usuario final. El estado actual de implementación se indica con los siguientes marcadores:

    ✅ Implementado: Funcionalidad completamente desarrollada y disponible.
    🚧 En desarrollo: Funcionalidad parcialmente implementada o en progreso.
    📋 Pendiente: Funcionalidad planificada pero aún no desarrollada.

Autenticación y Sesión

    HU-FE-001: Inicio de Sesión
        Como un usuario registrado (Aprendiz, Instructor, Administrador)
        Quiero poder ingresar mi identificador (documento o correo) y contraseña en una pantalla de login
        Para acceder a las funcionalidades de la aplicación correspondientes a mi rol.
        Estado: Implementado (app/login.tsx).

    HU-FE-002: Cierre de Sesión
        Como un usuario autenticado
        Quiero poder cerrar mi sesión activa
        Para proteger mi cuenta cuando termino de usar la aplicación o cambio de dispositivo.
        Estado: Implementado (botón en app/(tabs)/profile.tsx, llama a AuthContext).

    HU-FE-003: Solicitud de Recuperación de Contraseña
        Como un usuario que olvidó su contraseña
        Quiero poder ingresar mi número de documento en una pantalla específica
        Para solicitar instrucciones o un enlace para restablecer mi contraseña.
        Estado: Implementado (app/forgot-password.tsx).

    HU-FE-004: Cambio de Contraseña Obligatorio
        Como un usuario que inicia sesión por primera vez o con una contraseña temporal
        Quiero ser redirigido a una pantalla para establecer una nueva contraseña segura
        Para asegurar mi cuenta antes de acceder a las demás funcionalidades.
        Estado: Implementado (app/change-password.tsx), la redirección es manejada por AuthContext y app/_layout.tsx.

    HU-FE-029: Restablecimiento de Contraseña
        Como un usuario que ha solicitado recuperar su contraseña
        Quiero poder usar el enlace o token recibido por correo para establecer una nueva contraseña
        Para recuperar el acceso a mi cuenta de forma segura.
        Estado: Implementado (app/reset-password.tsx), asume que el usuario llega con el token (ej: deep link).

    HU-FE-030: Contexto de Autenticación
        Como desarrollador del frontend
        Quiero tener un contexto global de autenticación (AuthContext)
        Para gestionar el estado de sesión, tokens y datos de usuario de manera centralizada.
        Estado: Implementado (context/AuthContext.tsx).

    HU-FE-031: Navegación Basada en Autenticación
        Como usuario de la aplicación
        Quiero ser redirigido automáticamente a las pantallas apropiadas según mi estado de autenticación
        Para tener una experiencia de navegación fluida y segura.
        Estado: Implementado (lógica en app/_layout.tsx usando AuthContext).

    HU-FE-032: Cliente API Autenticado
        Como desarrollador del frontend
        Quiero tener un cliente HTTP que maneje automáticamente los tokens de autenticación
        Para realizar peticiones autenticadas a la API Gateway sin repetir código.
        Estado: Implementado (hooks/useApiClient.ts y services/apiClient.ts).

Panel Principal (Dashboard) - Rol Aprendiz

    HU-FE-005: Ver Panel Principal (Aprendiz)
        Como un Aprendiz autenticado
        Quiero ver mi panel principal personalizado al iniciar sesión (app/(tabs)/index.tsx)
        Para tener una vista general de mi información relevante.
        Estado: Pantalla base existe, muestra saludo. Pendiente contenido específico (horario, asistencia, alertas).

    HU-FE-006: Ver Saludo Personalizado (Aprendiz)
        Como un Aprendiz autenticado
        Quiero ver un mensaje de saludo con mi nombre en el panel principal
        Para sentir que la aplicación me reconoce.
        Estado: Implementado (usa datos del AuthContext).

    HU-FE-007: Ver Horario del Día (Aprendiz)
        Como un Aprendiz autenticado
        Quiero ver la lista de mis clases programadas para el día actual en mi panel principal
        Para saber rápidamente mis compromisos académicos del día.
        Estado: Pendiente (requiere integración con scheduleservice).

    HU-FE-008: Ver Resumen de Asistencia del Día (Aprendiz)
        Como un Aprendiz autenticado
        Quiero ver mi estado de asistencia general para el día actual en mi panel principal
        Para verificar rápidamente mi registro de asistencia diario.
        Estado: Pendiente (requiere integración con attendanceservice).

    HU-FE-009: Ver Alertas Pendientes (Aprendiz)
        Como un Aprendiz autenticado
        Quiero ver alertas importantes (Ej: fallas consecutivas) en mi panel principal
        Para estar al tanto de situaciones que requieren mi atención.
        Estado: Pendiente (requiere integración con attendanceservice).

    HU-FE-010: Ver Acciones Rápidas (Aprendiz)
        Como un Aprendiz autenticado
        Quiero ver enlaces o botones para acciones comunes en mi panel principal
        Para acceder fácilmente a otras funcionalidades.
        Estado: UI básica puede existir, funcionalidad completa pendiente.

Panel Principal (Dashboard) - Rol Instructor

    HU-FE-011: Ver Panel Principal (Instructor)
        Como un Instructor autenticado
        Quiero ver mi panel principal personalizado al iniciar sesión (app/(tabs)/index.tsx)
        Para tener una vista general de mis clases y tareas pendientes.
        Estado: Pantalla base existe, muestra saludo. Pendiente contenido específico (clases, justificaciones, alertas).

    HU-FE-012: Ver Clases del Día (Instructor)
        Como un Instructor autenticado
        Quiero ver la lista de mis clases programadas para el día actual
        Para saber mis compromisos académicos del día.
        Estado: Pendiente (requiere integración con scheduleservice).

    HU-FE-013: Acceder a Registrar Asistencia (Instructor)
        Como un Instructor autenticado
        Quiero tener un botón "Registrar Asistencia" junto a cada clase del día
        Para iniciar rápidamente el proceso de toma de asistencia.
        Estado: Pendiente (requiere UI y lógica de registro de asistencia).

    HU-FE-014: Ver Notificación de Justificaciones Pendientes (Instructor)
        Como un Instructor autenticado
        Quiero ver una notificación si tengo justificaciones pendientes de revisar
        Para estar al tanto y poder gestionarlas.
        Estado: Pendiente (requiere integración con attendanceservice).

    HU-FE-015: Ver Alertas de Aprendices (Instructor)
        Como un Instructor (especialmente director de ficha)
        Quiero ver alertas sobre aprendices con patrones de inasistencia preocupantes
        Para poder intervenir a tiempo.
        Estado: Pendiente (requiere integración con attendanceservice).

Panel Principal (Dashboard) - Rol Administrador

    HU-FE-016: Ver Panel Principal (Administrador)
        Como un Administrador autenticado
        Quiero ver un panel principal con accesos directos a las funciones administrativas (app/(tabs)/index.tsx)
        Para poder navegar eficientemente a las tareas de gestión.
        Estado: Pantalla base existe, muestra saludo. Pendiente contenido específico (accesos directos).

    HU-FE-017: Acceder a Gestión de Usuarios (Administrador)
        Como un Administrador autenticado
        Quiero tener un botón o enlace claro para "Gestionar Usuarios"
        Para poder administrar las cuentas del sistema.
        Estado: UI básica puede existir, funcionalidad completa pendiente (requiere integración con userservice admin endpoints).

    HU-FE-018: Acceder a Gestión de Horarios (Administrador)
        Como un Administrador autenticado
        Quiero tener un botón o enlace claro para "Gestionar Horarios"
        Para poder administrar los horarios de las fichas.
        Estado: Pendiente (requiere UI y integración con scheduleservice admin endpoints).

    HU-FE-019: Acceder a Carga Masiva de Datos (Administrador)
        Como un Administrador autenticado
        Quiero tener un botón o enlace claro para "Cargar Datos (CSV)"
        Para poder realizar cargas masivas de usuarios y horarios.
        Estado: Pendiente (requiere UI y integración con endpoints de carga masiva).

    HU-FE-020: Acceder a Gestión de Entidades Maestras (Administrador)
        Como un Administrador autenticado
        Quiero tener botones para gestionar "Programas", "Fichas", "Sedes", "Ambientes"
        Para mantener actualizada la información estructural.
        Estado: UI básica puede existir, funcionalidad completa pendiente (requiere integración con scheduleservice admin endpoints).

    HU-FE-031: Ver Alertas de Instructores Sin Lista de Asistencia (Administrador)
        Como un Administrador autenticado
        Quiero tener acceso a un panel de alertas que muestre instructores que no llamaron lista el día anterior
        Para poder tomar medidas administrativas y asegurar el correcto registro de asistencia.
        Estado: Implementado (app/admin/instructor-alerts.tsx y components/InstructorAlertsPanel.tsx).

Navegación y UI/UX

    HU-FE-021: Navegación por Pestañas
        Como usuario de la aplicación
        Quiero tener una barra de navegación inferior con pestañas para las principales secciones (Dashboard, Perfil, etc.)
        Para poder moverme fácilmente entre diferentes partes de la aplicación.
        Estado: Implementado (app/(tabs)/_layout.tsx).

    HU-FE-022: Perfil de Usuario
        Como usuario autenticado
        Quiero tener una pestaña o sección dedicada a mi perfil
        Para ver mi información básica y cerrar sesión.
        Estado: Implementado (app/(tabs)/profile.tsx), muestra info básica del token, botón logout funcional.

    HU-FE-023: Tema Adaptativo
        Como usuario de la aplicación
        Quiero que la interfaz se adapte al tema de mi dispositivo (claro/oscuro)
        Para tener una experiencia visual cómoda en diferentes condiciones.
        Estado: Implementado (usando useColorScheme, , Themed* components).

    HU-FE-024: Pantalla de Carga Animada
        Como usuario de la aplicación
        Quiero ver una pantalla de carga animada mientras la aplicación se inicializa
        Para tener feedback visual durante la carga inicial.
        Estado: Implementado (components/AnimatedSplashScreen.tsx).

Funcionalidades Adicionales (Pendientes)

    HU-FE-025: Editar Perfil de Usuario
        Como usuario autenticado
        Quiero poder editar información limitada de mi perfil (ej: foto, teléfono)
        Para mantener mis datos actualizados.
        Estado: Pendiente.

    HU-FE-026: Ver Historial de Asistencia Detallado
        Como usuario (Aprendiz o Instructor)
        Quiero acceder a un historial detallado de asistencias
        Para revisar los registros pasados.
        Estado: Pendiente (requiere UI y integración con attendanceservice).

    HU-FE-027: Enviar Justificación de Inasistencia
        Como Aprendiz
        Quiero poder subir un archivo PDF como justificación de una inasistencia
        Para explicar el motivo de mi ausencia.
        Estado: Pendiente (requiere UI y integración con attendanceservice).

    HU-FE-028: CRUD Completo de Entidades (Admin)
        Como Administrador
        Quiero interfaces completas para crear, leer, actualizar y eliminar entidades del sistema (Usuarios, Fichas, Programas, etc.)
        Para gestionar todos los datos maestros.
        Estado: Pendiente (requiere múltiples pantallas/componentes y integración con userservice y scheduleservice).

Funcionalidades de IA para Administradores

    HU-FE-031: Dashboard Predictivo de Deserción (Admin)
        Como un Administrador
        Quiero visualizar en mi dashboard un panel con métricas predictivas de deserción
        Para identificar tempranamente aprendices en riesgo y tomar acciones preventivas.
        Estado: Pendiente. Depende de HU-BE-021.

    HU-FE-032: Optimizador Inteligente de Horarios (Admin)
        Como un Administrador
        Quiero acceder a un módulo de optimización de horarios con visualizaciones de datos y recomendaciones
        Para tomar mejores decisiones en la distribución de actividades en próximos trimestres.
        Estado: Pendiente. Depende de HU-BE-022.

    HU-FE-033: Consultas en Lenguaje Natural (Admin)
        Como un Administrador
        Quiero disponer de un campo de búsqueda donde pueda escribir preguntas en lenguaje natural sobre los datos
        Para obtener rápidamente insights y visualizaciones sin necesidad de crear consultas técnicas.
        Estado: Pendiente. Depende de HU-BE-023.

    HU-FE-034: Validación Inteligente de CSV (Admin)
        Como un Administrador
        Quiero que al subir archivos CSV para carga masiva, estos sean analizados y validados por IA antes del procesamiento
        Para identificar posibles anomalías o inconsistencias y corregirlas antes de afectar los datos del sistema.
        Estado: Pendiente. Depende de HU-BE-024.

Funcionalidades de IA para Instructores

    HU-FE-035: Asistente de Gestión Proactiva (Instructor)
        Como un Instructor
        Quiero ver en mi dashboard recomendaciones personalizadas para cada aprendiz basadas en sus patrones de asistencia
        Para poder intervenir de manera proactiva en casos potencialmente problemáticos.
        Estado: Pendiente. Depende de HU-BE-025.

    HU-FE-036: Análisis Inteligente de Justificaciones (Instructor)
        Como un Instructor
        Quiero que al revisar una justificación, el sistema me muestre automáticamente información clave extraída del PDF y sugerencias basadas en precedentes
        Para tomar decisiones más informadas y consistentes sobre la aprobación o rechazo.
        Estado: Pendiente. Depende de HU-BE-026.

    HU-FE-037: Visualizador de Impacto de Asistencia (Instructor)
        Como un Instructor
        Quiero acceder a visualizaciones que muestren proyecciones del impacto de los patrones actuales de asistencia en el rendimiento
        Para comunicar efectivamente a los aprendices la importancia de la asistencia con datos concretos.
        Estado: Pendiente. Depende de HU-BE-027.

    HU-FE-038: Recomendador de Momentos para Registro de Asistencia (Instructor)
        Como un Instructor
        Quiero recibir sugerencias sobre los momentos óptimos para realizar los llamados a lista
        Para capturar de manera más precisa la asistencia real de los aprendices.
        Estado: Pendiente. Depende de HU-BE-028.

## Funcionalidad Offline

### HU-OFFLINE-CONFIG-SYNC

- **Como** usuario de la aplicación móvil,
- **Quiero** poder configurar mis preferencias de sincronización de datos (solo WiFi, WiFi o datos móviles),
- **Para** controlar el uso de mis datos móviles y optimizar la batería.
- **Prioridad:** Alta
- **Criterios de Aceptación:**
  - Debe existir una sección en la configuración de la app para ajustar esta preferencia.
  - Las opciones deben ser claras: "Solo WiFi", "WiFi y Datos Móviles".
  - La selección del usuario debe persistir entre sesiones.
  - La app debe respetar la configuración seleccionada para todas las operaciones de sincronización.
  - Por defecto, la app intentará sincronizar usando "WiFi y Datos Móviles", priorizando WiFi si está disponible.

### HU-OFFLINE-STATUS-INDICATOR

- **Como** usuario de la aplicación móvil,
- **Quiero** ver un indicador claro del estado de mi conexión a internet y del estado de la última sincronización,
- **Para** saber si mis datos están actualizados y si la app está operando online u offline.
- **Prioridad:** Alta
- **Criterios de Aceptación:**
  - Un indicador visual (ej. icono, texto) debe mostrar si hay conexión a internet (WiFi, Datos Móviles, Sin Conexión).
  - Se debe mostrar la fecha/hora de la última sincronización exitosa.
  - Si hay datos pendientes de sincronizar, se debe indicar de forma sutil (ej. un pequeño badge o icono).
  - El indicador debe actualizarse dinámicamente según cambie el estado de la red.

### HU-OFFLINE-REG-ASSIST (Instructor)

- **Como** instructor,
- **Quiero** poder registrar la asistencia de mis aprendices incluso cuando no tengo conexión a internet,
- **Para** cumplir con mis responsabilidades sin depender de la conectividad en el ambiente de formación.
- **Prioridad:** Alta
- **Criterios de Aceptación:**
  - La pantalla de registro de asistencia debe ser completamente funcional offline, cargando las fichas y aprendices desde datos locales.
  - Los datos de asistencia registrados offline deben guardarse localmente de forma segura en una cola de pendientes.
  - Al recuperar la conexión (según la configuración de HU-OFFLINE-CONFIG-SYNC), los datos de asistencia deben sincronizarse automáticamente con el servidor.
  - Se debe notificar al instructor visualmente el estado de la sincronización de cada registro (pendiente, sincronizando, sincronizado, error).
  - En caso de error de sincronización, el registro debe permanecer en la cola con indicación del error y opción de reintentar.
  - La interfaz debe mostrar claramente qué registros están pendientes de sincronizar.

### HU-OFFLINE-CREATE-JUST (Aprendiz)

- **Como** aprendiz,
- **Quiero** poder crear y guardar una justificación por inasistencia, incluyendo la posibilidad de adjuntar un archivo (si el sistema de archivos local lo permite y el archivo es accesible offline), incluso sin conexión a internet,
- **Para** poder registrar mi justificación tan pronto como sea posible, independientemente de mi conectividad.
- **Prioridad:** Alta
- **Criterios de Aceptación:**
  - El formulario de creación de justificaciones debe ser funcional offline.
  - Las justificaciones creadas offline (texto y referencia al adjunto) deben guardarse localmente en una cola de pendientes.
  - Si se adjunta un archivo, este debe almacenarse localmente de forma temporal y segura hasta su sincronización.
  - Al recuperar la conexión (según la configuración de HU-OFFLINE-CONFIG-SYNC), las justificaciones (incluyendo el adjunto) deben sincronizarse automáticamente con el servidor.
  - Se debe notificar al aprendiz visualmente el estado de la sincronización de su justificación.
  - En caso de error, la justificación debe permanecer en la cola con indicación del error y opción de reintentar.

### HU-OFFLINE-VIEW-SCHEDULE (Todos los roles)

- **Como** usuario (aprendiz o instructor),
- **Quiero** poder consultar mi horario académico almacenado localmente cuando no tengo conexión a internet,
- **Para** estar informado sobre mis clases y actividades programadas.
- **Prioridad:** Alta
- **Criterios de Aceptación:**
  - El horario académico del usuario (semanal/mensual según diseño) debe descargarse y almacenarse localmente durante una sincronización exitosa.
  - La vista de horario debe ser accesible y mostrar los datos almacenados localmente cuando la app está offline.
  - La interfaz debe indicar claramente que el horario mostrado es una versión offline y mostrar la fecha/hora de su última actualización desde el servidor.

### HU-OFFLINE-DATA-STORAGE

- **Como** aplicación móvil,
- **Necesito** almacenar localmente de forma segura los datos críticos para el funcionamiento offline,
- **Para** garantizar la disponibilidad de la información y las funcionalidades clave sin conexión.
- **Prioridad:** Alta
- **Criterios de Aceptación:**
  - Utilizar AsyncStorage o una base de datos local (ej. SQLite) para persistir datos.
  - Almacenar de forma segura tokens de autenticación para mantener la sesión offline.
  - Guardar datos de perfil del usuario, horarios, listas de asistencia (para instructores), y justificaciones pendientes (para aprendices).
  - Implementar un mecanismo de limpieza o gestión del almacenamiento local para evitar el uso excesivo de espacio.

### HU-OFFLINE-CONFLICT-HANDLING-FE

- **Como** aplicación móvil,
- **Necesito** manejar de forma básica los conflictos de datos que puedan ser informados por el backend durante la sincronización,
- **Para** informar al usuario y permitir acciones si es necesario.
- **Prioridad:** Media
- **Criterios de Aceptación:**
  - Si el backend reporta un conflicto que requiere intervención del usuario (poco común en la estrategia inicial), mostrar una notificación clara.
  - Para la estrategia inicial "servidor gana" o "último en escribir gana (manejado por BE)", la FE principalmente reflejará el estado final provisto por el BE tras la sincronización.
  - Registrar localmente los eventos de sincronización, incluyendo cualquier conflicto reportado o resuelto automáticamente.

Sistema de Respaldo y Recuperación Frontend

    HU-FE-039: Funcionamiento Sin Conexión para Registro de Asistencia
        Como Instructor
        Quiero poder registrar la asistencia de mi clase incluso cuando la aplicación no tiene conectividad a internet
        Para no depender de la disponibilidad de la red al momento de llamar a lista.
        Estado: En desarrollo.

    HU-FE-040: Sincronización Automática de Datos Offline
        Como usuario de la aplicación
        Quiero que los datos registrados sin conexión se sincronicen automáticamente cuando la conectividad se restablezca
        Para no tener que preocuparme manualmente por la sincronización de información.
        Estado: En desarrollo.

    HU-FE-041: Indicador de Estado de Sincronización
        Como usuario de la aplicación
        Quiero ver un indicador claro del estado de sincronización (sincronizado, pendiente, error)
        Para conocer si mis acciones han sido guardadas en el servidor central.
        Estado: Pendiente.

    HU-FE-042: Gestión de Conflictos de Datos
        Como usuario de la aplicación
        Quiero recibir notificaciones cuando existan conflictos entre mis datos locales y los del servidor
        Para poder resolver estos conflictos de forma informada.
        Estado: Pendiente.

    HU-FE-043: Recuperación de Sesión Interrumpida
        Como usuario de la aplicación
        Quiero que la aplicación restaure mi sesión y estado de trabajo si se cierra inesperadamente
        Para no perder información o progreso en mis tareas.
        Estado: Pendiente.
