# Cliente GUI JavaFX para Microservicio JWT

![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![JavaFX](https://img.shields.io/badge/JavaFX-007396?style=for-the-badge&logo=java&logoColor=white)
![Maven](https://img.shields.io/badge/Maven-C71A36?style=for-the-badge&logo=apache-maven&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

## Vista Previa

![Vista de la aplicación JavaFX](java-gui.png)

## Descripción

Cliente JavaFX moderno para consumir el microservicio JWT. Interfaz gráfica nativa con autenticación completa, gestión de tokens JWT y operaciones protegidas.

## Arquitectura

```mermaid
graph TB
    A[JavaFX GUI] --> B[OkHttp Client]
    B --> C[Flask Microservice :5000]
    C --> D[(MariaDB :3306)]
    C --> E[(Redis :6379)]
    A --> F[(JSON Config File)]
```

**Nota**: Los tokens JWT se gestionan únicamente en Redis, no se almacenan localmente.

## Flujo de Autenticación

```mermaid
stateDiagram-v2
    [*] --> Login: Credenciales
    Login --> Autenticado: Tokens JWT en Redis

    Autenticado --> Protegido: Bearer Token
    Protegido --> Autenticado: Validado contra Redis

    Autenticado --> Refresh: Refresh Token
    Refresh --> Autenticado: Nuevo Access Token

    Autenticado --> Logout: Revocar
    Logout --> [*]: Tokens eliminados de Redis
```

## Tecnologías

- **JavaFX**: UI nativa moderna
- **OkHttp**: Cliente HTTP
- **Jackson**: JSON processing
- **Maven**: Build system

## Inicio Rápido

```bash
# Requisitos: JDK 17+, Maven 3.6+, Microservicio JWT corriendo

# Ejecutar
mvn clean compile
mvn javafx:run
```

## Configuración

**JSON Config File**: Archivo local que guarda la configuración del cliente (IP, puerto, URLs de endpoints). Se genera automáticamente y permite cambiar la conexión al microservicio sin recompilar.

```json
{
  "ip": "localhost",
  "port": "5000",
  "endpoints": {
    "register": "/register",
    "login": "/login",
    "protected": "/protected",
    "refresh": "/refresh",
    "logout": "/logout",
    "users": "/users"
  }
}
```

## Estructura del Proyecto

```
cliente-jwt-gui/
├── src/main/java/com/example/jwttest/
│   ├── Main.java              # Entry point
│   └── JWTController.java     # Business logic
├── src/main/resources/jwt-gui.fxml
├── pom.xml
└── README.md
```

```bash
cliente-jwt-gui/
├── src/main/java/com/example/jwttest/Main.java
├── src/main/java/com/example/jwttest/JWTController.java
├── src/main/resources/jwt-gui.fxml
├── pom.xml
├── jwt_gui_config.json
└── README.md
```

