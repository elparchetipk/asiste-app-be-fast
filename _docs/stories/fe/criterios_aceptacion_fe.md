# Criterios de Aceptación - Historias de Usuario Frontend

**Actualizado: 1 de junio de 2025**

Este documento define los criterios de aceptación detallados para las historias de usuario del frontend, proporcionando una guía clara para la implementación y verificación de cada funcionalidad.

## 📋 Documentación de Referencia

- **[Historias de Usuario Frontend](_docs/stories/fe/historias_usuario_fe.md)**: Especifica las funcionalidades desde la perspectiva del usuario final.
- **[Historias de Usuario KB Service Frontend](_docs/stories/fe/historias_usuario_fe_kbservice.md)**: Especifica las funcionalidades del servicio de Knowledge Base en el frontend.
- **[Historias de Usuario EVALIN Service Frontend](_docs/stories/fe/historias_usuario_fe_evalinservice.md)**: Especifica las funcionalidades del servicio de Evaluación de Instructores en el frontend.
- **[Requisitos Funcionales](../../general/rf.md)**: Contexto y requisitos generales del sistema.
- **[Requisitos Funcionales KB](../../general/rf_kb.md)**: Requisitos específicos del Knowledge Base Service.

## 🏷️ Estados de Implementación

- ✅ **Implementado**: Funcionalidad completamente desarrollada y verificada
- 🚧 **En desarrollo**: Funcionalidad parcialmente implementada o en progreso
- 📋 **Pendiente**: Funcionalidad planificada pero aún no desarrollada
- ❌ **Bloqueado**: Requiere dependencias o revisión de diseño

## 🔐 Autenticación y Sesión

**HU-FE-001: Inicio de Sesión**

**Criterios de Aceptación:**
1. La pantalla de login debe contener campos para ingresar identificador (documento o correo) y contraseña.
2. El sistema debe validar que ambos campos estén completos antes de enviar la solicitud al backend.
3. Si las credenciales son incorrectas, se debe mostrar un mensaje de error claro y específico.
4. Durante el proceso de autenticación, se debe mostrar un indicador de carga.
5. Al autenticarse exitosamente, el sistema debe almacenar de forma segura los tokens JWT (acceso y refresco).
6. El sistema debe redirigir al usuario a su panel principal correspondiente según su rol.
7. Si el usuario tiene el flag `must_change_password` en `true`, debe ser redirigido a la pantalla de cambio obligatorio de contraseña.

**HU-FE-002: Cierre de Sesión**

**Criterios de Aceptación:**
1. Debe existir un botón o enlace claramente visible para cerrar sesión en la pantalla de perfil.
2. Al hacer clic en cerrar sesión, se debe mostrar una confirmación para prevenir cierres accidentales.
3. Al confirmar, el sistema debe enviar una solicitud al endpoint `POST /api/v1/auth/logout`.
4. El sistema debe eliminar todos los tokens almacenados localmente.
5. El sistema debe limpiar cualquier dato sensible del usuario almacenado en el estado de la aplicación.
6. El usuario debe ser redirigido a la pantalla de login.
7. El proceso debe funcionar correctamente incluso si hay problemas de conectividad (offline).

**HU-FE-003: Solicitud de Recuperación de Contraseña**

**Criterios de Aceptación:**
1. Debe existir un enlace "Olvidé mi contraseña" en la pantalla de login.
2. La pantalla de recuperación debe contener un campo para ingresar el número de documento o correo electrónico.
3. El sistema debe validar que el campo esté completo antes de enviar la solicitud.
4. Durante el proceso, se debe mostrar un indicador de carga.
5. Después de enviar la solicitud, se debe mostrar un mensaje de confirmación indicando que se han enviado instrucciones al correo registrado.
6. El mensaje de confirmación debe mostrarse incluso si el documento/correo no existe (por seguridad).
7. Debe existir un enlace para volver a la pantalla de login.

**HU-FE-004: Cambio de Contraseña Obligatorio**

**Criterios de Aceptación:**
1. Si el usuario tiene el flag `must_change_password` en `true`, debe ser redirigido automáticamente a esta pantalla después del login.
2. La pantalla debe contener campos para ingresar la nueva contraseña y confirmarla.
3. El sistema debe validar que la nueva contraseña cumpla con los requisitos de seguridad (mínimo 10 caracteres, al menos una mayúscula, una minúscula, un dígito y un símbolo).
4. El sistema debe validar que ambos campos coincidan antes de enviar la solicitud.
5. Se debe mostrar feedback en tiempo real sobre el cumplimiento de los requisitos de seguridad.
6. Al completar el cambio exitosamente, el usuario debe ser redirigido a su panel principal.
7. El usuario no debe poder acceder a otras partes de la aplicación hasta que complete este proceso.

**HU-FE-029: Restablecimiento de Contraseña**

**Criterios de Aceptación:**
1. La aplicación debe poder procesar enlaces de restablecimiento de contraseña (deep links).
2. La pantalla debe extraer y validar el token de restablecimiento de la URL.
3. La pantalla debe contener campos para ingresar la nueva contraseña y confirmarla.
4. El sistema debe validar que la nueva contraseña cumpla con los requisitos de seguridad.
5. El sistema debe validar que ambos campos coincidan antes de enviar la solicitud.
6. Se debe mostrar feedback en tiempo real sobre el cumplimiento de los requisitos de seguridad.
7. Al completar el restablecimiento exitosamente, el usuario debe ser redirigido a la pantalla de login con un mensaje de éxito.

**HU-FE-030: Contexto de Autenticación**

**Criterios de Aceptación:**
1. El contexto de autenticación debe proporcionar métodos para login, logout y refresh token.
2. El contexto debe almacenar y proporcionar acceso seguro a los datos del usuario autenticado.
3. El contexto debe manejar automáticamente el refresco de tokens cuando estén próximos a expirar.
4. El contexto debe detectar y manejar tokens inválidos o expirados, redirigiendo al usuario al login cuando sea necesario.
5. El contexto debe proporcionar un método para verificar si el usuario está autenticado.
6. El contexto debe proporcionar un método para verificar el rol del usuario.
7. El contexto debe ser accesible desde cualquier componente de la aplicación.

**HU-FE-031: Navegación Basada en Autenticación**

**Criterios de Aceptación:**
1. La aplicación debe redirigir a usuarios no autenticados a la pantalla de login.
2. La aplicación debe redirigir a usuarios autenticados con `must_change_password` en `true` a la pantalla de cambio obligatorio de contraseña.
3. La aplicación debe redirigir a usuarios autenticados normales a su panel principal según su rol.
4. La navegación debe proteger rutas que requieren autenticación.
5. La navegación debe proteger rutas que requieren roles específicos.
6. Las redirecciones deben ocurrir automáticamente sin intervención del usuario.
7. La navegación debe manejar correctamente el estado de carga inicial mientras se verifica la autenticación.

**HU-FE-032: Cliente API Autenticado**

**Criterios de Aceptación:**
1. El cliente API debe incluir automáticamente el token de acceso en todas las peticiones.
2. El cliente debe manejar errores 401 (Unauthorized) intentando refrescar el token y reintentando la petición.
3. Si el refresco falla, el cliente debe notificar al contexto de autenticación para cerrar la sesión.
4. El cliente debe proporcionar métodos para realizar peticiones GET, POST, PUT y DELETE.
5. El cliente debe manejar correctamente la serialización y deserialización de datos JSON.
6. El cliente debe proporcionar un mecanismo para cancelar peticiones en curso.
7. El cliente debe incluir manejo de timeouts y reintentos para peticiones fallidas por problemas de red.

## 📊 Panel Principal (Dashboard) - Rol Aprendiz

**HU-FE-005: Ver Panel Principal (Aprendiz)**

**Criterios de Aceptación:**
1. El panel principal debe cargarse automáticamente después del login exitoso para usuarios con rol de aprendiz.
2. El panel debe mostrar un saludo personalizado con el nombre del aprendiz.
3. El panel debe mostrar la información del horario del día actual.
4. El panel debe mostrar un resumen del estado de asistencia del día.
5. El panel debe mostrar alertas pendientes si existen.
6. El panel debe incluir acciones rápidas para funcionalidades frecuentes.
7. El diseño debe ser responsivo y adaptarse a diferentes tamaños de pantalla.

**HU-FE-006: Ver Saludo Personalizado (Aprendiz)**

**Criterios de Aceptación:**
1. El saludo debe incluir el nombre del aprendiz obtenido del contexto de autenticación.
2. El saludo debe variar según la hora del día ("Buenos días", "Buenas tardes", "Buenas noches").
3. El saludo debe ser visible en la parte superior del panel principal.
4. El texto debe tener un tamaño y estilo que lo haga fácilmente legible.
5. El componente debe manejar correctamente nombres largos sin romper el diseño.
6. El componente debe manejar correctamente la ausencia de nombre mostrando un saludo genérico.
7. El componente debe actualizarse si los datos del usuario cambian durante la sesión.

**HU-FE-007: Ver Horario del Día (Aprendiz)**

**Criterios de Aceptación:**
1. El panel debe mostrar la lista de clases programadas para el día actual.
2. Cada entrada debe mostrar hora de inicio, hora de fin, nombre de la actividad, nombre del instructor y ubicación (ambiente).
3. Las clases deben estar ordenadas cronológicamente.
4. Las clases en curso o próximas deben destacarse visualmente.
5. Si no hay clases programadas para el día, se debe mostrar un mensaje informativo.
6. Durante la carga de datos, se debe mostrar un indicador de carga.
7. En caso de error al cargar los datos, se debe mostrar un mensaje de error con opción de reintentar.

**HU-FE-008: Ver Resumen de Asistencia del Día (Aprendiz)**

**Criterios de Aceptación:**
1. El panel debe mostrar un resumen visual del estado de asistencia del día actual.
2. El resumen debe indicar claramente si el aprendiz ha sido registrado como presente, ausente o si la asistencia aún no ha sido tomada.
3. Para cada clase del día, se debe mostrar el estado de asistencia correspondiente.
4. Si hay ausencias, debe existir un enlace para crear una justificación.
5. Durante la carga de datos, se debe mostrar un indicador de carga.
6. En caso de error al cargar los datos, se debe mostrar un mensaje de error con opción de reintentar.
7. El componente debe actualizarse automáticamente si se registra nueva asistencia durante la sesión.

**HU-FE-009: Ver Alertas Pendientes (Aprendiz)**

**Criterios de Aceptación:**
1. El panel debe mostrar alertas importantes relacionadas con la asistencia del aprendiz.
2. Las alertas deben categorizarse por nivel de criticidad (alta, media, baja) con indicadores visuales claros.
3. Cada alerta debe incluir una descripción clara del problema y acciones recomendadas.
4. Las alertas de alta criticidad deben destacarse visualmente.
5. Debe existir una opción para marcar alertas como leídas o descartarlas.
6. Si no hay alertas, esta sección debe ocultarse o mostrar un mensaje informativo.
7. Las alertas deben actualizarse automáticamente cuando cambien los datos de asistencia.

**HU-FE-010: Ver Acciones Rápidas (Aprendiz)**

**Criterios de Aceptación:**
1. El panel debe incluir botones o enlaces para acciones frecuentes como "Ver horario completo", "Historial de asistencia" y "Crear justificación".
2. Los botones deben tener iconos intuitivos y texto descriptivo.
3. Los botones deben tener un tamaño adecuado para facilitar la interacción táctil.
4. Al hacer clic en cada botón, el usuario debe ser redirigido a la pantalla correspondiente.
5. Los botones deben estar organizados según frecuencia de uso o importancia.
6. El diseño debe ser responsivo y adaptarse a diferentes tamaños de pantalla.
7. Los botones deben tener estados visuales para hover, active y focus.

## 📊 Panel Principal (Dashboard) - Rol Instructor

**HU-FE-011: Ver Panel Principal (Instructor)**

**Criterios de Aceptación:**
1. El panel principal debe cargarse automáticamente después del login exitoso para usuarios con rol de instructor.
2. El panel debe mostrar un saludo personalizado con el nombre del instructor.
3. El panel debe mostrar la lista de clases programadas para el día actual.
4. El panel debe mostrar notificaciones sobre justificaciones pendientes de revisar.
5. El panel debe mostrar alertas sobre aprendices con patrones de inasistencia preocupantes.
6. El panel debe incluir acciones rápidas para funcionalidades frecuentes.
7. El diseño debe ser responsivo y adaptarse a diferentes tamaños de pantalla.

**HU-FE-012: Ver Clases del Día (Instructor)**

**Criterios de Aceptación:**
1. El panel debe mostrar la lista de clases programadas para el día actual.
2. Cada entrada debe mostrar hora de inicio, hora de fin, nombre de la actividad, ficha y ubicación (ambiente).
3. Las clases deben estar ordenadas cronológicamente.
4. Las clases en curso o próximas deben destacarse visualmente.
5. Cada clase debe indicar si ya se ha registrado asistencia o no.
6. Durante la carga de datos, se debe mostrar un indicador de carga.
7. En caso de error al cargar los datos, se debe mostrar un mensaje de error con opción de reintentar.

**HU-FE-013: Acceder a Registrar Asistencia (Instructor)**

**Criterios de Aceptación:**
1. Cada clase del día debe tener un botón "Registrar Asistencia" claramente visible.
2. El botón debe estar deshabilitado o mostrar un estado diferente si ya se registró asistencia para esa clase.
3. Al hacer clic en el botón, el instructor debe ser redirigido a la pantalla de registro de asistencia para esa clase específica.
4. La pantalla de registro debe cargarse con la información correcta de la clase seleccionada.
5. Si la clase aún no ha comenzado, se debe mostrar una advertencia pero permitir el registro.
6. Si la clase ya terminó, se debe mostrar una advertencia pero permitir el registro.
7. El botón debe tener un tamaño adecuado para facilitar la interacción táctil.

**HU-FE-014: Ver Notificación de Justificaciones Pendientes (Instructor)**

**Criterios de Aceptación:**
1. El panel debe mostrar una notificación clara si hay justificaciones pendientes de revisar.
2. La notificación debe indicar el número de justificaciones pendientes.
3. La notificación debe incluir un enlace para acceder directamente a la lista de justificaciones.
4. La notificación debe destacarse visualmente para llamar la atención del instructor.
5. Si no hay justificaciones pendientes, esta sección debe ocultarse o mostrar un mensaje informativo.
6. La notificación debe actualizarse automáticamente si se reciben nuevas justificaciones durante la sesión.
7. Al hacer clic en la notificación, el instructor debe ser redirigido a la pantalla de gestión de justificaciones.

**HU-FE-015: Ver Alertas de Aprendices (Instructor)**

**Criterios de Aceptación:**
1. El panel debe mostrar alertas sobre aprendices con patrones de inasistencia preocupantes.
2. Las alertas deben categorizarse por nivel de criticidad (alta, media, baja) con indicadores visuales claros.
3. Cada alerta debe incluir el nombre del aprendiz, la ficha, el patrón detectado y acciones recomendadas.
4. Las alertas de alta criticidad deben destacarse visualmente.
5. Debe existir una opción para ver más detalles de cada alerta.
6. Si no hay alertas, esta sección debe ocultarse o mostrar un mensaje informativo.
7. Las alertas deben actualizarse automáticamente cuando cambien los datos de asistencia.

## 📊 Panel Principal (Dashboard) - Rol Administrador

**HU-FE-016: Ver Panel Principal (Administrador)**

**Criterios de Aceptación:**
1. El panel principal debe cargarse automáticamente después del login exitoso para usuarios con rol de administrador.
2. El panel debe mostrar un saludo personalizado con el nombre del administrador.
3. El panel debe incluir accesos directos a las principales funciones administrativas.
4. El panel debe mostrar un resumen de métricas clave del sistema.
5. El panel debe mostrar alertas importantes que requieran atención administrativa.
6. El diseño debe ser responsivo y adaptarse a diferentes tamaños de pantalla.
7. El panel debe organizarse de manera que las funciones más importantes sean fácilmente accesibles.

**HU-FE-017: Acceder a Gestión de Usuarios (Administrador)**

**Criterios de Aceptación:**
1. El panel debe incluir un botón o enlace claramente visible para "Gestionar Usuarios".
2. El botón debe tener un icono intuitivo y texto descriptivo.
3. Al hacer clic en el botón, el administrador debe ser redirigido a la pantalla de gestión de usuarios.
4. La pantalla de gestión debe cargar correctamente la lista de usuarios del sistema.
5. La pantalla debe incluir funcionalidades para buscar, filtrar, crear, editar y desactivar usuarios.
6. El botón debe tener un tamaño adecuado para facilitar la interacción táctil.
7. El botón debe tener estados visuales para hover, active y focus.

**HU-FE-018: Acceder a Gestión de Horarios (Administrador)**

**Criterios de Aceptación:**
1. El panel debe incluir un botón o enlace claramente visible para "Gestionar Horarios".
2. El botón debe tener un icono intuitivo y texto descriptivo.
3. Al hacer clic en el botón, el administrador debe ser redirigido a la pantalla de gestión de horarios.
4. La pantalla de gestión debe cargar correctamente la información de horarios del sistema.
5. La pantalla debe incluir funcionalidades para buscar, filtrar, crear, editar y eliminar horarios.
6. El botón debe tener un tamaño adecuado para facilitar la interacción táctil.
7. El botón debe tener estados visuales para hover, active y focus.

**HU-FE-019: Acceder a Carga Masiva de Datos (Administrador)**

**Criterios de Aceptación:**
1. El panel debe incluir un botón o enlace claramente visible para "Cargar Datos (CSV)".
2. El botón debe tener un icono intuitivo y texto descriptivo.
3. Al hacer clic en el botón, el administrador debe ser redirigido a la pantalla de carga masiva de datos.
4. La pantalla debe permitir seleccionar el tipo de datos a cargar (usuarios, horarios, etc.).
5. La pantalla debe permitir seleccionar y subir un archivo CSV.
6. La pantalla debe mostrar el progreso de la carga y un resumen de resultados al finalizar.
7. La pantalla debe manejar y mostrar claramente los errores que puedan ocurrir durante la carga.

**HU-FE-020: Acceder a Gestión de Entidades Maestras (Administrador)**

**Criterios de Aceptación:**
1. El panel debe incluir botones o enlaces claramente visibles para gestionar "Programas", "Fichas", "Sedes" y "Ambientes".
2. Cada botón debe tener un icono intuitivo y texto descriptivo.
3. Al hacer clic en cada botón, el administrador debe ser redirigido a la pantalla de gestión correspondiente.
4. Cada pantalla de gestión debe cargar correctamente la información de la entidad seleccionada.
5. Cada pantalla debe incluir funcionalidades para buscar, filtrar, crear, editar y eliminar entidades.
6. Los botones deben tener un tamaño adecuado para facilitar la interacción táctil.
7. Los botones deben tener estados visuales para hover, active y focus.

**HU-FE-031: Ver Alertas de Instructores Sin Lista de Asistencia (Administrador)**

**Criterios de Aceptación:**
1. El panel debe incluir un acceso a un panel de alertas que muestre instructores que no llamaron lista el día anterior.
2. El panel de alertas debe mostrar una lista clara de instructores, con detalles de la ficha, bloque horario y ambiente.
3. La lista debe estar ordenada por instructor y hora para facilitar la revisión.
4. El panel debe incluir opciones para filtrar por sede, programa o ficha.
5. Cada entrada debe incluir una opción para contactar al instructor directamente.
6. El panel debe actualizarse automáticamente cada día con nueva información.
7. Si no hay alertas, el panel debe mostrar un mensaje informativo.

## 🧭 Navegación y UI/UX

**HU-FE-021: Navegación por Pestañas**

**Criterios de Aceptación:**
1. La aplicación debe tener una barra de navegación inferior con pestañas para las principales secciones.
2. Las pestañas deben incluir al menos "Inicio", "Horario", "Asistencia" y "Perfil".
3. Las pestañas deben tener iconos intuitivos y etiquetas de texto.
4. La pestaña activa debe destacarse visualmente.
5. La navegación debe ser fluida y sin retrasos perceptibles.
6. La barra de navegación debe ser accesible desde cualquier pantalla principal.
7. La barra de navegación debe adaptarse según el rol del usuario, mostrando solo las secciones relevantes.

**HU-FE-022: Perfil de Usuario**

**Criterios de Aceptación:**
1. La pestaña de perfil debe mostrar la información básica del usuario: nombre, apellido, documento, email, rol.
2. La pantalla debe incluir una opción para cerrar sesión claramente visible.
3. La pantalla debe mostrar la versión de la aplicación.
4. Si el rol lo permite, debe incluir un enlace para editar información limitada del perfil.
5. La información debe obtenerse del contexto de autenticación.
6. Durante la carga de datos adicionales, se debe mostrar un indicador de carga.
7. En caso de error al cargar datos adicionales, se debe mostrar un mensaje de error con opción de reintentar.

**HU-FE-023: Tema Adaptativo**

**Criterios de Aceptación:**
1. La interfaz debe adaptarse automáticamente al tema del dispositivo (claro/oscuro).
2. Todos los componentes deben tener estilos definidos para ambos temas.
3. Los colores deben tener suficiente contraste en ambos temas para garantizar la legibilidad.
4. Las transiciones entre temas deben ser suaves si el usuario cambia la configuración del dispositivo durante el uso.
5. Los iconos y gráficos deben ser visibles y claros en ambos temas.
6. El tema debe aplicarse consistentemente en toda la aplicación, incluyendo modales y diálogos.
7. El tema debe respetar las preferencias de accesibilidad del usuario.

**HU-FE-024: Pantalla de Carga Animada**

**Criterios de Aceptación:**
1. Durante la inicialización de la aplicación, se debe mostrar una pantalla de carga animada.
2. La animación debe incluir el logo de la aplicación y un indicador de progreso.
3. La animación debe ser fluida y profesional.
4. La pantalla de carga debe mostrarse hasta que se complete la inicialización de la aplicación y la verificación de autenticación.
5. La transición a la siguiente pantalla (login o dashboard) debe ser suave.
6. La pantalla de carga debe adaptarse a ambos temas (claro/oscuro).
7. La pantalla de carga debe ser responsiva y verse correctamente en diferentes tamaños de pantalla.

## 📱 Funcionalidades Adicionales

**HU-FE-025: Editar Perfil de Usuario**

**Criterios de Aceptación:**
1. Debe existir una pantalla para editar información limitada del perfil (foto, teléfono).
2. La pantalla debe mostrar los valores actuales de los campos editables.
3. La pantalla debe incluir validación para cada campo editable.
4. Al guardar cambios, se debe mostrar un indicador de progreso.
5. Después de guardar exitosamente, se debe mostrar un mensaje de confirmación.
6. En caso de error al guardar, se debe mostrar un mensaje claro con la opción de reintentar.
7. Debe existir un botón para cancelar la edición y volver a la pantalla de perfil sin guardar cambios.

**HU-FE-026: Ver Historial de Asistencia Detallado**

**Criterios de Aceptación:**
1. Debe existir una pantalla para ver el historial detallado de asistencia.
2. La pantalla debe permitir filtrar por período (desde/hasta).
3. Para aprendices, debe mostrar su historial personal.
4. Para instructores, debe permitir seleccionar una ficha y ver el historial de todos los aprendices.
5. Cada registro debe mostrar fecha, bloque horario, estado (presente, ausente, justificado) y detalles adicionales.
6. La pantalla debe incluir estadísticas resumidas (porcentaje de asistencia, ausencias totales, justificadas).
7. Los datos deben presentarse en un formato claro y fácil de interpretar, posiblemente con códigos de color.

**HU-FE-027: Enviar Justificación de Inasistencia**

**Criterios de Aceptación:**
1. Debe existir una pantalla para enviar justificaciones de inasistencia.
2. La pantalla debe permitir seleccionar la fecha y bloque horario de la inasistencia.
3. La pantalla debe incluir un campo para describir el motivo de la inasistencia.
4. La pantalla debe permitir adjuntar un archivo PDF como evidencia.
5. El sistema debe validar que el archivo no exceda un tamaño máximo (5MB).
6. Al enviar la justificación, se debe mostrar un indicador de progreso.
7. Después de enviar exitosamente, se debe mostrar un mensaje de confirmación y redirigir al historial de asistencia.

**HU-FE-028: CRUD Completo de Entidades (Admin)**

**Criterios de Aceptación:**
1. Deben existir interfaces completas para gestionar usuarios, fichas, programas, sedes y ambientes.
2. Cada interfaz debe incluir una lista paginada de entidades con opciones de búsqueda y filtrado.
3. Cada interfaz debe permitir crear nuevas entidades con validación de campos.
4. Cada interfaz debe permitir ver detalles completos de una entidad.
5. Cada interfaz debe permitir editar entidades existentes con validación de campos.
6. Cada interfaz debe permitir eliminar o desactivar entidades con confirmación.
7. Todas las operaciones deben mostrar indicadores de progreso y mensajes de éxito o error.

## 🤖 Funcionalidades de IA para Administradores

**HU-FE-031: Dashboard Predictivo de Deserción (Admin)**

**Criterios de Aceptación:**
1. Debe existir un panel con métricas predictivas de deserción accesible para administradores.
2. El panel debe mostrar una lista de aprendices en riesgo, ordenados por nivel de riesgo.
3. Cada entrada debe incluir el nombre del aprendiz, ficha, score de riesgo y factores contribuyentes.
4. El panel debe incluir visualizaciones gráficas que muestren tendencias y patrones.
5. El panel debe permitir filtrar por ficha, programa o nivel de riesgo.
6. Al seleccionar un aprendiz, se deben mostrar detalles adicionales y recomendaciones específicas.
7. Los datos deben actualizarse automáticamente o incluir una opción para refrescar manualmente.

**HU-FE-032: Optimizador Inteligente de Horarios (Admin)**

**Criterios de Aceptación:**
1. Debe existir un módulo de optimización de horarios accesible para administradores.
2. El módulo debe mostrar visualizaciones de la distribución horaria actual con métricas de eficiencia.
3. El módulo debe generar recomendaciones específicas para optimizar la distribución.
4. Cada recomendación debe incluir una justificación clara y el impacto esperado.
5. El módulo debe permitir simular los cambios propuestos antes de aplicarlos.
6. El módulo debe mostrar métricas comparativas entre la distribución actual y la optimizada.
7. Las recomendaciones deben considerar patrones históricos de asistencia, disponibilidad de ambientes y preferencias registradas.

**HU-FE-033: Consultas en Lenguaje Natural (Admin)**

**Criterios de Aceptación:**
1. Debe existir un campo de búsqueda donde los administradores puedan escribir preguntas en lenguaje natural.
2. El sistema debe interpretar la intención de la consulta y mostrar resultados relevantes.
3. Los resultados deben incluir visualizaciones apropiadas según el tipo de consulta.
4. El sistema debe soportar consultas comparativas, de tendencias, correlaciones y anomalías.
5. Junto con los datos, debe mostrarse una interpretación en lenguaje natural de los resultados.
6. El sistema debe manejar consultas ambiguas solicitando clarificación.
7. Debe existir un historial de consultas recientes para facilitar el acceso a análisis previos.

**HU-FE-034: Validación Inteligente de CSV (Admin)**

**Criterios de Aceptación:**
1. En la pantalla de carga masiva, debe existir una opción para validar el CSV antes de procesarlo.
2. El sistema debe analizar el archivo y detectar posibles anomalías o inconsistencias.
3. Los resultados de la validación deben categorizarse por severidad (críticos, advertencias, sugerencias).
4. Cada hallazgo debe incluir una descripción clara del problema y recomendaciones para corregirlo.
5. El sistema debe proporcionar estadísticas sobre el archivo (número de registros, distribución de valores).
6. Debe existir una opción para descargar un reporte detallado de la validación.
7. El usuario debe poder decidir si proceder con la carga a pesar de las advertencias.

## 🤖 Funcionalidades de IA para Instructores

**HU-FE-035: Asistente de Gestión Proactiva (Instructor)**

**Criterios de Aceptación:**
1. El dashboard del instructor debe incluir recomendaciones personalizadas para cada aprendiz basadas en patrones de asistencia.
2. Las recomendaciones deben categorizarse por urgencia y tipo de intervención.
3. Cada recomendación debe incluir el contexto (datos que la justifican) y acciones sugeridas.
4. El instructor debe poder marcar recomendaciones como implementadas o descartadas.
5. El sistema debe aprender de las acciones del instructor para mejorar futuras recomendaciones.
6. Las recomendaciones deben actualizarse automáticamente cuando cambien los patrones de asistencia.
7. Debe existir una opción para ver el historial de recomendaciones y sus resultados.

**HU-FE-036: Análisis Inteligente de Justificaciones (Instructor)**

**Criterios de Aceptación:**
1. Al revisar una justificación, el sistema debe mostrar automáticamente información clave extraída del PDF.
2. La información extraída debe incluir tipo de justificación, fechas mencionadas, entidades emisoras y firmas detectadas.
3. El sistema debe verificar la consistencia interna del documento y destacar posibles anomalías.
4. El sistema debe mostrar sugerencias basadas en precedentes (casos similares anteriores).
5. El instructor debe poder ver la justificación original junto con el análisis.
6. El sistema debe proporcionar una recomendación preliminar (aprobar/rechazar) con su justificación.
7. El instructor debe mantener la decisión final, pudiendo aceptar o ignorar la recomendación del sistema.

**HU-FE-037: Visualizador de Impacto de Asistencia (Instructor)**

**Criterios de Aceptación:**
1. Debe existir una pantalla con visualizaciones que muestren proyecciones del impacto de los patrones de asistencia.
2. Las visualizaciones deben incluir gráficos de tendencias, comparativas y proyecciones.
3. El sistema debe mostrar correlaciones entre asistencia y otros factores relevantes.
4. Las visualizaciones deben ser interactivas, permitiendo al instructor explorar diferentes escenarios.
5. El sistema debe generar automáticamente insights clave basados en los datos.
6. Las visualizaciones deben ser exportables para usar en comunicaciones con aprendices.
7. Los datos deben actualizarse automáticamente para reflejar la información más reciente.

**HU-FE-038: Recomendador de Momentos para Registro de Asistencia (Instructor)**

**Criterios de Aceptación:**
1. El sistema debe sugerir momentos óptimos para realizar los llamados a lista.
2. Las sugerencias deben basarse en análisis de patrones históricos de asistencia.
3. Cada sugerencia debe incluir una justificación clara y el beneficio esperado.
4. Las sugerencias deben adaptarse a las características específicas de cada ficha y actividad.
5. El sistema debe aprender de los resultados para mejorar futuras recomendaciones.
6. Las sugerencias deben presentarse de manera no intrusiva en el dashboard del instructor.
7. El instructor debe poder configurar sus preferencias para este tipo de recomendaciones.

## 📱 Funcionalidad Offline

**HU-OFFLINE-CONFIG-SYNC: Configuración de Sincronización**

**Criterios de Aceptación:**
1. Debe existir una sección en la configuración de la app para ajustar preferencias de sincronización.
2. Las opciones deben incluir "Solo WiFi" y "WiFi y Datos Móviles" con descripciones claras.
3. La selección debe guardarse localmente y persistir entre sesiones.
4. La aplicación debe respetar la configuración seleccionada para todas las operaciones de sincronización.
5. Debe existir un indicador visual que muestre la configuración actual.
6. El valor predeterminado debe ser "WiFi y Datos Móviles", priorizando WiFi si está disponible.
7. Los cambios en la configuración deben aplicarse inmediatamente sin necesidad de reiniciar la aplicación.

**HU-OFFLINE-STATUS-INDICATOR: Indicador de Estado de Conexión**

**Criterios de Aceptación:**
1. La aplicación debe mostrar un indicador visual del estado de conexión a internet.
2. El indicador debe diferenciar entre WiFi, Datos Móviles y Sin Conexión con iconos claros.
3. Junto al estado de conexión, debe mostrarse la fecha y hora de la última sincronización exitosa.
4. Si hay datos pendientes de sincronizar, debe mostrarse un badge o icono indicativo.
5. El indicador debe actualizarse en tiempo real cuando cambie el estado de la red.
6. El indicador debe ser visible pero no intrusivo en la interfaz.
7. Al tocar el indicador, debe mostrarse información adicional sobre el estado de sincronización.

**HU-OFFLINE-REG-ASSIST: Registro de Asistencia Offline (Instructor)**

**Criterios de Aceptación:**
1. La pantalla de registro de asistencia debe funcionar completamente sin conexión a internet.
2. La aplicación debe cargar fichas y aprendices desde datos almacenados localmente.
3. Los registros de asistencia realizados offline deben guardarse localmente en una cola de pendientes.
4. Al recuperar conexión, los datos deben sincronizarse automáticamente según la configuración.
5. Cada registro debe mostrar claramente su estado (pendiente, sincronizando, sincronizado, error).
6. En caso de error de sincronización, debe mostrarse el motivo y ofrecer la opción de reintentar.
7. La interfaz debe mostrar claramente qué registros están pendientes de sincronizar.

**HU-OFFLINE-CREATE-JUST: Creación de Justificaciones Offline (Aprendiz)**

**Criterios de Aceptación:**
1. El formulario de creación de justificaciones debe funcionar sin conexión a internet.
2. Las justificaciones creadas offline deben guardarse localmente en una cola de pendientes.
3. Si se adjunta un archivo, debe almacenarse localmente hasta su sincronización.
4. Al recuperar conexión, las justificaciones deben sincronizarse automáticamente según la configuración.
5. Cada justificación debe mostrar claramente su estado (pendiente, sincronizando, sincronizada, error).
6. En caso de error de sincronización, debe mostrarse el motivo y ofrecer la opción de reintentar.
7. La interfaz debe mostrar claramente qué justificaciones están pendientes de sincronizar.

**HU-OFFLINE-VIEW-SCHEDULE: Visualización de Horario Offline**

**Criterios de Aceptación:**
1. La vista de horario debe ser accesible y funcional sin conexión a internet.
2. El horario debe cargarse desde datos almacenados localmente durante la última sincronización.
3. La interfaz debe indicar claramente que se está mostrando una versión offline del horario.
4. Debe mostrarse la fecha y hora de la última actualización desde el servidor.
5. Si hay cambios pendientes de sincronizar, debe indicarse claramente.
6. La vista debe incluir todas las funcionalidades de filtrado y navegación, operando sobre datos locales.
7. Al recuperar conexión, debe ofrecerse la opción de actualizar los datos.

**HU-OFFLINE-DATA-STORAGE: Almacenamiento Local de Datos**

**Criterios de Aceptación:**
1. La aplicación debe utilizar AsyncStorage o una base de datos local para persistir datos críticos.
2. Los tokens de autenticación deben almacenarse de forma segura para mantener la sesión offline.
3. Deben almacenarse localmente: datos de perfil, horarios, listas de asistencia y justificaciones pendientes.
4. La aplicación debe implementar un mecanismo de limpieza para evitar el uso excesivo de almacenamiento.
5. Los datos sensibles deben almacenarse de forma segura, preferiblemente encriptados.
6. La aplicación debe manejar correctamente errores de almacenamiento (ej. espacio insuficiente).
7. Debe existir un mecanismo para verificar la integridad de los datos almacenados localmente.

**HU-OFFLINE-CONFLICT-HANDLING-FE: Manejo de Conflictos de Datos**

**Criterios de Aceptación:**
1. La aplicación debe manejar conflictos reportados por el backend durante la sincronización.
2. Si se requiere intervención del usuario, debe mostrarse una notificación clara con opciones.
3. Para la estrategia "servidor gana", la aplicación debe actualizar los datos locales según lo indicado por el backend.
4. La aplicación debe registrar localmente eventos de sincronización, incluyendo conflictos.
5. El usuario debe poder ver un historial de sincronizaciones y conflictos en la configuración.
6. La interfaz debe explicar claramente la naturaleza del conflicto y las opciones disponibles.
7. Después de resolver un conflicto, la aplicación debe actualizar la interfaz para reflejar el estado final.

## 💾 Sistema de Respaldo y Recuperación Frontend

**HU-FE-039: Funcionamiento Sin Conexión para Registro de Asistencia**

**Criterios de Aceptación:**
1. La funcionalidad de registro de asistencia debe estar disponible sin conexión a internet.
2. La aplicación debe cargar y mostrar la lista de aprendices desde datos almacenados localmente.
3. El instructor debe poder marcar asistencia para cada aprendiz sin conexión.
4. Los datos de asistencia deben guardarse localmente hasta que se pueda sincronizar.
5. La interfaz debe indicar claramente que se está trabajando en modo offline.
6. La aplicación debe manejar correctamente casos donde no hay datos locales disponibles.
7. La experiencia de usuario debe ser consistente entre los modos online y offline.

**HU-FE-040: Sincronización Automática de Datos Offline**

**Criterios de Aceptación:**
1. La aplicación debe detectar automáticamente cuando se restablece la conexión a internet.
2. Al detectar conexión, debe sincronizar los datos registrados offline según la configuración del usuario.
3. La sincronización debe ocurrir en segundo plano sin interrumpir la experiencia del usuario.
4. La aplicación debe implementar una estrategia de reintentos para manejar fallos temporales.
5. La sincronización debe respetar prioridades (ej. datos críticos primero).
6. El proceso debe ser eficiente en términos de uso de batería y datos.
7. La aplicación debe manejar correctamente interrupciones durante la sincronización.

**HU-FE-041: Indicador de Estado de Sincronización**

**Criterios de Aceptación:**
1. La aplicación debe mostrar un indicador claro del estado de sincronización (sincronizado, pendiente, error).
2. El indicador debe ser visible pero no intrusivo en la interfaz.
3. Para cada tipo de dato (asistencia, justificaciones, etc.), debe mostrarse su estado específico.
4. Al tocar el indicador, debe mostrarse información detallada sobre los elementos pendientes.
5. En caso de error, debe mostrarse información sobre la naturaleza del error y opciones para resolverlo.
6. El indicador debe actualizarse en tiempo real durante el proceso de sincronización.
7. Debe existir una opción para forzar la sincronización manual.

**HU-FE-042: Gestión de Conflictos de Datos**

**Criterios de Aceptación:**
1. La aplicación debe notificar al usuario cuando existan conflictos entre datos locales y del servidor.
2. Las notificaciones deben ser claras y explicar la naturaleza del conflicto.
3. Para conflictos que requieran intervención, la aplicación debe presentar opciones claras.
4. La interfaz debe permitir comparar las versiones en conflicto cuando sea posible.
5. Después de resolver un conflicto, la aplicación debe actualizar todos los datos relacionados.
6. La aplicación debe recordar las preferencias del usuario para conflictos similares.
7. Debe existir un registro de conflictos resueltos accesible desde la configuración.

**HU-FE-043: Recuperación de Sesión Interrumpida**

**Criterios de Aceptación:**
1. Si la aplicación se cierra inesperadamente, debe restaurar la sesión del usuario al reiniciar.
2. La aplicación debe recordar la última pantalla visitada y el estado de trabajo.
3. Los formularios parcialmente completados deben restaurarse con los datos ingresados.
4. La restauración debe ser rápida y no requerir intervención del usuario.
5. Si no es posible restaurar completamente, la aplicación debe explicar qué información se perdió.
6. La aplicación debe implementar guardado automático periódico para minimizar pérdida de datos.
7. El proceso de recuperación no debe comprometer la seguridad (ej. no restaurar datos sensibles en pantallas públicas).

## 🧠 Knowledge Base Service (kbservice) - Interfaz General

**HU-FE-KB-001: Acceso a Base de Conocimiento**

**Criterios de Aceptación:**
1. Debe existir una sección dedicada a la base de conocimiento accesible desde la navegación principal.
2. La sección debe ser accesible para todos los usuarios autenticados (Administrador, Instructor, Aprendiz).
3. La página principal debe mostrar categorías de conocimiento y artículos destacados.
4. El contenido mostrado debe adaptarse automáticamente según el rol del usuario.
5. La interfaz debe ser intuitiva y facilitar la exploración de contenido.
6. Durante la carga de datos, se debe mostrar un indicador de progreso.
7. En caso de error al cargar los datos, se debe mostrar un mensaje claro con opción de reintentar.

**HU-FE-KB-002: Búsqueda en Base de Conocimiento**

**Criterios de Aceptación:**
1. Debe existir un campo de búsqueda prominente en la sección de base de conocimiento.
2. La búsqueda debe activarse automáticamente después de una breve pausa en la escritura.
3. Durante la búsqueda, se debe mostrar un indicador de progreso.
4. Los resultados deben mostrarse en tiempo real a medida que el usuario escribe.
5. Si no hay resultados, se debe mostrar un mensaje claro y sugerencias alternativas.
6. La búsqueda debe incluir títulos, contenido y metadatos de los artículos.
7. El campo de búsqueda debe incluir un botón para limpiar el texto y reiniciar la búsqueda.

**HU-FE-KB-003: Visualización de Resultados de Búsqueda**

**Criterios de Aceptación:**
1. Los resultados de búsqueda deben mostrarse ordenados por relevancia.
2. Cada resultado debe mostrar título, breve extracto con las coincidencias destacadas, categoría y fecha de actualización.
3. Los resultados deben agruparse por tipo de contenido si es aplicable.
4. Debe existir una opción para ordenar los resultados por diferentes criterios (relevancia, fecha, etc.).
5. La lista de resultados debe ser paginada si hay muchos elementos.
6. Cada resultado debe ser clickeable para acceder al contenido completo.
7. La interfaz debe adaptarse a diferentes tamaños de pantalla, manteniendo la legibilidad.

**HU-FE-KB-004: Filtrado de Contenido por Categoría**

**Criterios de Aceptación:**
1. Debe existir un sistema de filtros para navegar por categorías de contenido.
2. Los filtros deben ser visibles y accesibles en la interfaz principal de la base de conocimiento.
3. Debe ser posible seleccionar múltiples categorías simultáneamente.
4. Al aplicar filtros, los resultados deben actualizarse inmediatamente.
5. Debe existir una opción para limpiar todos los filtros.
6. Las categorías deben organizarse jerárquicamente si es aplicable.
7. El sistema debe recordar los últimos filtros utilizados por el usuario.

**HU-FE-KB-005: Visualización de Artículo de Conocimiento**

**Criterios de Aceptación:**
1. Al seleccionar un artículo, debe mostrarse su contenido completo en una vista dedicada.
2. La vista debe incluir título, contenido formateado, categoría, fecha de creación y última actualización.
3. El contenido debe soportar formato enriquecido (negritas, listas, enlaces, imágenes).
4. Debe existir una opción para volver a los resultados de búsqueda o a la página principal.
5. La vista debe incluir opciones para compartir o guardar el artículo si es aplicable.
6. El contenido debe ser responsivo y legible en diferentes tamaños de pantalla.
7. Si el artículo es extenso, debe incluir un índice o navegación interna.

**HU-FE-KB-006: Navegación entre Artículos Relacionados**

**Criterios de Aceptación:**
1. Al final de cada artículo, deben mostrarse enlaces a artículos relacionados.
2. Los artículos relacionados deben determinarse por similitud temática, categoría o metadatos.
3. Cada enlace debe mostrar el título del artículo y una breve descripción.
4. Debe ser posible navegar directamente a cualquiera de estos artículos con un clic.
5. La sección de artículos relacionados debe ser visualmente distinta del contenido principal.
6. Si no hay artículos relacionados, esta sección debe ocultarse.
7. La selección de artículos relacionados debe adaptarse al rol del usuario.

## 🤖 Asistente Virtual Inteligente

**HU-FE-KB-007: Interfaz de Chat con Asistente**

**Criterios de Aceptación:**
1. Debe existir una interfaz de chat accesible desde cualquier parte de la aplicación.
2. La interfaz debe incluir un historial de mensajes y un campo para ingresar nuevas consultas.
3. Los mensajes del usuario y del asistente deben diferenciarse visualmente.
4. El asistente debe mostrar un indicador de "escribiendo" mientras procesa una consulta.
5. La interfaz debe soportar diferentes tipos de respuestas (texto, enlaces, imágenes, botones interactivos).
6. Debe ser posible desplazarse por el historial de la conversación actual.
7. La interfaz debe ser responsiva y adaptarse a diferentes tamaños de pantalla.

**HU-FE-KB-008: Historial de Conversaciones**

**Criterios de Aceptación:**
1. Debe existir una sección para ver el historial de conversaciones con el asistente.
2. Cada entrada debe mostrar la fecha, hora y un extracto de la primera consulta.
3. Debe ser posible buscar en el historial por texto o fecha.
4. Al seleccionar una conversación, debe cargarse completa en la interfaz de chat.
5. Debe existir una opción para eliminar conversaciones individuales.
6. El historial debe organizarse cronológicamente, con las conversaciones más recientes primero.
7. Debe implementarse paginación si hay muchas conversaciones.

**HU-FE-KB-009: Sugerencias de Consultas**

**Criterios de Aceptación:**
1. La interfaz de chat debe mostrar sugerencias de consultas frecuentes o relevantes.
2. Las sugerencias deben adaptarse al contexto actual y al historial del usuario.
3. Debe ser posible seleccionar una sugerencia con un clic para enviarla como consulta.
4. Las sugerencias deben actualizarse según el tema de la conversación actual.
5. Las sugerencias deben ser visualmente distintas pero no intrusivas.
6. Debe existir una opción para ocultar las sugerencias si el usuario lo prefiere.
7. Las sugerencias deben adaptarse al rol del usuario.

**HU-FE-KB-010: Feedback sobre Respuestas**

**Criterios de Aceptación:**
1. Cada respuesta del asistente debe incluir opciones para calificar su utilidad (ej. pulgar arriba/abajo).
2. Debe existir un campo opcional para proporcionar comentarios adicionales sobre la respuesta.
3. Al enviar feedback negativo, se debe solicitar información específica sobre el problema.
4. Después de enviar feedback, debe mostrarse un mensaje de agradecimiento.
5. El sistema debe registrar el feedback para mejorar futuras respuestas.
6. La interfaz de feedback debe ser discreta pero accesible.
7. Debe ser posible enviar feedback en cualquier momento, incluso para respuestas anteriores en la conversación.

## 📊 Resumen de Estado

### ✅ Funcionalidades Implementadas (10)

- ✅ **Autenticación básica**: login, logout, recuperación de contraseña
- ✅ **Navegación principal**: estructura de pestañas, pantalla de perfil
- ✅ **Tema adaptativo**: soporte para modo claro/oscuro
- ✅ **Pantalla de carga**: animación durante inicialización
- ✅ **Contexto de autenticación**: gestión centralizada de sesión
- ✅ **Cliente API autenticado**: manejo automático de tokens
- ✅ **Navegación basada en autenticación**: protección de rutas
- ✅ **Cambio forzado de contraseña**: flujo para primer inicio de sesión
- ✅ **Restablecimiento de contraseña**: procesamiento de tokens
- ✅ **Alertas de instructores sin lista**: panel administrativo

### 🚧 En Desarrollo (2)

- 🚧 **Funcionamiento sin conexión**: registro de asistencia offline
- 🚧 **Sincronización automática**: datos registrados offline

### 📋 Funcionalidades Pendientes (61)

- 📋 **Paneles principales**: implementación completa para todos los roles
- 📋 **Gestión de horarios**: visualización y administración
- 📋 **Control de asistencia**: registro y consulta
- 📋 **Funcionalidades administrativas**: gestión de usuarios y entidades
- 📋 **Funcionalidades de IA**: análisis predictivo y asistencia inteligente
- 📋 **Knowledge Base**: interfaz completa y asistente virtual
- 📋 **Sistema offline completo**: configuración, indicadores, manejo de conflictos
- 📋 **Recuperación de sesión**: restauración después de cierres inesperados

**Total de Historias:** 73  
**Progreso:** 14% implementado, 3% en desarrollo, 83% pendiente

## 📊 Evaluación de Instructores (EVALIN Service)

### Panel de Administración

**HU-FE-EVALIN-001: Gestión de Preguntas de Evaluación**

**Criterios de Aceptación:**
1. La interfaz debe proporcionar un formulario para crear nuevas preguntas con campos para: texto de la pregunta, tipo (selección única, múltiple, escala, texto libre), dimensión/categoría y opciones de respuesta (si aplica).
2. Para preguntas de tipo escala, se debe permitir definir el rango (mínimo, máximo) y etiquetas para los extremos.
3. La interfaz debe mostrar una lista paginada de preguntas existentes con opciones de filtrado por dimensión/categoría y búsqueda por texto.
4. Cada pregunta en la lista debe tener opciones para editar y eliminar, con confirmación antes de eliminar.
5. Al editar una pregunta, el formulario debe cargarse con los datos actuales y permitir modificarlos.
6. La interfaz debe mostrar mensajes de error específicos para cada campo cuando la validación falle.
7. La interfaz debe mostrar mensajes de éxito después de crear, actualizar o eliminar preguntas.

**HU-FE-EVALIN-002: Agrupar Preguntas en Cuestionarios**

**Criterios de Aceptación:**
1. La interfaz debe proporcionar un formulario para crear nuevos cuestionarios con campos para: título, descripción y estado (borrador, activo, inactivo).
2. La interfaz debe permitir buscar y seleccionar preguntas existentes para agregarlas al cuestionario.
3. Se debe permitir organizar las preguntas en secciones y establecer su orden mediante arrastrar y soltar.
4. La interfaz debe mostrar una vista previa del cuestionario tal como lo verán los aprendices.
5. Debe existir una lista paginada de cuestionarios existentes con opciones de filtrado por estado.
6. Cada cuestionario en la lista debe tener opciones para editar, duplicar y eliminar, con confirmación antes de eliminar.
7. La interfaz debe impedir eliminar cuestionarios que estén asociados a periodos de evaluación activos.

**HU-FE-EVALIN-003: Definir Periodos de Evaluación**

**Criterios de Aceptación:**
1. La interfaz debe proporcionar un formulario para crear nuevos periodos con campos para: título, fecha de inicio, fecha de fin, cuestionario a utilizar y fichas/programas aplicables.
2. El selector de fechas debe impedir seleccionar fechas incoherentes (fin anterior a inicio) y mostrar advertencias sobre solapamientos con otros periodos.
3. La interfaz debe permitir buscar y seleccionar múltiples fichas o programas a los que aplicará el periodo.
4. Debe existir una lista paginada de periodos existentes con opciones de filtrado por estado (activo, inactivo, futuro, pasado).
5. Cada periodo en la lista debe mostrar su estado actual, fechas, progreso de participación (si está activo) y opciones para editar, activar/desactivar y eliminar.
6. La interfaz debe impedir eliminar periodos que ya hayan iniciado.
7. Al activar un periodo, se debe mostrar una confirmación indicando que se enviarán notificaciones a los aprendices afectados.

**HU-FE-EVALIN-004: Consultar Reportes Consolidados de Evaluación**

**Criterios de Aceptación:**
1. La interfaz debe proporcionar filtros para seleccionar el alcance del reporte: instructor específico, programa o ficha.
2. Se deben mostrar gráficos y tablas con estadísticas consolidadas por dimensión/categoría.
3. Los gráficos deben incluir distribución de respuestas, promedios y comparativas con periodos anteriores cuando sea posible.
4. La interfaz debe permitir profundizar (drill-down) desde las dimensiones hasta las preguntas individuales.
5. Se debe proporcionar una opción para exportar los reportes en formatos comunes (PDF, Excel).
6. La interfaz debe aplicar las reglas de anonimización configuradas, mostrando advertencias cuando no hay suficientes respuestas.
7. Los reportes deben actualizarse en tiempo real o indicar claramente la última actualización de los datos.

**HU-FE-EVALIN-005: Configurar Parámetros del Módulo de Evaluación**

**Criterios de Aceptación:**
1. La interfaz debe proporcionar un formulario con todos los parámetros configurables del módulo EVALIN.
2. Los parámetros deben incluir: número mínimo de respuestas para mostrar resultados, habilitar/deshabilitar comentarios cualitativos, umbral de anonimización.
3. Cada parámetro debe tener una descripción clara de su propósito y efecto en el sistema.
4. La interfaz debe validar que los valores ingresados estén dentro de rangos aceptables.
5. Se debe mostrar una confirmación antes de guardar cambios que puedan afectar la privacidad o visualización de datos.
6. La interfaz debe mostrar los valores por defecto y permitir restablecer la configuración original.
7. Los cambios en la configuración deben aplicarse inmediatamente y mostrarse un mensaje de éxito al guardar.

**HU-FE-EVALIN-006: Dashboard de Seguimiento para Directores de Grupo**

**Criterios de Aceptación:**
1. El dashboard debe mostrar un resumen visual del estado de las evaluaciones para las fichas del director de grupo.
2. Se debe mostrar el porcentaje de participación global y por instructor para cada ficha.
3. La interfaz debe incluir una lista de aprendices que no han completado sus evaluaciones, con opciones para enviar recordatorios.
4. El dashboard debe actualizarse automáticamente o proporcionar un botón para refrescar los datos.
5. Se deben mostrar alertas para periodos próximos a vencer con baja participación.
6. La interfaz debe permitir filtrar por ficha y periodo de evaluación.
7. Se debe proporcionar acceso rápido a los reportes detallados de cada instructor evaluado en las fichas.

**HU-FE-EVALIN-007: Cargar Preguntas desde CSV**

**Criterios de Aceptación:**
1. La interfaz debe proporcionar un área para arrastrar y soltar o seleccionar un archivo CSV.
2. Se debe mostrar una plantilla descargable con el formato correcto y ejemplos.
3. Antes de procesar el archivo, la interfaz debe validar su estructura y mostrar errores si los encabezados no son correctos.
4. Durante el procesamiento, se debe mostrar un indicador de progreso.
5. Al finalizar, se debe mostrar un resumen del resultado: total de filas, filas procesadas exitosamente, filas con errores.
6. Para las filas con errores, se debe mostrar una tabla con el número de fila, campo problemático y descripción del error.
7. La interfaz debe proporcionar opciones para manejar duplicados: omitir, actualizar o crear nuevo.

### Interfaz para Aprendices

**HU-FE-EVALIN-008: Visualizar Instructores a Evaluar**

**Criterios de Aceptación:**
1. La interfaz debe mostrar una lista clara de instructores que el aprendiz puede evaluar, con sus fotos para fácil identificación.
2. Cada instructor debe mostrar información básica: nombre, ficha/programa asociado y periodo de evaluación aplicable.
3. Se debe indicar visualmente qué instructores ya han sido evaluados y cuáles están pendientes.
4. La interfaz debe mostrar la fecha límite para cada evaluación, destacando las próximas a vencer.
5. Al seleccionar un instructor, se debe navegar a la pantalla de cuestionario correspondiente.
6. Si no hay instructores para evaluar, se debe mostrar un mensaje informativo claro.
7. La lista debe actualizarse automáticamente cuando se completen evaluaciones, sin requerir recargar la página.

**HU-FE-EVALIN-009: Responder Cuestionario de Evaluación**

**Criterios de Aceptación:**
1. La interfaz debe mostrar el nombre y foto del instructor que se está evaluando en todo momento.
2. Las preguntas deben presentarse de forma clara, agrupadas por secciones si el cuestionario las define.
3. Para preguntas de selección única o múltiple, las opciones deben ser fácilmente seleccionables.
4. Para preguntas de escala, se debe mostrar una representación visual (estrellas, slider) con las etiquetas correspondientes.
5. La interfaz debe validar que todas las preguntas obligatorias tengan respuesta antes de permitir enviar.
6. Se debe mostrar el progreso actual (ej. "Pregunta 5 de 20") y permitir navegar entre secciones.
7. La interfaz debe guardar automáticamente las respuestas parciales para evitar pérdida de datos si el usuario abandona la página.

**HU-FE-EVALIN-010: Enviar Evaluación Completada**

**Criterios de Aceptación:**
1. El botón de envío debe estar claramente visible al final del cuestionario.
2. Antes de enviar, se debe mostrar un resumen de las respuestas para revisión final.
3. Se debe mostrar una confirmación solicitando al usuario que verifique sus respuestas antes del envío definitivo.
4. Durante el proceso de envío, se debe mostrar un indicador de progreso.
5. Al completar el envío exitosamente, se debe mostrar un mensaje de confirmación claro.
6. Después del envío, se debe redirigir al usuario a la lista de instructores a evaluar.
7. Si ocurre un error durante el envío, se debe mostrar un mensaje claro y ofrecer la opción de reintentar.

**HU-FE-EVALIN-011: Visualizar Resumen de Evaluaciones Enviadas**

**Criterios de Aceptación:**
1. La interfaz debe mostrar una lista de todas las evaluaciones completadas por el aprendiz.
2. Cada entrada debe incluir: instructor evaluado, fecha de envío, periodo de evaluación.
3. La interfaz debe permitir filtrar por periodo de evaluación.
4. Se debe mostrar un indicador de completitud general (ej. "Has completado 5 de 8 evaluaciones").
5. La interfaz no debe mostrar las respuestas específicas dadas, solo el estado de completitud.
6. Se debe proporcionar un enlace para volver a la lista de instructores pendientes de evaluar.
7. Si está habilitado en la configuración, se debe mostrar un certificado o constancia de participación.

### Interfaz para Instructores

**HU-FE-EVALIN-012: Visualizar Resultados Consolidados de Evaluaciones**

**Criterios de Aceptación:**
1. La interfaz debe mostrar los resultados consolidados solo cuando el administrador lo haya autorizado y haya suficientes respuestas para mantener el anonimato.
2. Se deben presentar gráficos y tablas con estadísticas por dimensión/categoría.
3. Los resultados deben incluir comparativas con promedios generales del programa/centro.
4. La interfaz debe permitir filtrar por periodo de evaluación para ver la evolución temporal.
5. Se deben destacar visualmente las fortalezas y áreas de mejora basadas en los puntajes.
6. La interfaz no debe mostrar información que pueda identificar a aprendices individuales.
7. Se debe proporcionar una opción para exportar un resumen de los resultados en formato PDF.

**HU-FE-EVALIN-013: Visualizar Comentarios Cualitativos Anonimizados**

**Criterios de Aceptación:**
1. La interfaz debe mostrar los comentarios cualitativos solo si están habilitados en la configuración y el administrador lo ha autorizado.
2. Los comentarios deben presentarse de forma completamente anonimizada, sin información que pueda identificar al aprendiz.
3. Se debe permitir filtrar comentarios por periodo de evaluación.
4. La interfaz debe agrupar comentarios por temas o sentimientos si es posible.
5. Se debe mostrar un aviso claro sobre la confidencialidad y propósito constructivo de los comentarios.
6. Si no hay suficientes comentarios para mantener el anonimato, se debe mostrar un mensaje explicativo.
7. La interfaz no debe permitir responder directamente a los comentarios para mantener el anonimato.

**HU-FE-EVALIN-014: Cargar Foto de Perfil**

**Criterios de Aceptación:**
1. La interfaz debe proporcionar una sección clara en el perfil del instructor para cargar o actualizar su foto.
2. Se debe permitir seleccionar una imagen desde el dispositivo o tomar una foto con la cámara en dispositivos móviles.
3. La interfaz debe mostrar una vista previa de la imagen antes de confirmar la carga.
4. Se deben validar el formato y tamaño de la imagen, mostrando errores específicos si no cumplen los requisitos.
5. Durante la carga, se debe mostrar un indicador de progreso.
6. Al completar la carga exitosamente, la nueva foto debe actualizarse inmediatamente en la interfaz.
7. Se debe proporcionar una opción para eliminar o restaurar la foto de perfil predeterminada.

### Notificaciones y Recordatorios

**HU-FE-EVALIN-015: Recibir Notificaciones de Periodos de Evaluación**

**Criterios de Aceptación:**
1. Las notificaciones de nuevos periodos de evaluación deben aparecer en el centro de notificaciones de la aplicación.
2. Las notificaciones deben incluir información clara: periodo, instructores a evaluar, fecha límite.
3. Al hacer clic en la notificación, se debe navegar directamente a la lista de instructores a evaluar.
4. Las notificaciones no leídas deben destacarse visualmente.
5. Se debe mostrar un contador de notificaciones no leídas en el ícono del centro de notificaciones.
6. Las notificaciones deben persistir hasta que el usuario las marque como leídas o complete todas las evaluaciones.
7. La interfaz debe permitir configurar preferencias de notificación (en app, email, ambas).

**HU-FE-EVALIN-016: Recibir Recordatorios de Evaluación**

**Criterios de Aceptación:**
1. Los recordatorios de evaluaciones pendientes deben aparecer en el centro de notificaciones con un indicador de urgencia.
2. Los recordatorios deben mostrar claramente los días restantes hasta el cierre del periodo.
3. Al hacer clic en el recordatorio, se debe navegar directamente a la lista de instructores pendientes de evaluar.
4. Para periodos próximos a vencer (menos de 3 días), se debe mostrar un banner persistente en la aplicación.
5. Los recordatorios deben tener una frecuencia razonable para no saturar al usuario.
6. La interfaz debe permitir descartar temporalmente un recordatorio ("recordarme más tarde").
7. Los recordatorios deben desaparecer automáticamente cuando se completen todas las evaluaciones del periodo.

**HU-FE-EVALIN-017: Enviar Recordatorios Manuales**

**Criterios de Aceptación:**
1. La interfaz para administradores y directores de grupo debe proporcionar una sección para enviar recordatorios manuales.
2. Se debe permitir seleccionar una ficha específica y filtrar por aprendices que no han completado sus evaluaciones.
3. La interfaz debe permitir seleccionar destinatarios individuales o enviar a todos los pendientes.
4. Se debe proporcionar un editor para personalizar el mensaje del recordatorio o seleccionar una plantilla predefinida.
5. Antes de enviar, se debe mostrar una confirmación con el número de destinatarios y vista previa del mensaje.
6. Después del envío, se debe mostrar un resumen: total enviados, exitosos, fallidos.
7. La interfaz debe impedir enviar recordatorios repetidos en un periodo corto (ej. máximo uno por día).
