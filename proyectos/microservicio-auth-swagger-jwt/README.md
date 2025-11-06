# Microservicio JWT con Swagger

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## ¿Qué es Swagger?

Swagger es una herramienta poderosa para diseñar, construir, documentar y consumir APIs REST. En este proyecto, utilizamos **Flasgger** (una extensión de Flask) para integrar Swagger/OpenAPI 2.0 directamente en nuestro microservicio.

### Beneficios de Swagger en este proyecto

- **Documentación Interactiva**: Genera automáticamente una interfaz web (`/apidocs/`) donde puedes explorar y probar todos los endpoints
- **Esquemas de Seguridad**: Define claramente cómo usar tokens JWT en las cabeceras de autorización
- **Validación Automática**: Los decoradores `@swag_from` validan que las respuestas coincidan con los esquemas definidos
- **Descubrimiento de APIs**: Los desarrolladores pueden entender rápidamente cómo consumir la API sin leer código

## Arquitectura del Microservicio

```text
Flask App (Puerto 5000)
├── Swagger UI (/apidocs/) - Documentación interactiva
├── Endpoints REST con documentación @swag_from
├── Autenticación JWT con Redis
└── Base de datos MariaDB
```

## Configuración de Swagger

El microservicio utiliza Flasgger con la siguiente configuración:

```python
swagger_config = {
    "specs": [{"endpoint": 'apispec', "route": '/apispec.json'}],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, config=swagger_config)
```

### Definición de Seguridad JWT

```python
swagger.template = {
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    }
}
```

## Endpoints Documentados con Swagger

### Autenticación

- `POST /register` - Registro de nuevos usuarios
- `POST /login` - Inicio de sesión y obtención de tokens
- `POST /refresh` - Renovación de tokens de acceso
- `POST /logout` - Cierre de sesión y revocación de tokens

### Recursos Protegidos

- `GET /protected` - Endpoint protegido que requiere autenticación
- `GET /users` - Lista de usuarios (requiere token)
- `DELETE /users/{id}` - Eliminación de usuario (solo propio usuario)

### Monitoreo

- `GET /health` - Verificación del estado del servicio

## Cómo Acceder a la Documentación Swagger

1. **Inicia el microservicio**:

   ```bash
   python app.py
   # o con Docker
   docker-compose up
   ```

2. **Abre tu navegador** y ve a:

   ```
   http://localhost:5000/apidocs/
   ```

3. **Explora la documentación interactiva**:

   - Verás todos los endpoints organizados por tags
   - Cada endpoint muestra parámetros, respuestas y ejemplos
   - Puedes probar los endpoints directamente desde la interfaz
   - La autenticación JWT está documentada en la sección de seguridad

## Uso de la API con Swagger

### 1. Registro de Usuario

En Swagger UI, expande el endpoint `POST /register` y haz click en "Try it out". Ingresa:

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepass123"
}
```

### 2. Inicio de Sesión

Usa `POST /login` para obtener tokens JWT:

```json
{
  "username": "testuser",
  "password": "securepass123"
}
```

La respuesta incluirá `access_token` y `refresh_token`.

### 3. Acceder a Endpoints Protegidos

Para endpoints protegidos, copia el `access_token` y pégalo en el campo "Authorize" (botón con candado) en la parte superior de Swagger UI, usando el formato:

```
Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### 4. Probar Endpoint Protegido

Ahora puedes probar `GET /protected` - debería funcionar sin errores de autenticación.

## Características Técnicas de la Implementación

### Decoradores Swagger

Cada endpoint usa `@swag_from` con un diccionario que define:

- **tags**: Agrupación lógica de endpoints
- **summary**: Título breve del endpoint
- **description**: Descripción detallada
- **parameters**: Esquema de entrada (body, path, query)
- **responses**: Códigos HTTP y esquemas de respuesta
- **security**: Requisitos de autenticación

### Validación Automática

Swagger valida que:

- Las respuestas HTTP coincidan con los esquemas definidos
- Los parámetros requeridos estén presentes
- Los tipos de datos sean correctos
- La documentación esté sincronizada con el código

### Seguridad JWT en Swagger

- Define el esquema "Bearer" para autenticación
- Documenta cómo pasar tokens en headers
- Valida automáticamente tokens en endpoints protegidos

## Beneficios para Desarrolladores

1. **Documentación Viva**: La documentación se mantiene actualizada automáticamente
2. **Pruebas Interactivas**: Prueba APIs sin escribir código adicional
3. **Descubrimiento Automático**: Encuentra endpoints fácilmente
4. **Validación**: Asegura consistencia entre código y documentación
5. **Colaboración**: Equipos pueden entender APIs rápidamente
