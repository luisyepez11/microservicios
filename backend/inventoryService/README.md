# Documentación del API de Gestión de Stock

Esta documentación detalla el funcionamiento, instalación y consumo de la API REST desarrollada con **Axum (Rust)**. El sistema gestiona el stock de productos mediante operaciones CRUD con persistencia en PostgreSQL.

## 📋 Tabla de Contenidos

1. Descripción General
2. Stack Tecnológico
3. Instalación y Despliegue
4. Configuración
5. Estructura de Base de Datos
6. Autenticación y Seguridad
7. Documentación de Endpoints

-----

## Descripción General

Este microservicio proporciona una API RESTful para gestionar el inventario de productos. Permite realizar operaciones CRUD (Crear, Leer, Actualizar) sobre registros de stock, con persistencia en PostgreSQL y manejo de transacciones robustas.

### Características Principales

* **API RESTful:** Endpoints bien definidos siguiendo convenciones REST
* **Base de Datos:** Persistencia en PostgreSQL con SQLx ORM
* **UUIDs:** Identificadores únicos universales para todos los registros
* **CORS Configurado:** Permite peticiones desde diferentes orígenes
* **Servidor Estático:** Sirve archivos estáticos desde el directorio raíz
* **Manejo de Errores:** Respuestas HTTP apropiadas con mensajes descriptivos

-----

## Stack Tecnológico

* **Lenguaje:** Rust 1.70+
* **Framework Web:** Axum
* **Runtime Asíncrono:** Tokio
* **Base de Datos:** PostgreSQL 15
* **ORM y Migraciones:** SQLx
* **Serialización:** Serde (JSON)
* **Identificadores Únicos:** UUID v4
* **Middleware HTTP:** Tower HTTP (CORS, servicios estáticos)
* **Infraestructura:** Docker, Docker Compose (opcional)

-----

## Instalación y Despliegue

### Requisitos Previos

* Rust y Cargo instalados (mínimo versión 1.70)
* PostgreSQL 15+ instalado y ejecutándose
* Opcional: Docker y Docker Compose para despliegue contenerizado

### Método 1: Ejecución Local

1. **Clonar el repositorio:**
```bash
git clone <url-del-repositorio>
cd stock-api
```

2. **Configurar base de datos:**
```bash
# Conectar a PostgreSQL
psql -U postgres -c "CREATE DATABASE stock_api;"
psql -U postgres -d stock_api -c "
CREATE TABLE stock (
    id_stock UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_producto UUID NOT NULL,
    cantidad INTEGER NOT NULL
);"
```

3. **Configurar variables de conexión:**
Editar el archivo `src/main.rs` línea 16 con tus credenciales de PostgreSQL:
```rust
let database_url = "postgres://usuario:contraseña@localhost:5432/stock_api";
```

4. **Compilar y ejecutar:**
```bash
cargo build --release
cargo run --release
```

### Método 2: Despliegue con Docker

El proyecto incluye configuración para ejecutarse en contenedores:

1. **Configurar docker-compose.yml:**
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgres://postgres:prueba123@db:5432/stock_api
  
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: prueba123
      POSTGRES_DB: stock_api
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

2. **Construir y levantar servicios:**
```bash
docker-compose up --build
```

3. **Crear tabla en la base de datos:**
```bash
docker-compose exec db psql -U postgres -d stock_api -c "
CREATE TABLE stock (
    id_stock UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_producto UUID NOT NULL,
    cantidad INTEGER NOT NULL
);"
```

### Estructura de Archivos

```
stock-api/
├── src/
│   └── main.rs          # Código principal de la aplicación
├── Cargo.toml           # Dependencias y metadatos de Rust
├── Cargo.lock           # Versiones bloqueadas de dependencias
├── docker-compose.yml   # Orquestación de contenedores (opcional)
├── Dockerfile          # Imagen Docker de la aplicación (opcional)
└── static/             # Archivos estáticos (HTML, CSS, JS)
```

-----

## Configuración

### Variables de Configuración

Las siguientes configuraciones están codificadas en el archivo `src/main.rs`:

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| Puerto API | 8000 | Puerto donde escucha el servidor |
| Host API | 0.0.0.0 | Dirección de escucha (todas las interfaces) |
| Máx. conexiones DB | 5 | Conexiones máximas al pool de PostgreSQL |
| Timeout conexión DB | 3 segundos | Tiempo máximo para establecer conexión |
| CORS | Permitido cualquier origen | Configuración para desarrollo |

### Configuración de Base de Datos

La cadena de conexión sigue el formato:
```
postgres://usuario:contraseña@host:puerto/nombre_base_datos
```

Ejemplo:
```rust
let database_url = "postgres://postgres:prueba123@localhost:5432/stock_api";
```

-----

## Estructura de Base de Datos

### Tabla Principal: `stock`

```sql
CREATE TABLE stock (
    id_stock UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    id_producto UUID NOT NULL,
    cantidad INTEGER NOT NULL
);
```

### Modelo de Datos en Rust

```rust
#[derive(Debug, Deserialize, Serialize, FromRow)]
pub struct Stock {
    pub id_stock: Option<Uuid>,      // UUID auto-generado por PostgreSQL
    pub id_producto: Uuid,           // ID del producto relacionado
    pub cantidad: i32,               // Cantidad disponible en inventario
}
```

### Relaciones

* `id_producto` es un UUID que referencia un producto en otro sistema/microservicio
* Cada registro representa el stock disponible de un producto específico
* No hay restricciones de unicidad en `id_producto` (puede haber múltiples registros por producto)

-----

## Autenticación y Seguridad

### Configuración CORS

La API incluye middleware CORS configurado para desarrollo:
* **Orígenes permitidos:** Cualquier origen (`*`)
* **Métodos permitidos:** Todos los métodos HTTP
* **Headers permitidos:** Todos los headers
* **Credenciales:** No permitidas por defecto

**Nota:** Para entornos de producción, se recomienda restringir los orígenes permitidos.

### Validación de Datos

* **UUIDs:** Validación estricta de formatos UUID v4
* **Tipos de datos:** Conversión y validación automática de tipos (i32 para cantidades)
* **Respuestas HTTP:** Códigos de estado apropiados según el resultado de la operación

### Consideraciones de Seguridad

1. **Exponer solo puertos necesarios:** Solo el puerto 8000 está expuesto
2. **Validación de inputs:** Todos los parámetros son validados antes de procesar
3. **Manejo de errores:** No se exponen detalles internos en respuestas de error
4. **Pool de conexiones:** Limitado a 5 conexiones concurrentes

-----

## Documentación de Endpoints

### Estado del Sistema

#### Verificar Estado del Sistema
* **GET** `/`
* **Descripción:** Sirve archivos estáticos desde el directorio `./`
* **Respuesta:** Archivo HTML estático o listado de directorio

#### Verificar Conexión a Base de Datos
* **GET** `/db-check`
* **Descripción:** Realiza un ping a la base de datos para verificar conectividad
* **Respuesta Exitosa (200):** `Base de datos conectada. Ping: 1`
* **Respuesta de Error:** Mensaje de error específico

-----

### Gestión de Stock

#### Obtener Todos los Registros de Stock
* **GET** `/api`
* **Descripción:** Retorna todos los registros de stock en la base de datos
* **Respuesta Exitosa (200):**
```json
[
    {
        "id_stock": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "id_producto": "b2c3d4e5-f6g7-8901-bcde-fg2345678901",
        "cantidad": 100
    },
    {
        "id_stock": "c3d4e5f6-g7h8-9012-cdef-gh3456789012",
        "id_producto": "d4e5f6g7-h8i9-0123-defg-hi4567890123",
        "cantidad": 50
    }
]
```
* **Posibles Errores:**
  * `500`: Error interno del servidor

#### Obtener Stock por ID de Producto
* **GET** `/api/{id_producto}`
* **Parámetros de Ruta:**
  * `id_producto` (UUID): ID único del producto
* **Descripción:** Retorna el registro de stock para un producto específico
* **Respuesta Exitosa (200):**
```json
{
    "id_stock": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "id_producto": "b2c3d4e5-f6g7-8901-bcde-fg2345678901",
    "cantidad": 100
}
```
* **Posibles Errores:**
  * `400`: ID de producto inválido (formato UUID incorrecto)
  * `404`: Producto no encontrado en la base de datos
  * `500`: Error interno del servidor

#### Crear Nuevo Registro de Stock
* **POST** `/api`
* **Headers:**
  * `Content-Type: application/json`
* **Body:**
```json
{
    "id_producto": "b2c3d4e5-f6g7-8901-bcde-fg2345678901",
    "cantidad": 75
}
```
* **Descripción:** Crea un nuevo registro de stock en la base de datos
* **Respuesta Exitosa (201):** `Stock creado exitosamente`
* **Respuesta de Error:**
  * `400`: Datos inválidos en el body
  * `500`: Error interno del servidor

#### Actualizar Cantidad de Stock
* **PUT** `/api`
* **Headers:**
  * `Content-Type: application/json`
* **Body:**
```json
{
    "id_producto": "b2c3d4e5-f6g7-8901-bcde-fg2345678901",
    "cantidad": 125
}
```
* **Descripción:** Actualiza la cantidad de stock para un producto existente
* **Nota:** Este endpoint realiza una actualización completa (PUT), no incremental
* **Respuesta Exitosa (201):** `Stock modificado exitosamente`
* **Posibles Errores:**
  * `400`: Datos inválidos en el body
  * `404`: Producto no encontrado (si no existe, no se crea automáticamente)
  * `500`: Error interno del servidor

-----

### Ejemplos de Uso con cURL

#### Obtener todo el stock:
```bash
curl -X GET http://localhost:8000/api
```

#### Obtener stock específico:
```bash
curl -X GET http://localhost:8000/api/b2c3d4e5-f6g7-8901-bcde-fg2345678901
```

#### Crear nuevo stock:
```bash
curl -X POST http://localhost:8000/api \
  -H "Content-Type: application/json" \
  -d '{"id_producto": "b2c3d4e5-f6g7-8901-bcde-fg2345678901", "cantidad": 50}'
```

#### Actualizar stock:
```bash
curl -X PUT http://localhost:8000/api \
  -H "Content-Type: application/json" \
  -d '{"id_producto": "b2c3d4e5-f6g7-8901-bcde-fg2345678901", "cantidad": 75}'
```

#### Verificar conexión a DB:
```bash
curl -X GET http://localhost:8000/db-check
```

-----

### Códigos de Estado HTTP

| Código | Significado | Casos de Uso |
|--------|-------------|--------------|
| 200 | OK | Operaciones GET exitosas |
| 201 | Creado | Operaciones POST/PUT exitosas |
| 400 | Bad Request | Datos inválidos, UUID mal formado |
| 404 | Not Found | Recurso no encontrado |
| 500 | Internal Server Error | Error en base de datos o servidor |

### Notas Adicionales

1. **UUIDs:** Todos los IDs deben estar en formato UUID estándar (8-4-4-4-12 caracteres hexadecimales)
2. **Cantidades:** Valores enteros (positivos o negativos según necesidad de inventario)
3. **Persistencia:** Los cambios se reflejan inmediatamente en la base de datos
4. **Concurrencia:** El pool de conexiones maneja múltiples peticiones concurrentes
5. **Rendimiento:** La aplicación está construida en Rust con Axum para alto rendimiento

### Próximas Mejoras (Roadmap)

1. Implementar autenticación JWT
2. Agregar endpoint para actualización incremental de stock (PATCH)
3. Implementar filtros y paginación en GET /api
4. Agregar logging estructurado
5. Implementar métricas y health checks
6. Agregar documentación Swagger/OpenAPI
7. Implementar pruebas unitarias y de integración
8. Agregar migraciones de base de datos con SQLx migrate
