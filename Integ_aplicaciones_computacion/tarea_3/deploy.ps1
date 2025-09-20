#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script de despliegue para el MVP de Banca Móvil - AWS CDK

.DESCRIPTION
    Este script automatiza el proceso de despliegue del stack de AWS CDK
    para el MVP de banca móvil con arquitectura híbrida.

.PARAMETER Environment
    El ambiente de despliegue (dev, staging, prod)

.PARAMETER Region
    La región de AWS donde desplegar

.EXAMPLE
    .\deploy.ps1 -Environment dev -Region us-east-1
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("dev", "staging", "prod")]
    [string]$Environment = "dev",
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-east-1"
)

Write-Host "🚀 Iniciando despliegue del MVP de Banca Móvil..." -ForegroundColor Green
Write-Host "📋 Configuración:" -ForegroundColor Yellow
Write-Host "   Ambiente: $Environment" -ForegroundColor White
Write-Host "   Región: $Region" -ForegroundColor White

# Verificar que AWS CLI esté configurado
Write-Host "`n🔍 Verificando configuración de AWS..." -ForegroundColor Yellow
try {
    aws sts get-caller-identity | Out-Null
    Write-Host "✅ AWS CLI configurado correctamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: AWS CLI no está configurado" -ForegroundColor Red
    Write-Host "   Ejecuta 'aws configure' para configurar tus credenciales" -ForegroundColor Red
    exit 1
}

# Verificar que CDK esté instalado
Write-Host "`n🔍 Verificando AWS CDK..." -ForegroundColor Yellow
try {
    cdk --version | Out-Null
    Write-Host "✅ AWS CDK instalado correctamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: AWS CDK no está instalado" -ForegroundColor Red
    Write-Host "   Instala CDK con: npm install -g aws-cdk" -ForegroundColor Red
    exit 1
}

# Instalar dependencias de Python
Write-Host "`n📦 Instalando dependencias de Python..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error al instalar dependencias" -ForegroundColor Red
    exit 1
}

# Bootstrap CDK (si es necesario)
Write-Host "`n🔧 Verificando bootstrap de CDK..." -ForegroundColor Yellow
try {
    cdk bootstrap aws://$env:AWS_ACCOUNT_ID/$Region
    Write-Host "✅ CDK bootstrap completado" -ForegroundColor Green
} catch {
    Write-Host "⚠️  CDK bootstrap ya configurado o error (continuando...)" -ForegroundColor Yellow
}

# Sintetizar el stack
Write-Host "`n🏗️ Sintetizando stack..." -ForegroundColor Yellow
try {
    cdk synth --context environment=$Environment --context region=$Region
    Write-Host "✅ Stack sintetizado correctamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error al sintetizar el stack" -ForegroundColor Red
    exit 1
}

# Desplegar el stack
Write-Host "`n🚀 Desplegando stack..." -ForegroundColor Yellow
try {
    cdk deploy --context environment=$Environment --context region=$Region --require-approval never
    Write-Host "✅ Stack desplegado correctamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error al desplegar el stack" -ForegroundColor Red
    exit 1
}

# Mostrar outputs
Write-Host "`n📊 Información del despliegue:" -ForegroundColor Yellow
try {
    cdk list
    Write-Host "`n🔗 URLs de la API:" -ForegroundColor Cyan
    Write-Host "   - Consulta de Saldo: https://[API_ID].execute-api.$Region.amazonaws.com/saldo" -ForegroundColor White
    Write-Host "   - Historial: https://[API_ID].execute-api.$Region.amazonaws.com/historial" -ForegroundColor White
} catch {
    Write-Host "⚠️  No se pudieron mostrar los outputs" -ForegroundColor Yellow
}

Write-Host "`n🎉 ¡Despliegue completado exitosamente!" -ForegroundColor Green
Write-Host "📚 Para más información, consulta el README.md" -ForegroundColor Cyan
