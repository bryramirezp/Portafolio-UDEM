import json
import logging
import boto3
import os
from typing import Dict, Any
from datetime import datetime

# Configurar logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Función Lambda para consultar el saldo de una cuenta bancaria.
    
    Args:
        event: Evento de entrada de API Gateway v2 (HTTP API)
        context: Contexto de ejecución de Lambda
    
    Returns:
        Dict con la respuesta en formato API Gateway v2
    """
    try:
        logger.info(f"Evento recibido: {json.dumps(event, indent=2)}")
        
        # Extraer user_id de los query string parameters
        query_params = event.get('queryStringParameters', {}) or {}
        user_id = query_params.get('user_id')
        
        logger.info(f"Query parameters: {query_params}")
        logger.info(f"User ID extraído: {user_id}")
        
        # Validar que user_id esté presente
        if not user_id:
            logger.error("user_id no encontrado en query parameters")
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
                },
                'body': json.dumps({
                    'error': 'user_id es requerido en query parameters',
                    'message': 'Debe proporcionar user_id como parámetro de consulta',
                    'example': '/saldo?user_id=12345'
                })
            }
        
        # TODO: Implementar llamada real al servicio interno on-premise
        # Ejemplo de implementación:
        # - Obtener credenciales de Secrets Manager
        # - Establecer conexión VPN a base de datos on-premise
        # - Ejecutar consulta SQL: SELECT balance FROM accounts WHERE user_id = %s
        # - Procesar resultado y retornar
        
        logger.info(f"Simulando consulta de saldo para user_id: {user_id}")
        
        # Simular llamada al servicio interno on-premise
        # En producción, aquí iría la lógica real de conexión a la base de datos
        mock_balance_data = {
            'userId': user_id,
            'balance': 5450.75,
            'currency': 'USD',
            'accountType': 'CHECKING',
            'lastUpdated': datetime.utcnow().isoformat() + 'Z',
            'status': 'ACTIVE'
        }
        
        logger.info(f"Saldo obtenido: {mock_balance_data}")
        
        # Retornar respuesta en formato API Gateway v2
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': json.dumps(mock_balance_data, indent=2)
        }
        
    except KeyError as e:
        logger.error(f"Error al acceder a parámetros del evento: {str(e)}")
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': json.dumps({
                'error': 'Formato de evento inválido',
                'message': f'Error al procesar parámetros: {str(e)}'
            })
        }
        
    except Exception as e:
        logger.error(f"Error interno del servidor: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': json.dumps({
                'error': 'Error interno del servidor',
                'message': 'Ocurrió un error inesperado al procesar la solicitud',
                'requestId': context.aws_request_id if context else 'unknown'
            })
        }
