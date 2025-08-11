#!/usr/bin/env python3
"""
Script de prueba para la función Lambda de consulta de saldo.

Este script simula diferentes escenarios de llamadas a la función Lambda
para verificar su comportamiento con diferentes tipos de eventos.
"""

import json
import sys
import os

# Agregar el directorio actual al path para importar main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import lambda_handler

def test_successful_request():
    """Prueba una solicitud exitosa con user_id válido"""
    print("🧪 Probando solicitud exitosa...")
    
    event = {
        "version": "2.0",
        "routeKey": "GET /saldo",
        "rawPath": "/saldo",
        "rawQueryString": "user_id=12345",
        "queryStringParameters": {
            "user_id": "12345"
        },
        "requestContext": {
            "requestId": "test-request-123"
        }
    }
    
    result = lambda_handler(event, None)
    
    print(f"Status Code: {result['statusCode']}")
    print(f"Headers: {result['headers']}")
    print(f"Body: {result['body']}")
    print("✅ Prueba exitosa completada\n")

def test_missing_user_id():
    """Prueba una solicitud sin user_id"""
    print("🧪 Probando solicitud sin user_id...")
    
    event = {
        "version": "2.0",
        "routeKey": "GET /saldo",
        "rawPath": "/saldo",
        "rawQueryString": "",
        "queryStringParameters": None,
        "requestContext": {
            "requestId": "test-request-456"
        }
    }
    
    result = lambda_handler(event, None)
    
    print(f"Status Code: {result['statusCode']}")
    print(f"Headers: {result['headers']}")
    print(f"Body: {result['body']}")
    print("✅ Prueba sin user_id completada\n")

def test_empty_user_id():
    """Prueba una solicitud con user_id vacío"""
    print("🧪 Probando solicitud con user_id vacío...")
    
    event = {
        "version": "2.0",
        "routeKey": "GET /saldo",
        "rawPath": "/saldo",
        "rawQueryString": "user_id=",
        "queryStringParameters": {
            "user_id": ""
        },
        "requestContext": {
            "requestId": "test-request-789"
        }
    }
    
    result = lambda_handler(event, None)
    
    print(f"Status Code: {result['statusCode']}")
    print(f"Headers: {result['headers']}")
    print(f"Body: {result['body']}")
    print("✅ Prueba con user_id vacío completada\n")

def test_invalid_event():
    """Prueba un evento inválido"""
    print("🧪 Probando evento inválido...")
    
    event = {
        "invalid": "event",
        "missing": "required_fields"
    }
    
    result = lambda_handler(event, None)
    
    print(f"Status Code: {result['statusCode']}")
    print(f"Headers: {result['headers']}")
    print(f"Body: {result['body']}")
    print("✅ Prueba de evento inválido completada\n")

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 Iniciando pruebas de la función Lambda de consulta de saldo\n")
    
    try:
        test_successful_request()
        test_missing_user_id()
        test_empty_user_id()
        test_invalid_event()
        
        print("🎉 Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
