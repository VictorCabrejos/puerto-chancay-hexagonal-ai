#!/bin/bash

# 🚢 Puerto de Chancay - Setup Script
# Script de configuración automática para el proyecto

echo "🚢 Puerto de Chancay - Sistema de Gestión Inteligente"
echo "=================================================="
echo ""

# Verificar Python
echo "🔍 Verificando Python..."
if ! command -v python &> /dev/null; then
    echo "❌ Python no encontrado. Por favor instala Python 3.11+"
    exit 1
fi

PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "✅ Python $PYTHON_VERSION encontrado"

# Verificar si estamos en un entorno virtual
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Entorno virtual activo: $VIRTUAL_ENV"
else
    echo "⚠️ No se detectó entorno virtual activo"
    echo "💡 Recomendamos usar: conda create -n chancay_env python=3.11"
    echo ""
    read -p "¿Continuar sin entorno virtual? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "👋 Setup cancelado. Activa tu entorno virtual primero."
        exit 1
    fi
fi

# Instalar dependencias
echo ""
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error instalando dependencias"
    exit 1
fi

echo "✅ Dependencias instaladas correctamente"

# Verificar OpenAI API Key
echo ""
echo "🤖 Verificando configuración de OpenAI..."

if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️ Variable OPENAI_API_KEY no encontrada"
    echo ""
    echo "Opciones para configurar:"
    echo "1. export OPENAI_API_KEY='tu-api-key'"
    echo "2. Crear archivo .env con OPENAI_API_KEY=tu-api-key"
    echo "3. Editar config.py directamente"
    echo ""
    echo "💡 Obtén tu API key en: https://platform.openai.com/api-keys"
else
    echo "✅ OPENAI_API_KEY configurada"
fi

# Verificar estructura del proyecto
echo ""
echo "📁 Verificando estructura del proyecto..."

REQUIRED_DIRS=("domain" "adapters" "api" "templates" "data")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/"
    else
        echo "❌ $dir/ - Directorio faltante"
    fi
done

REQUIRED_FILES=("app.py" "config.py" "requirements.txt")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - Archivo faltante"
    fi
done

echo ""
echo "🚀 Setup completado!"
echo ""
echo "Para ejecutar el sistema:"
echo "  uvicorn app:app --host 0.0.0.0 --port 5000 --reload"
echo ""
echo "URLs importantes:"
echo "  🏠 Landing Page: http://localhost:5000/landing"
echo "  📊 Dashboard:    http://localhost:5000"
echo "  📚 API Docs:     http://localhost:5000/docs"
echo ""
echo "🎯 ¡Listo para demostrar Arquitectura Hexagonal + IA!"
