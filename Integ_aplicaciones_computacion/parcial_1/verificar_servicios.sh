#!/bin/bash

# Script de verificación para el sistema de microservicios
# Uso: ./verificar_servicios.sh

echo "🔍 Verificando Sistema de Microservicios - Joyería El Brillo"
echo "=========================================================="

# Función para verificar si un puerto está ocupado
check_port() {
    local port=$1
    local service_name=$2
    
    if lsof -i:$port > /dev/null 2>&1; then
        echo "✅ Puerto $port ($service_name) - OCUPADO"
        return 0
    else
        echo "❌ Puerto $port ($service_name) - LIBRE"
        return 1
    fi
}

# Función para verificar si un servicio responde
check_service() {
    local url=$1
    local service_name=$2
    
    if curl -s --max-time 5 $url > /dev/null 2>&1; then
        echo "✅ $service_name - RESPONDE"
        return 0
    else
        echo "❌ $service_name - NO RESPONDE"
        return 1
    fi
}

echo ""
echo "🔍 Verificando puertos..."
echo "========================="

check_port 80 "Servidor Web"
check_port 5001 "Servicio Productos"
check_port 5002 "Servicio Pedidos"
check_port 5003 "Servicio Facturas"

echo ""
echo "🌐 Verificando servicios..."
echo "============================"

check_service "http://localhost/" "Servidor Web"
check_service "http://localhost:5001/api/products" "API Productos"
check_service "http://localhost:5002/" "API Pedidos"
check_service "http://localhost:5003/" "API Facturas"

echo ""
echo "📋 Instrucciones:"
echo "=================="
echo "Si algún servicio no responde:"
echo "1. Ejecuta: ./start.sh"
echo "2. Espera unos segundos"
echo "3. Ejecuta este script nuevamente"
echo ""
echo "Si los puertos están ocupados pero los servicios no responden:"
echo "1. Ejecuta: ./stop.sh"
echo "2. Espera unos segundos"
echo "3. Ejecuta: ./start.sh"
echo ""
echo "Para ver logs de un servicio específico:"
echo "tail -f logs/[nombre_servicio].log"
