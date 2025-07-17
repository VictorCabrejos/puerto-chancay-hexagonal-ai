@echo off
REM 🚢 Puerto de Chancay - Setup Script for Windows
REM Script de configuración automática para Windows

echo 🚢 Puerto de Chancay - Sistema de Gestión Inteligente
echo ==================================================
echo.

REM Verificar Python
echo 🔍 Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado. Por favor instala Python 3.11+
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('python --version') do set PYTHON_VERSION=%%v
echo ✅ Python %PYTHON_VERSION% encontrado

REM Verificar entorno virtual
if defined VIRTUAL_ENV (
    echo ✅ Entorno virtual activo: %VIRTUAL_ENV%
) else (
    echo ⚠️ No se detectó entorno virtual activo
    echo 💡 Recomendamos usar: conda create -n chancay_env python=3.11
    echo.
    set /p continue="¿Continuar sin entorno virtual? (y/N): "
    if /i not "%continue%"=="y" (
        echo 👋 Setup cancelado. Activa tu entorno virtual primero.
        pause
        exit /b 1
    )
)

REM Instalar dependencias
echo.
echo 📦 Instalando dependencias...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas correctamente

REM Verificar OpenAI API Key
echo.
echo 🤖 Verificando configuración de OpenAI...

if "%OPENAI_API_KEY%"=="" (
    echo ⚠️ Variable OPENAI_API_KEY no encontrada
    echo.
    echo Opciones para configurar:
    echo 1. set OPENAI_API_KEY=tu-api-key
    echo 2. Crear archivo .env con OPENAI_API_KEY=tu-api-key
    echo 3. Editar config.py directamente
    echo.
    echo 💡 Obtén tu API key en: https://platform.openai.com/api-keys
) else (
    echo ✅ OPENAI_API_KEY configurada
)

REM Verificar estructura del proyecto
echo.
echo 📁 Verificando estructura del proyecto...

if exist "domain\" (echo ✅ domain\) else (echo ❌ domain\ - Directorio faltante)
if exist "adapters\" (echo ✅ adapters\) else (echo ❌ adapters\ - Directorio faltante)
if exist "api\" (echo ✅ api\) else (echo ❌ api\ - Directorio faltante)
if exist "templates\" (echo ✅ templates\) else (echo ❌ templates\ - Directorio faltante)
if exist "data\" (echo ✅ data\) else (echo ❌ data\ - Directorio faltante)

if exist "app.py" (echo ✅ app.py) else (echo ❌ app.py - Archivo faltante)
if exist "config.py" (echo ✅ config.py) else (echo ❌ config.py - Archivo faltante)
if exist "requirements.txt" (echo ✅ requirements.txt) else (echo ❌ requirements.txt - Archivo faltante)

echo.
echo 🚀 Setup completado!
echo.
echo Para ejecutar el sistema:
echo   uvicorn app:app --host 0.0.0.0 --port 5000 --reload
echo.
echo URLs importantes:
echo   🏠 Landing Page: http://localhost:5000/landing
echo   📊 Dashboard:    http://localhost:5000
echo   📚 API Docs:     http://localhost:5000/docs
echo.
echo 🎯 ¡Listo para demostrar Arquitectura Hexagonal + IA!
echo.
pause
