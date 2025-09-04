#!/bin/bash

# Script para detener todos los microservicios de la Joyería
# Uso: ./stop_services.sh

echo "🛑 Deteniendo Sistema de Microservicios - Joyería El Brillo"
echo "======================================================="

# Función para detener un servicio
stop_service() {
    local service_name=$1
    local pid_file="logs/${service_name}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat $pid_file)
        if ps -p $pid > /dev/null; then
            echo "🔄 Deteniendo $service_name (PID: $pid)..."
            kill $pid
            sleep 2
            
            # Si el proceso aún existe, forzar terminación
            if ps -p $pid > /dev/null; then
                echo "⚠️  Forzando terminación de $service_name..."
                kill -9 $pid
            fi
            
            echo "✅ $service_name detenido"
        else
            echo "⚠️  $service_name ya estaba detenido"
        fi
        rm -f $pid_file
    else
        echo "⚠️  No se encontró archivo PID para $service_name"
    fi
}

# Detener servicios
echo ""
echo "🛑 Deteniendo servicios..."
echo "========================="

stop_service "web_server"
stop_service "products_service"
stop_service "pedidos_service"
stop_service "facturas_service"

# Verificar y limpiar puertos ocupados
echo ""
echo "🔍 Limpiando puertos..."
echo "======================"

cleanup_port() {
    local port=$1
    if lsof -i:$port > /dev/null 2>&1; then
        echo "🔄 Liberando puerto $port..."
        sudo fuser -k $port/tcp 2>/dev/null
    fi
}

cleanup_port 80
cleanup_port 5001
cleanup_port 5002
cleanup_port 5003

echo ""
echo "🧹 Limpiando procesos Python restantes..."
pkill -f "python.*service.py" 2>/dev/null

echo ""
echo "✅ Todos los servicios han sido detenidos"
echo ""
echo "📋 Para reiniciar el sistema:"
echo "   ./start_services.sh"
echo ""
echo "======================================================="
