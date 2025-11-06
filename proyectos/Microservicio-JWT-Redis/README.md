# Microservicio JWT con Redis

Este proyecto es un microservicio de autenticación basado en JSON Web Tokens (JWT) desarrollado con Flask y Python. Proporciona una API REST completa para gestionar la autenticación de usuarios, incluyendo registro, login, refresh de tokens, logout y acceso a recursos protegidos. Utiliza Redis como sistema de almacenamiento temporal para tokens JWT y MariaDB para datos persistentes de usuarios, con dockerización completa para facilitar el despliegue.

## Tecnologías Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)
![Adminer](https://img.shields.io/badge/Adminer-FF6600?style=for-the-badge&logo=adminer&logoColor=white)
![PyJWT](https://img.shields.io/badge/PyJWT-000000?style=for-the-badge&logo=python&logoColor=white)

## Características

- ✅ Registro de usuarios con validación
- ✅ Autenticación segura con JWT
- ✅ Sistema de refresh tokens
- ✅ Revocación inmediata de tokens en logout
- ✅ Endpoint protegido para recursos autenticados
- ✅ Health check del servicio con monitoreo de Redis
- ✅ Redis para almacenamiento rápido de tokens con TTL automático
- ✅ MariaDB para datos persistentes de usuarios
- ✅ Dockerización completa con Docker Compose
- ✅ Logging detallado para debugging
- ✅ Adminer incluido para gestión de BD
- ✅ Script de pruebas automatizadas

## Arquitectura

```mermaid
graph TB
    A[Cliente HTTP] --> B[Flask App :5000]
    B --> C[(MariaDB :3306 - Usuarios)]
    B --> D[(Redis :6379 - Tokens)]
    E[Adminer :8080] --> C
```

### Componentes

- **Flask App**: API REST principal que maneja todas las operaciones de autenticación
- **Redis**: Base de datos en memoria para almacenamiento temporal de tokens JWT con expiración automática
- **MariaDB**: Base de datos relacional para almacenar datos persistentes de usuarios
- **Adminer**: Interfaz web para gestión y consulta de la base de datos
- **JWT**: Sistema de tokens para autenticación stateless

## Flujo de Autenticación JWT

```mermaid
sequenceDiagram
    participant U as Usuario
    participant A as API Flask
    participant DB as MariaDB
    participant R as Redis

    U->>A: POST /register
    A->>DB: Insertar usuario
    DB-->>A: Usuario creado
    A-->>U: Usuario registrado

    U->>A: POST /login
    A->>DB: Verificar credenciales
    DB-->>A: Usuario válido
    A->>R: Almacenar tokens con TTL
    R-->>A: Tokens guardados
    A-->>U: access_token + refresh_token

    U->>A: GET /protected (con access_token)
    A->>R: Verificar token existe
    R-->>A: Token válido
    A-->>U: Datos protegidos

    U->>A: POST /refresh (con refresh_token)
    A->>R: Verificar refresh_token
    R-->>A: Token válido
    A->>R: Actualizar access_token
    R-->>A: Token actualizado
    A-->>U: nuevo access_token

    U->>A: POST /logout (con access_token)
    A->>R: Eliminar tokens
    R-->>A: Tokens eliminados
    A-->>U: Logout exitoso
```

## Prerrequisitos

- Docker (versión 20.10 o superior)
- Docker Compose (versión 1.29 o superior)
- Puertos disponibles:
  - Puerto 5000 (API Flask)
  - Puerto 3306 (MariaDB)
  - Puerto 6379 (Redis)
  - Puerto 8080 (Adminer)

## Instalación

1. **Clona el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd jwt-microservice
   ```

2. **Configura las variables de entorno**
   ```bash
   cp .env.example .env  # Si existe, o crea .env con las variables
   ```

3. **Construye y ejecuta los contenedores**
   ```bash
   docker-compose up --build
   ```

4. **Verifica que los servicios estén corriendo**
   - API: http://localhost:5000/health
   - Adminer: http://localhost:8080

## Configuración

### Variables de Entorno (.env)

```env
# Configuración de Base de Datos
DB_HOST=mariadb
DB_PORT=3306
DB_USER=jwt_user
DB_PASSWORD=jwt_password
DB_NAME=jwt_auth

# Configuración JWT
JWT_SECRET_KEY=UDEM
ACCESS_TOKEN_EXPIRES_MINUTES=15
REFRESH_TOKEN_EXPIRES_DAYS=7

# Configuración Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=redis_password
REDIS_MAXMEMORY=256mb
REDIS_MAXMEMORY_POLICY=allkeys-lru
```

### Descripción de Variables

- **DB_HOST**: Host de la base de datos (por defecto: mariadb)
- **DB_PORT**: Puerto de la base de datos (por defecto: 3306)
- **DB_USER**: Usuario de la base de datos
- **DB_PASSWORD**: Contraseña del usuario
- **DB_NAME**: Nombre de la base de datos
- **JWT_SECRET_KEY**: Clave secreta para firmar los tokens JWT
- **ACCESS_TOKEN_EXPIRES_MINUTES**: Tiempo de expiración del access token en minutos
- **REFRESH_TOKEN_EXPIRES_DAYS**: Tiempo de expiración del refresh token en días
- **REDIS_HOST**: Host de Redis (por defecto: redis)
- **REDIS_PORT**: Puerto de Redis (por defecto: 6379)
- **REDIS_PASSWORD**: Contraseña de Redis
- **REDIS_MAXMEMORY**: Memoria máxima para Redis (por defecto: 256mb)
- **REDIS_MAXMEMORY_POLICY**: Política de eviction de Redis (por defecto: allkeys-lru)

## Uso

### Acceso a los Servicios

- **API del Microservicio**: http://localhost:5000
- **Adminer (Gestión BD)**: http://localhost:8080
  - Usuario: jwt_user
  - Contraseña: jwt_password
  - Base de datos: jwt_auth

### Endpoints de la API

#### 1. Registro de Usuario
**POST** `/register`

Registra un nuevo usuario en el sistema.

**Request Body:**
```json
{
  "username": "usuario_ejemplo",
  "email": "usuario@example.com",
  "password": "contraseña_segura"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user_id": 1
}
```

#### 2. Login
**POST** `/login`

Autentica al usuario y devuelve tokens JWT.

**Request Body:**
```json
{
  "username": "usuario_ejemplo",
  "password": "contraseña_segura"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 900,
  "message": "Login successful"
}
```

#### 3. Refresh Token
**POST** `/refresh`

Renueva el access token usando el refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 900,
  "message": "Token refreshed successfully"
}
```

#### 4. Logout
**POST** `/logout`

Revoca el token actual del usuario.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

#### 5. Endpoint Protegido
**GET** `/protected`

Accede a recursos que requieren autenticación.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "message": "This is a protected endpoint",
  "user_id": 1,
  "data": "Secret data only for authenticated users"
}
```

#### 6. Health Check
**GET** `/health`

Verifica el estado del servicio, la conexión a la base de datos y Redis.

**Response (200):**
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "tables": ["users"],
  "redis_tokens": 5,
  "note": "Tokens managed in Redis, not database",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

## Pruebas

El proyecto incluye un script de pruebas automatizadas que verifica todas las funcionalidades.

### Ejecutar Pruebas

```bash
# Asegúrate de que los servicios estén corriendo
python test_jwt.py
```

### Qué Prueba el Script

- ✅ Salud del servicio
- ✅ Registro de usuario
- ✅ Login exitoso
- ✅ Acceso a endpoint protegido
- ✅ Refresh de token
- ✅ Logout y revocación
- ✅ Verificación de que el token fue revocado

### Pruebas Manuales

También puedes usar herramientas como Postman o curl. Consulta el archivo `commands-tests.txt` para ejemplos detallados de requests.

## Despliegue en Producción

### Consideraciones de Seguridad

1. **Cambia la JWT_SECRET_KEY** por una clave segura y única
2. **Configura REDIS_PASSWORD** con una contraseña fuerte
3. **Usa HTTPS** en producción
4. **Configura contraseñas fuertes** para la base de datos
5. **Aísla la red de Redis** - no expongas el puerto 6379 públicamente
6. **Configura REDIS_MAXMEMORY** según tus necesidades de carga
7. **Implementa rate limiting** para prevenir ataques de fuerza bruta
8. **Monitorea logs** para detectar actividades sospechosas
9. **Habilita persistencia de Redis** para recuperación ante fallos

### Variables de Producción

```env
JWT_SECRET_KEY=tu_clave_secreta_muy_segura_aqui
DB_PASSWORD=contraseña_muy_segura
REDIS_PASSWORD=redis_password_muy_segura
REDIS_MAXMEMORY=512mb
```


## Estructura del Proyecto

```
jwt-microservice/
├── app.py                 # Aplicación Flask principal con integración Redis
├── test_jwt.py           # Script de pruebas automatizadas
├── commands-tests.txt    # Ejemplos de requests para testing manual
├── requirements.txt      # Dependencias Python (incluye redis-py)
├── Dockerfile           # Dockerfile para la aplicación Flask
├── Dockerfile.mariadb   # Dockerfile personalizado para MariaDB
├── docker-compose.yml   # Configuración Docker Compose con Redis
├── init.sql            # Script de inicialización BD (solo tabla users)
├── .env                # Variables de entorno (DB, JWT, Redis)
└── README.md           # Este archivo
```

## Beneficios de Redis para JWT

### Rendimiento
- **Validación ultra-rápida**: Operaciones O(1) para verificar tokens
- **Sin consultas a BD**: Reducción del 90% en carga de base de datos para autenticación
- **Escalabilidad**: Manejo eficiente de miles de tokens concurrentes

### Seguridad y Gestión
- **Expiración automática**: Tokens se eliminan automáticamente al vencer TTL
- **Revocación inmediata**: Logout elimina tokens instantáneamente
- **Sin estado persistente**: Tokens no quedan en base de datos después de logout

### Arquitectura
- **Separación de responsabilidades**: Redis para datos efímeros, MariaDB para datos persistentes
- **Alta disponibilidad**: Redis con persistencia y configuración de memoria
- **Monitoreo integrado**: Health checks incluyen estado de Redis y conteo de tokens


¡El microservicio JWT con Redis está listo para usar! 🚀
