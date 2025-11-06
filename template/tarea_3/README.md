# MVP Banca Móvil - AWS CDK

Este proyecto implementa un MVP (Minimum Viable Product) de una aplicación de banca móvil utilizando AWS CDK en Python. El proyecto proporciona funcionalidades básicas de consulta de saldo e historial de movimientos bancarios.

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios

```
tarea3/
├── README.md                           # Documentación del proyecto
├── app_lambdas/                        # Funciones Lambda de la aplicación
│   ├── consulta_saldo/                 # Función para consultar saldo
│   │   ├── main.py                     # Código principal de la función
│   │   └── requirements.txt            # Dependencias de Python
│   └── historial_movimientos/          # Función para consultar historial
│       ├── main.py                     # Código principal de la función
│       └── requirements.txt            # Dependencias de Python
└── [CDK Stack Directory]               # Directorio principal del stack CDK
```

### 🏛️ Arquitectura Híbrida - MVP Banca Móvil

#### Diagrama de Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   App Móvil     │    │   AWS Cloud     │    │   On-Premise    │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │   Cliente   │ │    │ │ API Gateway │ │    │ │ Base de     │ │
│ │   Banking   │ │────│ │  (HTTP API) │ │    │ │ Datos       │ │
│ │   App       │ │    │ │             │ │    │ │ Principal   │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ │ (SQL Server │ │
│                 │    │        │        │    │ │  / Oracle)  │ │
└─────────────────┘    │ ┌─────────────┐ │    │ └─────────────┘ │
                       │ │   Lambda    │ │    │                 │
                       │ │  Functions  │ │    │ ┌─────────────┐ │
                       │ │             │ │    │ │   Router    │ │
                       │ │ ┌─────────┐ │ │    │ │   On-Prem   │ │
                       │ │ │Consulta │ │ │    │ │             │ │
                       │ │ │ Saldo   │ │ │    │ └─────────────┘ │
                       │ │ └─────────┘ │ │    │                 │
                       │ │ ┌─────────┐ │ │    │ ┌─────────────┐ │
                       │ │ │Historial│ │ │    │ │   VPN       │ │
                       │ │ │Movim.   │ │ │    │ │ Connection  │ │
                       │ │ └─────────┘ │ │    │ │             │ │
                       │ └─────────────┘ │    │ └─────────────┘ │
                       │        │        │    │                 │
                       │ ┌─────────────┐ │    │ ┌─────────────┐ │
                       │ │   VPC       │ │────│ │   Customer  │ │
                       │ │   Private   │ │    │ │   Gateway   │ │
                       │ │   Subnet    │ │    │ │             │ │
                       │ └─────────────┘ │    │ └─────────────┘ │
                       └─────────────────┘    └─────────────────┘
```

#### Flujo de Solicitud Completo

**1. Inicio de Solicitud**
```
App Móvil → API Gateway (HTTP API)
```

**2. Autenticación y Autorización**
```
API Gateway → Lambda Authorizer (opcional)
→ Validación de JWT Token
→ Verificación de permisos de cuenta
```

**3. Enrutamiento y Procesamiento**
```
API Gateway → Lambda Function (consulta_saldo/historial_movimientos)
→ Validación de parámetros de entrada
→ Preparación de consulta SQL
```

**4. Conexión a Base de Datos On-Premise**
```
Lambda Function → VPC Private Subnet
→ Customer Gateway (AWS)
→ Site-to-Site VPN Tunnel
→ Router On-Premise
→ Base de Datos Principal
```

**5. Respuesta y Retorno**
```
Base de Datos → Router → VPN → Lambda
→ Procesamiento de respuesta
→ Formateo JSON
→ API Gateway → App Móvil
```

### Componentes de la Arquitectura

#### 1. Funciones Lambda

**consulta_saldo**
- **Propósito**: Consultar el saldo actual de una cuenta bancaria
- **Entrada**: `account_id` (ID de la cuenta)
- **Salida**: Saldo actual, moneda y timestamp de última actualización
- **Endpoint**: `/consulta-saldo`
- **Conexión**: Base de datos on-premise vía VPN

**historial_movimientos**
- **Propósito**: Obtener el historial de transacciones de una cuenta
- **Entrada**: 
  - `account_id` (requerido)
  - `start_date` (opcional)
  - `end_date` (opcional)
  - `limit` (opcional, default: 50)
- **Salida**: Lista de transacciones con detalles
- **Endpoint**: `/historial-movimientos`
- **Conexión**: Base de datos on-premise vía VPN

#### 2. Servicios AWS Utilizados

| Componente | Propósito | Configuración |
|------------|-----------|---------------|
| **API Gateway** | Exposición de APIs REST | HTTP API (costo-efectivo) |
| **Lambda Functions** | Lógica de negocio | VPC-enabled, timeout 30s |
| **VPC** | Red privada para Lambda | Subnets privadas en 2 AZs |
| **Customer Gateway** | Conexión VPN a on-premise | IP estática del router |
| **VPN Connection** | Túnel seguro a on-premise | Site-to-Site VPN |
| **IAM Roles** | Permisos mínimos | Lambda execution role |
| **CloudWatch** | Monitoreo y logging | Logs automáticos |
| **Secrets Manager** | Credenciales DB | Rotación automática |
| **VPC Endpoints** | Acceso privado a servicios AWS | Para Secrets Manager |
| **Route Tables** | Enrutamiento de tráfico | Hacia VPN y VPC endpoints |

#### 3. Componentes On-Premise

| Componente | Propósito | Especificaciones |
|------------|-----------|------------------|
| **Router/Firewall** | Terminación VPN | Compatible con AWS VPN |
| **Base de Datos** | Datos de clientes | SQL Server/Oracle |
| **Red Local** | Conectividad interna | Subnet corporativa |

### 🔄 Flujo Detallado de Solicitud

#### Ejemplo: Consulta de Saldo

1. **App Móvil** envía solicitud HTTPS a API Gateway
   ```
   POST /consulta-saldo
   Headers: Authorization: Bearer <JWT>
   Body: {"account_id": "12345"}
   ```

2. **API Gateway** valida y enruta a Lambda
   - Validación de formato JSON
   - Rate limiting aplicado
   - Logging de acceso

3. **Lambda Function** procesa la solicitud
   ```python
   # Validación de entrada
   account_id = event.get('account_id')
   
   # Conexión a base de datos on-premise
   connection = get_db_connection()
   query = "SELECT balance, currency FROM accounts WHERE id = %s"
   result = execute_query(connection, query, [account_id])
   ```

4. **Conexión VPN** establece comunicación segura
   - Lambda en VPC privada
   - Túnel VPN encriptado
   - Latencia típica: 50-100ms

5. **Base de Datos On-Premise** ejecuta consulta
   - Validación de permisos de usuario
   - Ejecución de query optimizada
   - Retorno de resultados

6. **Respuesta** retorna por el mismo camino
   ```json
   {
     "statusCode": 200,
     "body": {
       "account_id": "12345",
       "balance": 15000.50,
       "currency": "USD",
       "last_updated": "2024-01-15T10:30:00Z"
     }
   }
   ```

### 🔒 Consideraciones de Seguridad

#### Encriptación
- **En Tránsito**: TLS 1.2+ en API Gateway y VPN
- **En Reposo**: Encriptación AES-256 en base de datos
- **Credenciales**: AWS Secrets Manager con rotación

#### Red y Acceso
- **VPC**: Lambda en subnets privadas
- **VPN**: Túnel encriptado IPSec
- **Firewall**: Reglas restrictivas en router on-premise
- **IAM**: Principio de menor privilegio

#### Monitoreo
- **CloudWatch**: Logs de Lambda y API Gateway
- **VPC Flow Logs**: Monitoreo de tráfico de red
- **VPN Metrics**: Estado y latencia de conexión

### 🌐 Configuración de Red y VPN

#### VPC y Subnets
```
VPC CIDR: 10.0.0.0/16
├── Private Subnet AZ-A: 10.0.1.0/24
├── Private Subnet AZ-B: 10.0.2.0/24
└── Route Tables:
    ├── Main Route Table: 0.0.0.0/0 → NAT Gateway
    └── Private Route Table: 0.0.0.0/0 → VPN Connection
```

#### Configuración VPN
- **Tipo**: Site-to-Site VPN
- **Encriptación**: AES256
- **Autenticación**: SHA256
- **Perfect Forward Secrecy**: Group 14 (2048-bit)
- **Túneles**: 2 túneles para alta disponibilidad
- **Latencia Esperada**: 50-100ms

#### Configuración On-Premise
- **Router/Firewall**: Compatible con AWS VPN
- **IP Pública**: Estática requerida
- **Subnet Local**: 192.168.1.0/24
- **Base de Datos**: 192.168.1.10

## 🚀 Funcionalidades del MVP

### Funcionalidades Implementadas

1. **Consulta de Saldo**
   - Verificar saldo actual de la cuenta
   - Información de moneda
   - Timestamp de última actualización

2. **Historial de Movimientos**
   - Lista de transacciones recientes
   - Filtrado por fechas
   - Paginación de resultados
   - Detalles de cada transacción

### Funcionalidades Futuras (Roadmap)

- [ ] Autenticación y autorización (Cognito)
- [ ] Transferencias entre cuentas
- [ ] Pagos y facturas
- [ ] Notificaciones push
- [ ] Análisis de gastos
- [ ] Integración con servicios de pago

## 📋 Requisitos Técnicos

### Prerrequisitos

- Python 3.8+
- AWS CLI configurado
- AWS CDK CLI instalado
- Node.js (para CDK)

### Dependencias Principales

```bash
# AWS CDK
aws-cdk-lib>=2.0.0
constructs>=10.0.0

# Funciones Lambda
boto3>=1.26.0
requests>=2.28.0

# Desarrollo
pytest>=7.0.0
black>=22.0.0
flake8>=5.0.0
```

## 🔧 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd tarea3
```

### 2. Configurar Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar AWS

```bash
aws configure
```

### 5. Desplegar la Infraestructura

```bash
cdk deploy
```

## 🧪 Testing

### Ejecutar Tests Unitarios

```bash
pytest tests/
```

### Testing de Funciones Lambda Localmente

```bash
# Consulta de saldo
python -c "
import json
from app_lambdas.consulta_saldo.main import lambda_handler
event = {'account_id': '12345'}
result = lambda_handler(event, None)
print(json.dumps(result, indent=2))
"

# Historial de movimientos
python -c "
import json
from app_lambdas.historial_movimientos.main import lambda_handler
event = {'account_id': '12345', 'limit': 10}
result = lambda_handler(event, None)
print(json.dumps(result, indent=2))
"
```

## 📊 Monitoreo y Logs

### CloudWatch Logs

Las funciones Lambda generan logs automáticamente en CloudWatch:

- **Grupo de Logs**: `/aws/lambda/banca-movil-consulta-saldo`
- **Grupo de Logs**: `/aws/lambda/banca-movil-historial-movimientos`

### Métricas Importantes

- Latencia de respuesta
- Tasa de errores
- Número de invocaciones
- Uso de memoria

## 🔒 Seguridad

### Medidas Implementadas

- **IAM Roles**: Permisos mínimos necesarios
- **VPC**: Aislamiento de red (opcional)
- **Encriptación**: Datos en tránsito y en reposo
- **Validación**: Validación de entrada en todas las funciones

### Buenas Prácticas

- Rotación de claves de acceso
- Monitoreo de acceso
- Auditoría regular de permisos
- Implementación de WAF para API Gateway

## 📈 Escalabilidad y Rendimiento

### Estrategias de Escalado

- **Auto-scaling**: Lambda se escala automáticamente
- **Caching**: Implementación de cache con ElastiCache
- **CDN**: Distribución de contenido estático
- **Load Balancing**: Distribución de carga con ALB

### ⚡ Optimización de Rendimiento Híbrido

#### Latencia y Tiempo de Respuesta
- **API Gateway**: ~10-50ms
- **Lambda Cold Start**: ~100-500ms (primera invocación)
- **Lambda Warm**: ~10-50ms
- **VPN Tunnel**: ~50-100ms
- **Base de Datos On-Premise**: ~5-20ms
- **Total Esperado**: ~175-720ms

#### Estrategias de Optimización
- **Connection Pooling**: Reutilización de conexiones DB
- **Lambda Warm-up**: Mantener instancias calientes
- **Query Optimization**: Índices y consultas optimizadas
- **Caching Strategy**: Cache de respuestas frecuentes
- **Async Processing**: Procesamiento asíncrono cuando sea posible

#### Monitoreo de Rendimiento
- **CloudWatch Metrics**: Latencia por endpoint
- **X-Ray Tracing**: Trazabilidad completa de requests
- **VPN Status**: Monitoreo de estado de conexión
- **Database Performance**: Métricas de consultas y conexiones

## 🛠️ Desarrollo

### Estructura de Desarrollo

```
tarea3/
├── tests/                              # Tests unitarios
├── docs/                               # Documentación técnica
├── scripts/                            # Scripts de utilidad
├── .github/                            # GitHub Actions
└── infrastructure/                     # Código CDK
    ├── stacks/                         # Stacks de CDK
    ├── constructs/                     # Constructos reutilizables
    └── app.py                          # Aplicación principal CDK
```

### Flujo de Desarrollo

1. **Feature Branch**: Crear rama para nueva funcionalidad
2. **Desarrollo**: Implementar en entorno local
3. **Testing**: Ejecutar tests unitarios e integración
4. **Code Review**: Revisión de código
5. **Deploy**: Despliegue a staging/producción

## 📞 Soporte

### Contacto

- **Equipo de Desarrollo**: dev-team@bancamovil.com
- **Soporte Técnico**: support@bancamovil.com
- **Documentación**: docs.bancamovil.com

### Recursos Adicionales

- [Documentación AWS CDK](https://docs.aws.amazon.com/cdk/)
- [Guía de Lambda](https://docs.aws.amazon.com/lambda/)
- [Mejores Prácticas de Seguridad](https://aws.amazon.com/security/)

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**Nota**: Este es un MVP educativo. Para uso en producción, se requieren implementaciones adicionales de seguridad, compliance y auditoría.
