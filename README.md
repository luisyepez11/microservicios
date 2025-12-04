# Sistema Distribuido Basado en Microservicios
## Nota
El proyecto actualmente está en fase de desarrollo , por lo cual no se subirán actualizaciones al main hasta que esté en una versión estable, todo el avance que tiene el proyecto actualmente está en la rama dev

## 🏗️ Descripción del Proyecto

Este proyecto implementa un sistema distribuido moderno compuesto por tres microservicios independientes, cada uno desarrollado con un framework y lenguaje diferente, integrados a través de un frontend desarrollado en Vue.js. El sistema demuestra conceptos avanzados de arquitectura de software distribuida, comunicación entre servicios y despliegue contenerizado.

## 🎯 Objetivo Principal

El propósito de este proyecto es diseñar, implementar y poner en funcionamiento un sistema distribuido que aplique los principios fundamentales de la arquitectura de microservicios, incluyendo:

- **Independencia tecnológica**: Cada servicio utiliza tecnologías diferentes
- **Despliegue independiente**: Contenedores separados para cada componente
- **Comunicación API-first**: Interacción mediante APIs REST bien definidas
- **Gestión centralizada de identidad**: Autenticación unificada con JWT
- **Frontend unificado**: Interfaz de usuario que consume múltiples servicios

## 📦 Componentes del Sistema

### 🔐 **Microservicio 1: Auth Service**
- **Tecnología**: Python + FastAPI
- **Responsabilidad**: Gestión centralizada de autenticación y autorización
- **Funcionalidades**:
  - Registro y autenticación de usuarios
  - Generación y validación de tokens JWT
  - Gestión de sesiones y permisos
  - Base de datos: PostgreSQL

### 🛒 **Microservicio 2: Products Service**
- **Tecnología**: PHP + Laravel/Slim
- **Responsabilidad**: Gestión del catálogo de productos
- **Funcionalidades**:
  - Operaciones CRUD completas de productos
  - Validación de datos y reglas de negocio
  - Integración con sistema de autenticación
  - Base de datos: MySQL/PostgreSQL

### 📊 **Microservicio 3: Inventory Service**
- **Tecnología**: Rust + Axum
- **Responsabilidad**: Control y gestión de inventario
- **Funcionalidades**:
  - Control de niveles de stock por producto
  - Operaciones de aumento/disminución de inventario
  - Consultas en tiempo real de disponibilidad
  - Base de datos: PostgreSQL

### 🎨 **Frontend: Vue.js Application**
- **Tecnología**: Vue.js 3 + Composition API
- **Responsabilidad**: Interfaz de usuario unificada
- **Funcionalidades**:
  - Dashboard administrativo
  - Gestión visual de productos e inventario
  - Formularios de autenticación
  - Consumo integrado de los tres microservicios

## 🏗️ Arquitectura del Sistema

### Principios Arquitectónicos
1. **Desacoplamiento**: Cada servicio es independiente y puede evolucionar por separado
2. **Escalabilidad horizontal**: Los servicios pueden escalar individualmente según demanda
3. **Resiliencia**: Fallos en un servicio no afectan el sistema completo
4. **Observabilidad**: Cada servicio expone métricas y logs para monitoreo

### Patrones Implementados
- **API Gateway Pattern** (implícito a través del frontend)
- **Token-based Authentication** con JWT
- **Database per Service**
- **Containerization** con Docker

## 🐳 Infraestructura y Despliegue

### Contenerización
Cada componente del sistema se ejecuta en contenedores Docker independientes, permitiendo:
- Despliegue consistente en cualquier entorno
- Aislamiento de dependencias
- Escalabilidad individual
- Orquestación con Docker Compose

### Comunicación entre Servicios
- **Protocolo**: HTTP/REST
- **Formato de datos**: JSON
- **Autenticación**: Tokens JWT en headers Authorization
- **CORS**: Configurado para permitir comunicación cross-origin

## 🛠️ Stack Tecnológico Completo

### Backend
- **Python** con FastAPI para el servicio de autenticación
- **PHP** con Laravel/Slim para el servicio de productos
- **Rust** con Axum para el servicio de inventario
- **PostgreSQL** y **MySQL** para persistencia de datos

### Frontend
- **Vue.js 3** con Composition API
- **Vue Router** para navegación
- **Pinia/Vuex** para gestión de estado
- **Axios** para comunicación HTTP
- **Tailwind CSS/Bootstrap** para estilos

### DevOps
- **Docker** para contenerización
- **Docker Compose** para orquestación
- **Git** para control de versiones
- **GitHub** para repositorio y CI/CD

## 🎓 Objetivos de Aprendizaje

Este proyecto permite a los estudiantes desarrollar habilidades en:

1. **Arquitectura de Microservicios**: Diseño e implementación de sistemas distribuidos
2. **Comunicación entre Servicios**: APIs REST, mensajería, gestión de errores
3. **Autenticación Distribuida**: Implementación de JWT en arquitectura distribuida
4. **Contenerización**: Uso de Docker para despliegue consistente
5. **Integración Frontend-Backend**: Consumo de múltiples APIs desde una SPA
6. **Trabajo en Equipo**: Colaboración en proyectos con múltiples tecnologías

## 👥 Organización del Equipo

El proyecto se desarrolla en equipos de 4-5 integrantes, distribuyendo responsabilidades:

- **Especialista Backend FastAPI**: Encargado del servicio de autenticación
- **Especialista Backend PHP**: Responsable del servicio de productos
- **Especialista Backend Rust**: Desarrollador del servicio de inventario
- **Especialista Frontend Vue.js**: Creador de la interfaz de usuario
- **Integrador/DevOps**: Coordinación, integración y despliegue


---

*Este proyecto representa una implementación práctica de arquitectura de microservicios, diseñada para demostrar competencias en desarrollo de sistemas distribuidos modernos.*
