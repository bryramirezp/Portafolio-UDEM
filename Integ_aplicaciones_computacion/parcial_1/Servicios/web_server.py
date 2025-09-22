# web_server.py (Flask Version, Port 8080 - IP Dinámica)
from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# Ahora apuntamos directamente a parcial1/
base_dir = os.path.dirname(os.path.abspath(__file__))

def get_external_ip():
    """Detecta automáticamente la IP externa del servidor"""
    try:
        # Intentar obtener IP desde el servicio de metadatos de Google Cloud
        response = requests.get(
            'http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip',
            headers={'Metadata-Flavor': 'Google'},
            timeout=5
        )
        if response.status_code == 200:
            return response.text.strip()
    except:
        pass
    
    # Fallback: usar servicio externo
    try:
        response = requests.get('https://ipinfo.io/ip', timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except:
        pass
    
    # Si todo falla, usar localhost
    return 'localhost'

@app.route('/')
def serve_index():
    return send_from_directory(base_dir, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(base_dir, path)

if __name__ == '__main__':
    # Detectar IP externa automáticamente
    external_ip = get_external_ip()
    PORT = 8080
    
    print("=" * 50)
    print("🚀 SERVIDOR WEB INICIADO")
    print("=" * 50)
    print(f"IP Externa detectada: {external_ip}")
    print(f"Puerto: {PORT}")
    print("")
    print("📱 URLs de acceso:")
    print(f"   Frontend: http://{external_ip}:{PORT}/")
    print(f"   Local:    http://localhost:{PORT}/")
    print("")
    print("🔗 URLs de microservicios:")
    print(f"   Productos: http://{external_ip}:5001/api/products")
    print(f"   Pedidos:   http://{external_ip}:5002/api/pedidos")
    print(f"   Facturas:  http://{external_ip}:5003/api/facturas")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=PORT, debug=True)
