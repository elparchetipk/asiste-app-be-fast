# Comparativa entre Microservicios y Self-Contained Systems (SCS)

**Actualizado: 1 de junio de 2025**

Este documento presenta una comparativa detallada entre dos enfoques arquitectónicos
modernos para el desarrollo de aplicaciones distribuidas: Microservicios y Self-Contained
Systems (SCS). El objetivo es proporcionar una visión clara de ambos enfoques, sus
similitudes, diferencias, ventajas, desventajas y casos de uso recomendados.

## 📋 Documentación de Referencia

Este documento debe leerse en conjunto con los siguientes documentos técnicos:

- **[Requisitos Funcionales](rf.md)**: Contexto y requisitos generales del sistema.
- **[Arquitectura y Tecnologías](rf.md#arquitectura-y-tecnologías)**: Descripción de la
  arquitectura actual del proyecto.

## 🔍 Introducción a los Conceptos

### Microservicios

Los microservicios son un enfoque arquitectónico y organizativo para el desarrollo de
software donde una aplicación se compone de pequeños servicios independientes que se
comunican a través de APIs bien definidas. Estos servicios son propiedad de equipos
pequeños y autónomos.

**Características definitorias:**

- Servicios pequeños y enfocados en una única funcionalidad o dominio de negocio
- Despliegue independiente
- Comunicación a través de APIs (generalmente HTTP/REST o mensajería)
- Bases de datos independientes (idealmente)
- Diferentes tecnologías posibles para cada servicio

### Self-Contained Systems (SCS)

Los Self-Contained Systems (SCS) son una arquitectura que se enfoca en la autonomía y la
independencia a nivel de sistema, no solo de servicio. Un SCS es una aplicación web
completa que incluye su propia interfaz de usuario, lógica de negocio y almacenamiento de
datos.

**Características definitorias:**

- Sistemas web completos y autónomos (frontend + backend + datos)
- Mínima dependencia entre sistemas
- Cada SCS pertenece a un único equipo
- Comunicación asíncrona preferida entre sistemas
- Experiencia de usuario integrada a través de enlaces, integración de UI o API Gateway

## 🔄 Comparación Directa

### Granularidad y Alcance

**Microservicios:**

- Granularidad fina, enfocados en una única capacidad de negocio
- Típicamente solo incluyen backend (sin UI)
- Pueden requerir decenas o cientos de servicios para una aplicación completa

**SCS:**

- Granularidad gruesa, enfocados en un área funcional completa
- Incluyen UI, lógica de negocio y datos
- Generalmente se necesitan menos sistemas (5-25) para una aplicación empresarial

### Autonomía y Acoplamiento

**Microservicios:**

- Autonomía a nivel de servicio
- Pueden tener dependencias en tiempo de ejecución entre servicios
- Requieren orquestación para funcionalidades completas

**SCS:**

- Autonomía a nivel de sistema completo
- Diseñados para minimizar dependencias en tiempo de ejecución
- Cada sistema puede funcionar independientemente

### Modelo de Datos

**Microservicios:**

- Base de datos por servicio (idealmente)
- Posible duplicación de datos entre servicios
- Consistencia eventual entre servicios

**SCS:**

- Base de datos por sistema
- Datos duplicados entre sistemas cuando es necesario
- Consistencia eventual entre sistemas, pero consistencia fuerte dentro del sistema

### Integración y Comunicación

**Microservicios:**

- Comunicación síncrona común (REST, gRPC)
- Comunicación asíncrona para desacoplamiento (eventos, colas)
- API Gateway para clientes externos

**SCS:**

- Preferencia por comunicación asíncrona entre sistemas
- Integración a nivel de UI (enlaces, composición de UI)
- API para integraciones cuando es necesario

### Despliegue y Operaciones

**Microservicios:**

- Despliegue independiente por servicio
- Contenedores y orquestación (Docker, Kubernetes)
- Monitoreo y trazabilidad complejos

**SCS:**

- Despliegue independiente por sistema
- Puede usar contenedores o despliegue tradicional
- Monitoreo más simple por sistema

## 📊 Ventajas y Desventajas

### Microservicios

**Ventajas:**

1. **Escalabilidad precisa**: Escalar solo los servicios que lo necesitan
2. **Flexibilidad tecnológica**: Cada servicio puede usar la tecnología más adecuada
3. **Despliegue independiente**: Actualizaciones más rápidas y de menor riesgo
4. **Equipos autónomos**: Desarrollo paralelo y mayor velocidad
5. **Resistencia a fallos**: El fallo de un servicio no afecta a toda la aplicación

**Desventajas:**

1. **Complejidad operativa**: Gestionar decenas o cientos de servicios
2. **Sobrecarga de red**: Latencia por comunicación entre servicios
3. **Consistencia de datos**: Desafíos con transacciones distribuidas
4. **Curva de aprendizaje**: Requiere nuevas habilidades y herramientas
5. **Costos de infraestructura**: Mayor consumo de recursos

### Self-Contained Systems (SCS)

**Ventajas:**

1. **Autonomía completa**: Sistemas verdaderamente independientes
2. **Menor complejidad operativa**: Menos sistemas para gestionar
3. **Mejor encapsulación**: Cambios localizados dentro de un sistema
4. **Transición más suave**: Más cercano a arquitecturas monolíticas tradicionales
5. **Equipos con responsabilidad end-to-end**: Frontend, backend y datos

**Desventajas:**

1. **Posible duplicación de código**: Funcionalidades comunes repetidas
2. **Experiencia de usuario fragmentada**: Desafíos en la integración de UI
3. **Granularidad más gruesa**: Menos flexibilidad para escalar componentes específicos
4. **Menos adopción en la industria**: Menos herramientas y prácticas establecidas
5. **Posible silos de conocimiento**: Equipos aislados en sus sistemas

## 🎯 Casos de Uso Recomendados

### Microservicios

Los microservicios son más adecuados para:

1. **Aplicaciones complejas a gran escala**: Sistemas con muchas funcionalidades distintas
2. **Equipos grandes y distribuidos**: Organizaciones con múltiples equipos de desarrollo
3. **Requisitos de escalabilidad variables**: Componentes con diferentes necesidades de
   recursos
4. **Evolución rápida**: Sistemas que requieren actualizaciones frecuentes y ágiles
5. **Experimentación tecnológica**: Cuando se necesita probar diferentes tecnologías

**Ejemplos de empresas**: Netflix, Amazon, Uber, Spotify

### Self-Contained Systems (SCS)

Los SCS son más adecuados para:

1. **Organizaciones en transición**: Migrando de monolitos a arquitecturas distribuidas
2. **Dominios de negocio claramente separados**: Funcionalidades con poca interdependencia
3. **Equipos multidisciplinarios**: Grupos que manejan frontend, backend y datos
4. **Sistemas empresariales complejos**: Aplicaciones con lógica de negocio compleja
5. **Prioridad en la autonomía de equipos**: Minimizar la coordinación entre equipos

**Ejemplos de empresas**: Otto Group (comercio electrónico alemán), empresas financieras y
de seguros

## 🔄 Comparación con Arquitecturas Tradicionales

### Microservicios vs. Monolito

| Aspecto       | Monolito                                    | Microservicios                                |
|---------------|---------------------------------------------|-----------------------------------------------|
| Despliegue    | Único despliegue                            | Múltiples despliegues independientes          |
| Escalabilidad | Escala como una unidad                      | Escalabilidad selectiva                       |
| Tecnología    | Homogénea                                   | Heterogénea                                   |
| Desarrollo    | Simple inicialmente, complejo a largo plazo | Complejo inicialmente, flexible a largo plazo |
| Rendimiento   | Menor latencia interna                      | Mayor latencia por comunicación en red        |

### SCS vs. Monolito

| Aspecto     | Monolito                     | SCS                                    |
|-------------|------------------------------|----------------------------------------|
| Despliegue  | Único despliegue             | Múltiples despliegues independientes   |
| Autonomía   | Baja                         | Alta                                   |
| Tecnología  | Homogénea                    | Potencialmente heterogénea por sistema |
| Integración | Interna (llamadas a métodos) | Externa (API, UI, enlaces)             |
| Evolución   | Difícil a largo plazo        | Más sostenible a largo plazo           |

### Microservicios vs. SCS

| Aspecto      | Microservicios          | SCS                         |
|--------------|-------------------------|-----------------------------|
| Granularidad | Fina (servicios)        | Gruesa (sistemas)           |
| Alcance      | Backend                 | Frontend + Backend + Datos  |
| Comunicación | Principalmente API      | API + Integración UI        |
| Complejidad  | Alta (muchos servicios) | Media (menos sistemas)      |
| Autonomía    | A nivel de servicio     | A nivel de sistema completo |

## 🚀 Implementación y Migración

### Consideraciones para Microservicios

1. **Infraestructura Cloud-Native**: Kubernetes, orquestación, service mesh
2. **Patrones de Resiliencia**: Circuit breaker, bulkhead, retry
3. **Observabilidad**: Logging centralizado, tracing distribuido, métricas
4. **API Gateway**: Enrutamiento, autenticación, rate limiting
5. **Estrategia de Migración**: Strangler pattern, descomposición por dominio

### Consideraciones para SCS

1. **Definición de Límites**: Identificar dominios de negocio autónomos
2. **Estrategia de Integración UI**: iFrames, Web Components, enlaces
3. **Comunicación Asíncrona**: Eventos, mensajería, feeds de datos
4. **Autenticación Centralizada**: SSO, tokens compartidos
5. **Estrategia de Migración**: Vertical slicing, migración por dominio

## 📝 Conclusiones

Tanto los microservicios como los Self-Contained Systems (SCS) representan enfoques
modernos para desarrollar aplicaciones distribuidas, cada uno con sus propias fortalezas y
debilidades:

- **Microservicios** ofrecen mayor granularidad, flexibilidad tecnológica y escalabilidad
  precisa, pero con mayor complejidad operativa y de integración.

- **SCS** proporcionan mayor autonomía, menor complejidad operativa y mejor encapsulación,
  pero pueden resultar en duplicación y desafíos en la experiencia de usuario unificada.

La elección entre estos enfoques debe basarse en:

1. **Tamaño y estructura de la organización**: Equipos, comunicación, cultura
2. **Complejidad del dominio**: Subdominios, interrelaciones, reglas de negocio
3. **Requisitos no funcionales**: Escalabilidad, disponibilidad, rendimiento
4. **Madurez tecnológica**: Herramientas, habilidades, experiencia
5. **Estrategia de evolución**: Velocidad de cambio, experimentación, crecimiento

En muchos casos, un enfoque híbrido puede ser beneficioso, utilizando SCS para la división
inicial de un monolito y luego refinando con microservicios dentro de cada SCS según sea
necesario.

Para el proyecto Asiste App, que ya utiliza una arquitectura de microservicios, la
incorporación de principios de SCS podría considerarse para áreas funcionales completas
como el módulo de evaluación de instructores (evalin) o el knowledge base (kbservice),
asegurando que estos sistemas mantengan una alta cohesión y baja dependencia con el resto
de la aplicación.