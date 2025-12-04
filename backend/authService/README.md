# Documentación del API de Gestión de Usuarios y Permisos (AuthService)

Esta documentación detalla el funcionamiento, instalación y consumo de la API REST desarrollada con **FastAPI**. El sistema gestiona usuarios, autenticación mediante JWT, roles/permisos granulares y notificaciones por correo electrónico.

## 📋 Tabla de Contenidos

1.  Descripción General
2.  Stack Tecnológico
3.  Instalación y Despliegue
4.  Variables de Entorno
5.  Estructura de Base de Datos
6.  Autenticación y Seguridad
7.  Documentación de Endpoints

-----

##  Descripción General

Este microservicio se encarga de la centralización de la identidad de los usuarios. Permite el registro, inicio de sesión (Login), gestión de perfiles y administración de permisos dinámicos (ACL). Incluye un sistema de verificación de correo electrónico mediante integración con webhooks (n8n/Resend).

### Características Principales

  * **Autenticación JWT:** Emisión de tokens de acceso con expiración y payload personalizado.
  * **Seguridad:** Hashing de contraseñas utilizando Argon2.
  * **Gestión de Permisos:** Creación y asignación dinámica de permisos a usuarios.
  * **Base de Datos:** Persistencia en PostgreSQL con SQLAlchemy ORM.
  * **Contenerización:** Despliegue automatizado con Docker y Docker Compose.

-----

## Stack Tecnológico

  * **Lenguaje:** Python 3.11 
  * **Framework Web:** FastAPI
  * **Servidor ASGI:** Uvicorn
  * **Base de Datos:** PostgreSQL 15
  * **ORM:** SQLAlchemy
  * **Validación de Datos:** Pydantic
  * **Seguridad:** Python-Jose (JWT), Passlib (Argon2), OAuth2 Password Bearer
  * **Infraestructura:** Docker, Docker Compose

-----

##  Instalación y Despliegue

### Requisitos Previos

  * Docker y Docker Compose instalados.
  * Git.

### Despliegue con Docker 

El proyecto está configurado para ejecutarse en contenedores, orquestando la aplicación y la base de datos automáticamente.

1.  **Clonar el repositorio:**

    ```bash
    git clone <url-del-repositorio>
    cd <nombre-del-proyecto>
    ```

2.  **Configurar Variables de Entorno:**
    Cree un archivo `.env` en la raíz basándose en la sección o utilice los valores por defecto definidos en `docker-compose.yml`.

3.  **Construir y levantar servicios:**

    ```bash
    docker-compose up --build
    ```

      * La aplicación espera 10 segundos antes de iniciar para asegurar que la base de datos esté lista.
      * El servidor se iniciará en `http://0.0.0.0:8001` con recarga automática (reload) activada.

### Estructura de Archivos Docker

  * **Dockerfile:** Utiliza la imagen base `python:3.11-slim`. Instala dependencias del sistema (`gcc`, `libpq-dev`) necesarias para `psycopg2` y el entorno de Python.
  * **docker-compose.yml:** Define dos servicios:
      * `app`: La aplicación FastAPI (Puerto host: 8001).
      * `db`: Base de datos PostgreSQL 15 (Puerto host: 5442).
      * Define persistencia de datos mediante el volumen `postgres_data`.

-----

##  Variables de Entorno

Las siguientes variables son necesarias para la conexión a base de datos, seguridad y servicios externos.

| Variable | Descripción | Valor por Defecto (Docker) |
| :--- | :--- | :--- |
| `DB_HOST` | Host de la base de datos | `db` |
| `DB_PORT` | Puerto de conexión PostgreSQL | `5442` |
| `DB_NAME` | Nombre de la base de datos | `auth_db` |
| `DB_USER` | Usuario de PostgreSQL | `postgres` |
| `DB_PASS` | Contraseña de PostgreSQL | `password` |
| `JWT_SECRET` | Clave secreta para firmar tokens | `contrasena` |
| `SAL_ENCRYPT` | Sal para encriptación (si aplica) | `contrasena` |
| `RESEND_API_KEY` | API Key para servicio de emails | `re_...` |
| `RESEND_FROM_EMAIL` | Remitente de correos | `onboarding@resend.dev` |

> **Nota:** El archivo `.env` está excluido del control de versiones por seguridad.

-----

##  Estructura de Base de Datos

El sistema utiliza ORM para definir las tablas. Al iniciar la aplicación, se crean automáticamente las tablas y un set de permisos por defecto.

### Modelos Principales

1.  **Usuarios (`usuarios`)**:

      * `id_usuario`: UUID (PK).
      * `correo_usuario`: String (Unique).
      * `contraseña_usuario`: Hash Argon2.
      * `fecha_creacion`: DateTime.

2.  **Permisos (`permisos`)**:

      * `id_permiso`: UUID (PK).
      * `nombre_permiso`: String (Unique).

3.  **PermisosUsuario (`permisos_usuario`)**:

      * Tabla intermedia para relación Muchos-a-Muchos.
      * `id_permiso_usuario`: UUID (PK).
      * `id_usuario`: FK -\> usuarios.
      * `id_permiso`: FK -\> permisos.

### Permisos por Defecto

Al iniciar, el sistema asegura la existencia de los siguientes permisos (con UUIDs fijos):

  * `vista_productos`
  * `modificacion_productos`
  * `vista_stock`
  * `modificacion_stock`
  * `manejo_usuarios`

-----

##  Autenticación y Seguridad

  * **Esquema:** HTTP Bearer Token.
  * **Algoritmo:** HS256.
  * **Expiración:** 30 minutos.
  * **Validación de Contraseñas:**
      * Debe contener números y letras.
      * No puede ser solo numérica.
      * Mínimo 6 caracteres.

### Flujo de Autenticación

1.  El usuario envía credenciales a `/login`.
2.  Si son válidas, recibe un `access_token` que contiene en su payload:
      * `id_usuario`
      * `correo_usuario`
      * Lista de permisos (`permisos`) asignados.
3.  Para rutas protegidas, el token debe enviarse en el header: `Authorization: Bearer <token>`.

-----

##  Documentación de Endpoints

###  Estado del Sistema

  * **GET /**
      * Verifica si la API está activa.
      * **Respuesta:** `{"mensaje": "API de Gestión de Usuarios y Permisos", "estado": "activo"}`

###  Gestión de Usuarios

#### Crear Usuario

  * **POST** `/usuarios`
  * **Body:**
    ```json
    {
      "correo_usuario": "usuario@ejemplo.com",
      "contraseña_usuario": "passwordSegura1"
    }
    ```
  * **Descripción:** Registra un usuario. Valida formato de email y fortaleza de contraseña.

#### Obtener Usuarios

  * **GET** `/usuarios`
  * **Descripción:** Lista todos los usuarios registrados (sin contraseñas).

#### Obtener Usuario por ID

  * **GET** `/usuarios/{usuario_id}`
  * **Parámetros:** `usuario_id` (UUID).

#### Actualizar Usuario

  * **PUT** `/usuarios/{usuario_id}`
  * **Body:** `UsuarioCreate` (correo y contraseña).
  * **Descripción:** Actualiza credenciales. Verifica que el nuevo correo no exista.

#### Eliminar Usuario

  * **DELETE** `/usuarios/{usuario_id}`
  * **Descripción:** Elimina el usuario y sus relaciones de permisos en cascada.

-----

###  Autenticación y Perfil

#### Iniciar Sesión (Login)

  * **POST** `/login`
  * **Body:**
    ```json
    {
      "correo_usuario": "usuario@ejemplo.com",
      "contraseña_usuario": "password"
    }
    ```
  * **Respuesta:** Objeto `TokenResponse` incluyendo el JWT y el perfil completo del usuario con sus permisos.

#### Mi Perfil

  * **GET** `/mi-perfil`
  * **Headers:** `Authorization: Bearer <token>`
  * **Descripción:** Decodifica el token actual y retorna la información del usuario contenida en él, incluyendo sus permisos.

#### Enviar Código de Verificación

  * **POST** `/enviar-codigo-verificacion`
  * **Body:**
    ```json
    {
      "correo_usuario": "usuario@ejemplo.com",
      "codigo_verificacion": "123456"
    }
    ```
  * **Descripción:** Envía un correo asíncrono (Background Task) utilizando un webhook de n8n.

-----

### Gestión de Permisos

#### Crear Permiso

  * **POST** `/permisos`
  * **Body:** `{"nombre_permiso": "nuevo_permiso"}`

#### Listar Permisos

  * **GET** `/permisos`
  * **Descripción:** Retorna el catálogo completo de permisos disponibles.

#### Asignar Permiso a Usuario

  * **POST** `/permisos-usuario`
  * **Body:**
    ```json
    {
      "id_usuario": "uuid-usuario",
      "id_permiso": "uuid-permiso"
    }
    ```
  * **Descripción:** Vincula un permiso existente a un usuario. Falla si la relación ya existe.

#### Desvincular Permiso

  * **DELETE** `/permisos-usuario/`
  * **Query Params:** `id_usuario`, `id_permiso`
  * **Descripción:** Elimina la relación específica entre un usuario y un permiso.

#### Obtener Permisos de un Usuario

  * **GET** `/usuarios/{usuario_id}/permisos`
  * **Descripción:** Retorna la lista de permisos asignados a un usuario específico.
