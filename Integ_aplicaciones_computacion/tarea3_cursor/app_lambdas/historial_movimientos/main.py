import json
import boto3
import os
from typing import Dict, Any
from datetime import datetime, timedelta

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Función Lambda para consultar el historial de movimientos de una cuenta bancaria.
    
    Args:
        event: Evento de entrada que contiene el ID de la cuenta y filtros opcionales
        context: Contexto de ejecución de Lambda
    
    Returns:
        Dict con el historial de movimientos y metadatos
    """
    try:
        # Extraer parámetros del evento
        account_id = event.get('account_id')
        start_date = event.get('start_date')
        end_date = event.get('end_date')
        limit = event.get('limit', 50)
        
        if not account_id:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'account_id es requerido'
                })
            }
        
        # TODO: Implementar lógica de consulta a base de datos
        # Por ahora retornamos movimientos de ejemplo
        mock_transactions = [
            {
                'transaction_id': 'TXN001',
                'account_id': account_id,
                'type': 'DEPOSIT',
                'amount': 5000.00,
                'description': 'Depósito inicial',
                'timestamp': '2024-01-15T09:00:00Z',
                'balance_after': 5000.00
            },
            {
                'transaction_id': 'TXN002',
                'account_id': account_id,
                'type': 'WITHDRAWAL',
                'amount': -150.25,
                'description': 'Retiro en cajero',
                'timestamp': '2024-01-15T14:30:00Z',
                'balance_after': 4849.75
            },
            {
                'transaction_id': 'TXN003',
                'account_id': account_id,
                'type': 'TRANSFER',
                'amount': -500.00,
                'description': 'Transferencia a cuenta 12345',
                'timestamp': '2024-01-16T10:15:00Z',
                'balance_after': 4349.75
            }
        ]
        
        # Aplicar filtros si se proporcionan
        if start_date or end_date:
            # TODO: Implementar filtrado por fecha
            pass
        
        # Limitar resultados
        mock_transactions = mock_transactions[:limit]
        
        response_data = {
            'account_id': account_id,
            'transactions': mock_transactions,
            'total_count': len(mock_transactions),
            'has_more': False
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error interno del servidor: {str(e)}'
            })
        }
