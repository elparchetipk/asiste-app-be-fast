# Guía de Implementación de Clean Architecture

**Fecha:** 7 de junio de 2025  
**Versión:** 1.0  
**Desarrollado por:** Equipo de Backend FastAPI

## 📋 Índice

1. [Introducción](#introducción)
2. [Principios Fundamentales](#principios-fundamentales)
3. [Estructura de Capas](#estructura-de-capas)
4. [Guía de Implementación Paso a Paso](#guía-de-implementación-paso-a-paso)
5. [Estructura de Carpetas Propuesta](#estructura-de-carpetas-propuesta)
6. [Ejemplos de Implementación](#ejemplos-de-implementación)
7. [Plan de Migración](#plan-de-migración)
8. [Testing Strategy](#testing-strategy)
9. [Mejores Prácticas](#mejores-prácticas)
10. [Referencias](#referencias)

---

## Introducción

### ¿Qué es Clean Architecture?

Clean Architecture es un patrón arquitectónico propuesto por Robert C. Martin (Uncle Bob) que organiza el código en capas concéntricas, donde las dependencias apuntan hacia el centro (dominio) y nunca hacia afuera.

### ¿Por qué implementar Clean Architecture?

- **Independencia de Frameworks**: El core business no depende de FastAPI, SQLAlchemy, etc.
- **Testabilidad**: Facilita testing unitario mediante inversión de dependencias
- **Independencia de Base de Datos**: Se puede cambiar PostgreSQL por MongoDB sin afectar la lógica de negocio
- **Independencia de UI**: El dominio no conoce si se accede por REST, GraphQL o CLI
- **Mantenibilidad**: Código más limpio, organizado y fácil de modificar
- **Escalabilidad**: Facilita agregar nuevas funcionalidades sin afectar las existentes

### Objetivos del Proyecto

1. **Migrar gradualmente** todos los microservicios hacia Clean Architecture
2. **Mantener funcionalidad** existente durante la migración
3. **Mejorar testabilidad** con cobertura del 90%
4. **Estandarizar estructura** entre microservicios
5. **Documentar proceso** para futuros desarrolladores

---

## Principios Fundamentales

### 1. Dependency Inversion Principle (DIP)

- Las capas internas no deben depender de las externas
- Se usan interfaces/puertos para invertir dependencias
- La implementación se inyecta desde afuera

### 2. Single Responsibility Principle (SRP)

- Cada clase/módulo tiene una sola razón para cambiar
- Separación clara de responsabilidades

### 3. Open/Closed Principle (OCP)

- Abierto para extensión, cerrado para modificación
- Nuevas funcionalidades sin modificar código existente

### 4. Interface Segregation Principle (ISP)

- Interfaces específicas y cohesivas
- No forzar dependencias innecesarias

---

## Estructura de Capas

### 1. Domain Layer (Centro - más estable)

**Responsabilidades:**

- Entidades de negocio
- Objetos de valor
- Reglas de negocio
- Excepciones de dominio
- Interfaces de repositorios (puertos)

**No depende de:**

- Frameworks específicos
- Base de datos
- APIs externas
- Capas superiores

### 2. Application Layer (Casos de Uso)

**Responsabilidades:**

- Orquestación de entidades de dominio
- Casos de uso específicos
- DTOs (Data Transfer Objects)
- Interfaces de servicios externos

**Depende de:**

- Domain Layer únicamente

### 3. Infrastructure Layer (Adapters - más volátil)

**Responsabilidades:**

- Implementación de repositorios
- Modelos de base de datos
- Clientes de APIs externas
- Configuraciones
- Mappers entre capas

**Depende de:**

- Domain Layer (a través de interfaces)
- Application Layer

### 4. Presentation Layer (Web/API)

**Responsabilidades:**

- Controladores/Routers
- Validación de entrada HTTP
- Serialización de respuestas
- Manejo de errores HTTP

**Depende de:**

- Application Layer

---

## Estructura de Carpetas Propuesta

```bash
microservice/
├── app/
│   ├── domain/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   ├── repositories/
│   │   └── exceptions/
│   ├── application/
│   │   ├── use_cases/
│   │   ├── dtos/
│   │   └── interfaces/
│   ├── infrastructure/
│   │   ├── repositories/
│   │   ├── models/
│   │   ├── adapters/
│   │   └── config/
│   └── presentation/
│       ├── routers/
│       ├── schemas/
│       └── dependencies/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── requirements.txt
```

---

## Plan de Migración

### Priorización de Microservicios

1. **userservice** (Primera prioridad - más maduro)
2. **scheduleservice** (Segunda prioridad - en desarrollo)
3. **attendanceservice** (Tercera prioridad - básico)
4. **evalinservice** (Cuarta prioridad - específico)
5. **aiservice** (Quinta prioridad - experimental)
6. **kbservice** (Sexta prioridad - experimental)

### Cronograma Sugerido

| Semana | Microservicio     | Actividades                                     |
| ------ | ----------------- | ----------------------------------------------- |
| 1-2    | userservice       | Análisis estructura actual, diseño domain layer |
| 3-4    | userservice       | Implementación domain + application layers      |
| 5-6    | userservice       | Migración infrastructure + testing              |
| 7-8    | scheduleservice   | Aplicación lecciones aprendidas                 |
| 9-10   | attendanceservice | Implementación con nueva estructura             |
| 11-12  | evalinservice     | Refactoring hacia Clean Architecture            |
| 13-14  | aiservice         | Diseño específico para ML/AI workflows          |
| 15-16  | kbservice         | Implementación con optimizaciones específicas   |

### Estrategia de Migración: Strangler Fig Pattern (Recomendado)

- Migrar endpoint por endpoint
- Mantener ambas versiones funcionando
- Gradualmente reemplazar implementación antigua
- Zero downtime, menor riesgo

---

## Testing Strategy

### Pirámide de Testing

```
       /\
      /  \
     / E2E\     <- Pocos, lentos, costosos
    /______\
   /        \
  /Integration\ <- Algunos, medios
 /____________\
/              \
/ Unit Tests   \   <- Muchos, rápidos, baratos
/________________\
```

### Objetivos de Testing

- **90% cobertura** en tests unitarios
- **100% cobertura** en casos de uso críticos
- **Tests de integración** para todos los endpoints
- **Tests E2E** para flujos completos del usuario

---

## Mejores Prácticas

### 1. Nomenclatura

- **Entidades**: PascalCase (`User`, `Schedule`, `Attendance`)
- **Value Objects**: Descriptivos (`Email`, `PhoneNumber`, `UserRole`)
- **Casos de Uso**: Verbos de acción (`CreateUserUseCase`, `UpdateUserProfileUseCase`)
- **Repositorios**: Interfaces (`UserRepository`) e implementaciones (`SQLAlchemyUserRepository`)

### 2. Manejo de Errores

- Excepciones específicas de dominio
- Propagación correcta entre capas
- Logging estructurado por capa

### 3. Performance

- Lazy loading en entidades
- Connection pooling optimizado
- Caching estratégico

---

## Referencias

### Documentación Relacionada

- [Historias de Usuario Backend](../stories/be/historias_usuario_be.md)
- [Criterios de Aceptación](../stories/be/criterios_aceptacion_be.md)
- [Requisitos Funcionales](../general/rf.md)

### Recursos Externos

- "Clean Architecture" - Robert C. Martin
- "Implementing Domain-Driven Design" - Vaughn Vernon
- [The Clean Architecture - Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

**Nota:** Esta guía está diseñada específicamente para el proyecto Asiste App Backend y debe adaptarse según las necesidades específicas de cada microservicio. La migración debe realizarse gradualmente para minimizar riesgos y mantener la funcionalidad operativa.
