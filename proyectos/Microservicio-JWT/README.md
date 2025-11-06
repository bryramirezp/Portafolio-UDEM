# Microservicio JWT

Este proyecto es un microservicio de autenticación basado en JSON Web Tokens (JWT) desarrollado con Flask y Python. Proporciona una API REST completa para gestionar la autenticación de usuarios, incluyendo registro, login, refresh de tokens, logout y acceso a recursos protegidos. Utiliza MariaDB como base de datos y está completamente dockerizado para facilitar el despliegue.

## Tecnologías Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)
![Adminer](https://img.shields.io/badge/Adminer-FF6600?style=for-the-badge&logo=adminer&logoColor=white)
![PyJWT](https://img.shields.io/badge/PyJWT-000000?style=for-the-badge&logo=python&logoColor=white)

## Características

- ✅ Registro de usuarios con validación
- ✅ Autenticación segura con JWT
- ✅ Sistema de refresh tokens
- ✅ Revocación de tokens en logout
- ✅ Endpoint protegido para recursos autenticados
- ✅ Health check del servicio
- ✅ Base de datos MariaDB con configuración UTF-8
- ✅ Dockerización completa con Docker Compose
- ✅ Logging detallado para debugging
- ✅ Adminer incluido para gestión de BD
- ✅ Script de pruebas automatizadas

## Arquitectura

```mermaid
graph TB
    A[Cliente HTTP] --> B[Flask App :5000]
    B --> C[(MariaDB :3306)]
    B --> D[JWT Tokens]
    E[Adminer :8080] --> C
```

### Componentes

- **Flask App**: API REST principal que maneja todas las operaciones de autenticación
- **MariaDB**: Base de datos relacional para almacenar usuarios y tokens
- **Adminer**: Interfaz web para gestión y consulta de la base de datos
- **JWT**: Sistema de tokens para autenticación stateless

## Flujo de Autenticación JWT

```mermaid
sequenceDiagram
    participant U as Usuario
    participant A as API Flask
    participant DB as MariaDB

    U->>A: POST /register
    A->>DB: Insertar usuario
    DB-->>A: Usuario creado
    A-->>U: Usuario registrado

    U->>A: POST /login
    A->>DB: Verificar credenciales
    DB-->>A: Usuario válido
    A->>DB: Almacenar tokens
    DB-->>A: Tokens guardados
    A-->>U: access_token + refresh_token

    U->>A: GET /protected (con access_token)
    A->>DB: Verificar token válido
    DB-->>A: Token válido
    A-->>U: Datos protegidos

    U->>A: POST /refresh (con refresh_token)
    A->>DB: Verificar refresh_token
    DB-->>A: Token válido
    A->>DB: Actualizar access_token
    DB-->>A: Token actualizado
    A-->>U: nuevo access_token

    U->>A: POST /logout (con access_token)
    A->>DB: Revocar token
    DB-->>A: Token revocado
    A-->>U: Logout exitoso
```

## Prerrequisitos

- Docker (versión 20.10 o superior)
- Docker Compose (versión 1.29 o superior)
- Puerto 5000 disponible (API)
- Puerto 3306 disponible (MariaDB)
- Puerto 8080 disponible (Adminer)

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

Verifica el estado del servicio y la conexión a la base de datos.

**Response (200):**
```json
{
  "status": "healthy",
  "database": "connected",
  "tables": ["users", "tokens"],
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

## Estructura del Proyecto

```
jwt-microservice/
├── app.py                 # Aplicación Flask principal
├── test_jwt.py           # Script de pruebas
├── commands-tests.txt    # Ejemplos de requests para Postman
├── requirements.txt      # Dependencias Python
├── Dockerfile           # Dockerfile para la app
├── Dockerfile.mariadb   # Dockerfile para MariaDB
├── docker-compose.yml   # Configuración Docker Compose
├── init.sql            # Script de inicialización BD
├── .env                # Variables de entorno
└── README.md           # Este archivo
```

¡El microservicio JWT está listo para usar! 🚀
