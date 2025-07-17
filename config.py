"""
Configuración del Sistema Puerto de Chancay
Arquitectura Hexagonal con integración OpenAI GPT-4o mini
"""

import os

# Configuración OpenAI
# IMPORTANTE: En producción usar variables de entorno
# Para desarrollo local, configura tu API key como variable de entorno:
# export OPENAI_API_KEY="tu-api-key-aqui"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
if OPENAI_API_KEY == "your-openai-api-key-here":
    print("⚠️ ADVERTENCIA: Configura tu OPENAI_API_KEY como variable de entorno")
    print("💡 Ejemplo: export OPENAI_API_KEY='tu-api-key'")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Configuración del Puerto de Chancay
PUERTO_CONFIG = {
    "nombre": "Puerto de Chancay",
    "pais": "Perú",
    "ubicacion": {"lat": -11.5664, "lng": -77.2689},
    "capacidad_anual": "1_000_000 TEU",
    "profundidad": "17.8 metros",
    "gruas_disponibles": 12,
    "muelles": 4,
}

# Rutas principales Perú-Asia
RUTAS_COMERCIALES = {
    "Shanghai": {"tiempo_navegacion": 23, "distancia_nm": 10420},
    "Qingdao": {"tiempo_navegacion": 25, "distancia_nm": 11200},
    "Ningbo": {"tiempo_navegacion": 24, "distancia_nm": 10800},
    "Busan": {"tiempo_navegacion": 26, "distancia_nm": 11500},
    "Yokohama": {"tiempo_navegacion": 22, "distancia_nm": 10100},
}

# Tipos de carga típicos Perú-Asia
TIPOS_CARGA_PERU = [
    "Cobre",
    "Zinc",
    "Plomo",
    "Oro",
    "Plata",  # Minerales
    "Harina de pescado",
    "Palta",
    "Uvas",
    "Espárragos",
    "Quinoa",  # Agro
    "Textiles",
    "Manufacturas",
    "Productos químicos",  # Industria
]

# Configuración Flask
FLASK_CONFIG = {"host": "0.0.0.0", "port": 5000, "debug": True}

# Configuración de datos
DATA_PATH = "data/"
CONTAINERS_FILE = "containers_chancay.csv"
SHIPS_FILE = "ships_chancay.csv"
