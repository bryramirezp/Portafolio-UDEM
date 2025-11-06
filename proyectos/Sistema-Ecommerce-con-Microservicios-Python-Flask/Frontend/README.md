# Frontend - Sistema de Joyería "El Brillo"

Este frontend desacoplado consume los microservicios de la joyería desde máquinas remotas.

## 🚀 Ejecución en Máquina Separada

### Prerrequisitos
- Python 3.8+
- pip

### Instalación y Ejecución
```bash
# Instalar dependencias
pip install flask flask-cors

# Ejecutar servidor web
python web_server.py
```

### Acceso
- Abrir navegador: `http://<IP_DE_ESTA_MAQUINA>:8080`
- Configurar URLs de microservicios en la interfaz

### Configuración de URLs
En la interfaz web, configurar:
- Products URL: `http://<IP_MAQUINA_MICROSERVICIOS>:5001`
- Pedidos URL: `http://<IP_MAQUINA_MICROSERVICIOS>:5002`
- Facturas URL: `http://<IP_MAQUINA_MICROSERVICIOS>:5003`

## 📁 Estructura de Archivos
- `index.html` - Interfaz principal
- `estilo.css` - Estilos CSS
- `factura.js` - Lógica JavaScript
- `factura.xsl` - Transformación XSL para facturas
- `web_server.py` - Servidor Flask para archivos estáticos