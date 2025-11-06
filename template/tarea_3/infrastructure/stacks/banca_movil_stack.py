#!/usr/bin/env python3
"""
Stack principal de Banca Móvil - AWS CDK

Este stack implementa la infraestructura completa para el MVP de banca móvil
con arquitectura híbrida que incluye:
- API Gateway (HTTP API)
- Lambda Functions (consulta_saldo, historial_movimientos)
- VPC con subnets privadas
- Customer Gateway y VPN Connection
- IAM Roles y políticas
- CloudWatch Logs
- Secrets Manager
"""

import os
from typing import Dict, Any
from aws_cdk import (
    Stack,
    aws_apigatewayv2 as apigw,
    aws_apigatewayv2_integrations as apigw_integrations,
    aws_lambda as _lambda,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_logs as logs,
    aws_secretsmanager as secretsmanager,
    Duration,
    RemovalPolicy,
    CfnOutput,
    Tags
)
from constructs import Construct


class BancaMovilStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Configuración del proyecto
        self.project_name = "banca-movil"
        self.environment = "mvp"
        
        # Crear VPC para la arquitectura híbrida
        self.vpc = self._create_vpc()
        
        # Crear Customer Gateway para VPN
        self.customer_gateway = self._create_customer_gateway()
        
        # Crear VPN Connection
        self.vpn_connection = self._create_vpn_connection()
        
        # Crear Secrets Manager para credenciales de base de datos
        self.db_secrets = self._create_db_secrets()
        
        # Crear roles IAM para Lambda
        self.lambda_role = self._create_lambda_role()
        
        # Crear funciones Lambda
        self.consulta_saldo_lambda = self._create_consulta_saldo_lambda()
        self.historial_movimientos_lambda = self._create_historial_movimientos_lambda()
        
        # Crear API Gateway
        self.api_gateway = self._create_api_gateway()
        
        # Crear outputs
        self._create_outputs()

    def _create_vpc(self) -> ec2.Vpc:
        """Crear VPC con subnets privadas para Lambda functions"""
        
        vpc = ec2.Vpc(
            self, 
            f"{self.project_name}-vpc",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                )
            ],
            nat_gateways=1,  # Para reducir costos en MVP
            enable_dns_hostnames=True,
            enable_dns_support=True
        )
        
        # Agregar tags
        Tags.of(vpc).add("Name", f"{self.project_name}-vpc")
        Tags.of(vpc).add("Environment", self.environment)
        
        return vpc

    def _create_customer_gateway(self) -> ec2.CfnCustomerGateway:
        """Crear Customer Gateway para conexión VPN on-premise"""
        
        # En producción, estas IPs vendrían de parámetros o context
        customer_gateway = ec2.CfnCustomerGateway(
            self,
            f"{self.project_name}-customer-gateway",
            bgp_asn=65000,
            ip_address="203.0.113.1",  # IP pública del router on-premise
            type="ipsec.1",
            tags=[
                {"key": "Name", "value": f"{self.project_name}-customer-gateway"},
                {"key": "Environment", "value": self.environment}
            ]
        )
        
        return customer_gateway

    def _create_vpn_connection(self) -> ec2.CfnVPNConnection:
        """Crear VPN Connection para conectar con infraestructura on-premise"""
        
        vpn_connection = ec2.CfnVPNConnection(
            self,
            f"{self.project_name}-vpn-connection",
            customer_gateway_id=self.customer_gateway.ref,
            type="ipsec.1",
            static_routes_only=False,
            vpn_gateway_id=self.vpc.vpn_gateway_id,
            vpn_tunnel_options_specifications=[
                {
                    "tunnelInsideIpVersion": "ipv4",
                    "preSharedKey": "banca-movil-vpn-key-2024",  # En producción usar Secrets Manager
                    "phase1EncryptionAlgorithms": ["AES256"],
                    "phase2EncryptionAlgorithms": ["AES256"],
                    "phase1IntegrityAlgorithms": ["SHA256"],
                    "phase2IntegrityAlgorithms": ["SHA256"],
                    "phase1DHGroupNumbers": [14],
                    "phase2DHGroupNumbers": [14],
                    "phase1LifetimeSeconds": 28800,
                    "phase2LifetimeSeconds": 3600,
                    "rekeyMarginTimeSeconds": 540,
                    "rekeyFuzzPercentage": 100,
                    "replayWindowSize": 1024,
                    "dpdTimeoutSeconds": 30,
                    "dpdTimeoutAction": "restart"
                }
            ],
            tags=[
                {"key": "Name", "value": f"{self.project_name}-vpn-connection"},
                {"key": "Environment", "value": self.environment}
            ]
        )
        
        return vpn_connection

    def _create_db_secrets(self) -> secretsmanager.Secret:
        """Crear secretos para credenciales de base de datos on-premise"""
        
        db_secrets = secretsmanager.Secret(
            self,
            f"{self.project_name}-db-secrets",
            secret_name=f"{self.project_name}/database/credentials",
            description="Credenciales para base de datos on-premise",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template='{"username": "banca_movil_user"}',
                generate_string_key="password",
                exclude_characters="\"@/\\",
                password_length=32
            ),
            removal_policy=RemovalPolicy.DESTROY  # Solo para MVP
        )
        
        return db_secrets

    def _create_lambda_role(self) -> iam.Role:
        """Crear rol IAM para las funciones Lambda"""
        
        lambda_role = iam.Role(
            self,
            f"{self.project_name}-lambda-role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ],
            inline_policies={
                "SecretsManagerAccess": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "secretsmanager:GetSecretValue",
                                "secretsmanager:DescribeSecret"
                            ],
                            resources=[self.db_secrets.secret_arn]
                        )
                    ]
                ),
                "CloudWatchLogs": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "logs:CreateLogGroup",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents"
                            ],
                            resources=["*"]
                        )
                    ]
                )
            }
        )
        
        return lambda_role

    def _create_consulta_saldo_lambda(self) -> _lambda.Function:
        """Crear función Lambda para consulta de saldo"""
        
        # Leer el código de la función Lambda
        lambda_code = _lambda.Code.from_asset("app_lambdas/consulta_saldo")
        
        consulta_saldo_lambda = _lambda.Function(
            self,
            f"{self.project_name}-consulta-saldo",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="main.lambda_handler",
            code=lambda_code,
            role=self.lambda_role,
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={
                "DB_SECRETS_ARN": self.db_secrets.secret_arn,
                "ENVIRONMENT": self.environment,
                "POWERTOOLS_SERVICE_NAME": "consulta-saldo"
            },
            log_retention=logs.RetentionDays.ONE_WEEK
        )
        
        # Agregar tags
        Tags.of(consulta_saldo_lambda).add("Name", f"{self.project_name}-consulta-saldo")
        Tags.of(consulta_saldo_lambda).add("Environment", self.environment)
        
        return consulta_saldo_lambda

    def _create_historial_movimientos_lambda(self) -> _lambda.Function:
        """Crear función Lambda para historial de movimientos"""
        
        # Leer el código de la función Lambda
        lambda_code = _lambda.Code.from_asset("app_lambdas/historial_movimientos")
        
        historial_movimientos_lambda = _lambda.Function(
            self,
            f"{self.project_name}-historial-movimientos",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="main.lambda_handler",
            code=lambda_code,
            role=self.lambda_role,
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={
                "DB_SECRETS_ARN": self.db_secrets.secret_arn,
                "ENVIRONMENT": self.environment,
                "POWERTOOLS_SERVICE_NAME": "historial-movimientos"
            },
            log_retention=logs.RetentionDays.ONE_WEEK
        )
        
        # Agregar tags
        Tags.of(historial_movimientos_lambda).add("Name", f"{self.project_name}-historial-movimientos")
        Tags.of(historial_movimientos_lambda).add("Environment", self.environment)
        
        return historial_movimientos_lambda

    def _create_api_gateway(self) -> apigw.HttpApi:
        """Crear API Gateway HTTP API"""
        
        # Crear integraciones para las funciones Lambda
        consulta_saldo_integration = apigw_integrations.HttpLambdaIntegration(
            "consulta-saldo-integration",
            self.consulta_saldo_lambda
        )
        
        historial_movimientos_integration = apigw_integrations.HttpLambdaIntegration(
            "historial-movimientos-integration",
            self.historial_movimientos_lambda
        )
        
        # Crear HTTP API
        api = apigw.HttpApi(
            self,
            f"{self.project_name}-api",
            api_name=f"{self.project_name}-api",
            description="API para MVP de Banca Móvil",
            cors_preflight=apigw.CorsPreflightOptions(
                allow_headers=["Content-Type", "Authorization"],
                allow_methods=[apigw.CorsHttpMethod.GET, apigw.CorsHttpMethod.POST],
                allow_origins=["*"],  # En producción especificar dominios específicos
                max_age=Duration.days(1)
            ),
            default_integration=consulta_saldo_integration
        )
        
        # Agregar rutas
        api.add_routes(
            path="/saldo",
            methods=[apigw.HttpMethod.GET, apigw.HttpMethod.POST],
            integration=consulta_saldo_integration
        )
        
        api.add_routes(
            path="/historial",
            methods=[apigw.HttpMethod.GET, apigw.HttpMethod.POST],
            integration=historial_movimientos_integration
        )
        
        # Agregar tags
        Tags.of(api).add("Name", f"{self.project_name}-api")
        Tags.of(api).add("Environment", self.environment)
        
        return api

    def _create_outputs(self):
        """Crear outputs para información importante del stack"""
        
        CfnOutput(
            self,
            "ApiGatewayUrl",
            value=self.api_gateway.url,
            description="URL del API Gateway",
            export_name=f"{self.project_name}-api-url"
        )
        
        CfnOutput(
            self,
            "VpcId",
            value=self.vpc.vpc_id,
            description="ID de la VPC",
            export_name=f"{self.project_name}-vpc-id"
        )
        
        CfnOutput(
            self,
            "CustomerGatewayId",
            value=self.customer_gateway.ref,
            description="ID del Customer Gateway",
            export_name=f"{self.project_name}-customer-gateway-id"
        )
        
        CfnOutput(
            self,
            "VpnConnectionId",
            value=self.vpn_connection.ref,
            description="ID de la VPN Connection",
            export_name=f"{self.project_name}-vpn-connection-id"
        )
        
        CfnOutput(
            self,
            "DbSecretsArn",
            value=self.db_secrets.secret_arn,
            description="ARN de los secretos de base de datos",
            export_name=f"{self.project_name}-db-secrets-arn"
        )
        
        CfnOutput(
            self,
            "ConsultaSaldoLambdaArn",
            value=self.consulta_saldo_lambda.function_arn,
            description="ARN de la función Lambda de consulta de saldo",
            export_name=f"{self.project_name}-consulta-saldo-lambda-arn"
        )
        
        CfnOutput(
            self,
            "HistorialMovimientosLambdaArn",
            value=self.historial_movimientos_lambda.function_arn,
            description="ARN de la función Lambda de historial de movimientos",
            export_name=f"{self.project_name}-historial-movimientos-lambda-arn"
        )
