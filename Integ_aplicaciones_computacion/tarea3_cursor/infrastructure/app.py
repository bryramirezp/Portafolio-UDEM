#!/usr/bin/env python3
"""
Aplicación principal de AWS CDK para el MVP de Banca Móvil.

Este archivo instancia el stack principal de la aplicación de banca móvil
con arquitectura híbrida que conecta AWS Cloud con infraestructura on-premise.
"""

import aws_cdk as cdk
from stacks.banca_movil_stack import BancaMovilStack

app = cdk.App()

# Stack principal de Banca Móvil
BancaMovilStack(
    app, 
    "BancaMovilStack",
    description="MVP de Banca Móvil con arquitectura híbrida - AWS CDK",
    env=cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region") or "us-east-1"
    ),
    tags={
        "Project": "BancaMovil",
        "Environment": "MVP",
        "Team": "DevOps"
    }
)

app.synth()
