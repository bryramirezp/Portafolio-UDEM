#!/bin/bash

# Script para iniciar todos los microservicios de la Joyería
# Uso: ./start_services.sh

echo "🚀 Iniciando Sistema de Microservicios - Joyería El Brillo"
echo "=================================================="

# Verificar que estamos en el directorio correcto
if [ ! -f "web_server.py" ] || [ ! -f "products_service.py" ]; then
    echo "❌ Error: No se encontraron los archivos de servicios."
    echo "   Asegúrate de ejecutar este script desde ~/parcial1/"
    exit 1
fi

# Crear directorio para logs
mkdir -p logs

# Función para verificar si un puerto está ocupado
check_port() {
    if lsof -i:$1 > /dev/null 2>&1; then
        echo "⚠️  Puerto $1 ya está en uso. Terminando proceso..."
        sudo fuser -k $1/tcp 2>/dev/null
        sleep 2
    fi
}

# Verificar y limpiar puertos
echo "🔍 Verificando puertos..."
check_port 80
check_port 5001
check_port 5002
check_port 5003

# Función para iniciar un servicio
start_service() {
    local service_name=$1
    local service_file=$2
    local port=$3
    
    echo "🔄 Iniciando $service_name (puerto $port)..."
    nohup python3 $service_file > logs/${service_name}.log 2>&1 &
    local pid=$!
    echo $pid > logs/${service_name}.pid
    
    # Verificar que el servicio inició correctamente
    sleep 3
    if ps -p $pid > /dev/null; then
        echo "✅ $service_name iniciado correctamente (PID: $pid)"
    else
        echo "❌ Error al iniciar $service_name"
        cat logs/${service_name}.log
        return 1
    fi
}

# Iniciar servicios
echo ""
echo "🚀 Iniciando servicios..."
echo "========================="

start_service "web_server" "web_server.py" "80"
start_service "products_service" "products_service.py" "5001"
start_service "pedidos_service" "pedidos_service.py" "5002"
start_service "facturas_service" "facturas_service.py" "5003"

echo ""
echo "⏳ Esperando que todos los servicios estén listos..."
sleep 5

# Verificar que todos los servicios están corriendo
echo ""
echo "🔍 Verificando estado de servicios..."
echo "====================================="

services_ok=true

check_service() {
    local service_name=$1
    local port=$2
    local url=$3
    
    if curl -s --max-time 5 $url > /dev/null; then
        echo "✅ $service_name - OK"
    else
        echo "❌ $service_name - ERROR"
        services_ok=false
    fi
}

check_service "Servidor Web" "80" "http://localhost/"
check_service "Servicio Productos" "5001" "http://localhost:5001/api/products"
check_service "Servicio Pedidos" "5002" "http://localhost:5002/"
check_service "Servicio Facturas" "5003" "http://localhost:5003/"

echo ""
if [ "$services_ok" = true ]; then
    echo "🎉 ¡Todos los servicios están funcionando correctamente!"
    echo ""
    echo "🌐 Accesos disponibles:"
    echo "   Frontend: http://34.57.252.58/"
    echo "   Productos API: http://34.57.252.58:5001/api/products"
    echo "   Pedidos API: http://34.57.252.58:5002/api/pedidos"
    echo "   Facturas API: http://34.57.252.58:5003/api/facturas"
    echo ""
    echo "📋 Para ver logs:"
    echo "   tail -f logs/web_server.log"
    echo "   tail -f logs/products_service.log"
    echo "   tail -f logs/pedidos_service.log"
    echo "   tail -f logs/facturas_service.log"
    echo ""
    echo "🛑 Para detener todos los servicios:"
    echo "   ./stop_services.sh"
else
    echo "⚠️  Algunos servicios tienen problemas. Revisa los logs en el directorio 'logs/'"
fi

echo ""
echo "=================================================="
