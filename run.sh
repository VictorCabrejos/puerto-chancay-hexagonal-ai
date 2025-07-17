#!/bin/bash

echo "========================================"
echo "   Puerto de Chancay Container Tracker"
echo "   Arquitectura Hexagonal + GPT-4o mini"
echo "========================================"
echo

echo "🔍 Activando environment ds_env..."
conda activate ds_env
if [ $? -ne 0 ]; then
    echo "❌ No se pudo activar el environment ds_env."
    echo "📝 Verifica que Miniconda esté instalado y que el environment ds_env exista."
    exit 1
fi

python --version

echo
echo "📦 Instalando dependencias en ds_env..."
pip install -r requirements.txt

echo
echo "🚢 Iniciando Puerto de Chancay Container Tracker..."
echo "📍 Puerto: Chancay, Perú"
echo "🤖 IA: OpenAI GPT-4o mini integrado"
echo "⚡ Framework: FastAPI (Moderno y Rápido)"
echo "🏗️ Arquitectura: Hexagonal"
echo "🌐 Corredor: Perú-Asia"
echo
echo "🌐 Dashboard disponible en: http://localhost:5000"
echo "📖 Documentación API: http://localhost:5000/docs"
echo

python app_fastapi.py
