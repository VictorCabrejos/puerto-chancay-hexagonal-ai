"""
Application Layer - FastAPI Web Application
Puerto de Chancay Container Tracker
Arquitectura Hexagonal + GPT-4o mini
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
import os
from typing import Dict, Any, List

# Imports del dominio
from domain.services import (
    ContainerTrackingService,
    AIAnalyticsService,
    PortEfficiencyService,
)
from adapters.data_adapter import CSVDataAdapter
from adapters.openai_adapter import OpenAIAnalyticsAdapter

# Configuración
from config import FLASK_CONFIG, PUERTO_CONFIG

# Crear aplicación FastAPI
app = FastAPI(
    title="Puerto de Chancay Container Tracker",
    description="Sistema de tracking inteligente con Arquitectura Hexagonal + GPT-4o mini",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar templates
templates = Jinja2Templates(directory="templates")


# Modelos Pydantic para requests
class ContainerProgressUpdate(BaseModel):
    progress: int


class CraneAssignment(BaseModel):
    container_id: str


# Configuración de dependencias (Inyección de Dependencias)
def setup_dependencies():
    """Configurar dependencias del sistema"""
    # Adaptadores
    data_adapter = CSVDataAdapter()
    ai_adapter = OpenAIAnalyticsAdapter()

    # Servicios del dominio
    container_service = ContainerTrackingService(
        container_repo=data_adapter,
        ship_tracking=data_adapter,
        ai_analytics=ai_adapter,
        notifications=None,  # Implementar si es necesario
        operations=None,  # Implementar si es necesario
    )

    ai_service = AIAnalyticsService(ai_port=ai_adapter, data_analytics=data_adapter)

    efficiency_service = PortEfficiencyService(
        operations_port=None,  # Implementar si es necesario
        data_analytics=data_adapter,
        ai_analytics=ai_adapter,
    )

    return {
        "container_service": container_service,
        "ai_service": ai_service,
        "efficiency_service": efficiency_service,
        "data_adapter": data_adapter,
        "ai_adapter": ai_adapter,
    }


# Configurar servicios
services = setup_dependencies()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Página principal del dashboard"""
    return templates.TemplateResponse(
        "index.html", {"request": request, "puerto_info": PUERTO_CONFIG}
    )


@app.get("/landing", response_class=HTMLResponse)
async def landing(request: Request):
    """Página de presentación y explicación del sistema"""
    return templates.TemplateResponse(
        "landing.html", {"request": request, "puerto_info": PUERTO_CONFIG}
    )


@app.get("/api/overview")
async def get_overview() -> Dict[str, Any]:
    """API: Resumen general del puerto"""
    try:
        data_adapter = services["data_adapter"]
        overview = data_adapter.get_port_overview()

        # Agregar información específica de Chancay
        overview.update(
            {
                "puerto_nombre": PUERTO_CONFIG["nombre"],
                "pais": PUERTO_CONFIG["pais"],
                "gruas_totales": PUERTO_CONFIG["gruas_disponibles"],
                "muelles_totales": 4,
                "capacidad_anual": PUERTO_CONFIG["capacidad_anual"],
            }
        )

        return overview
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/containers")
async def get_containers() -> List[Dict[str, Any]]:
    """API: Lista de contenedores"""
    try:
        data_adapter = services["data_adapter"]
        containers = data_adapter.get_all_containers()

        # Convertir a formato JSON
        containers_data = []
        for container in containers:
            containers_data.append(
                {
                    "container_id": container.container_id,
                    "ship_name": container.ship_name,
                    "origin_port": container.origin_port,
                    "destination_port": container.destination_port,
                    "cargo_type": container.cargo_type.value,
                    "weight_kg": container.weight_kg,
                    "status": container.status.value,
                    "eta": container.eta.strftime("%Y-%m-%d %H:%M"),
                    "priority": container.priority.value,
                    "progress_percent": container.progress_percent,
                    "crane_assigned": container.crane_assigned,
                    "temperature_controlled": container.temperature_controlled,
                    "customs_cleared": container.customs_cleared,
                }
            )

        return containers_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ships")
async def get_ships() -> List[Dict[str, Any]]:
    """API: Lista de embarcaciones"""
    try:
        data_adapter = services["data_adapter"]
        ships = data_adapter.get_all_ships()

        ships_data = []
        for ship in ships:
            ships_data.append(
                {
                    "ship_id": ship.ship_id,
                    "name": ship.name,
                    "captain": ship.captain,
                    "origin_port": ship.origin_port,
                    "containers_count": ship.containers_count,
                    "max_capacity": ship.max_capacity,
                    "current_status": ship.current_status,
                    "eta_chancay": ship.eta_chancay.strftime("%Y-%m-%d %H:%M"),
                    "load_percentage": ship.get_load_percentage(),
                }
            )

        return ships_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ai-insights")
async def get_ai_insights() -> List[Dict[str, Any]]:
    """API: Insights generados por IA (GPT-4o mini)"""
    try:
        ai_service = services["ai_service"]
        data_adapter = services["data_adapter"]

        # Generar insights en tiempo real
        insights = []

        # 1. Análisis de congestión
        port_data = data_adapter.get_port_overview()
        congestion_insight = services["ai_adapter"].predict_port_congestion(port_data)
        insights.append(
            {
                "id": congestion_insight.insight_id,
                "type": congestion_insight.type,
                "title": congestion_insight.title,
                "description": congestion_insight.description,
                "confidence": congestion_insight.confidence,
                "impact_level": congestion_insight.impact_level,
                "generated_at": congestion_insight.generated_at.strftime(
                    "%Y-%m-%d %H:%M"
                ),
            }
        )

        # 2. Análisis de patrones de carga
        containers = data_adapter.get_all_containers()
        cargo_insight = services["ai_adapter"].analyze_cargo_patterns(containers)
        insights.append(
            {
                "id": cargo_insight.insight_id,
                "type": cargo_insight.type,
                "title": cargo_insight.title,
                "description": cargo_insight.description,
                "confidence": cargo_insight.confidence,
                "impact_level": cargo_insight.impact_level,
                "generated_at": cargo_insight.generated_at.strftime("%Y-%m-%d %H:%M"),
            }
        )

        # 3. Recomendaciones de grúas
        waiting_containers = data_adapter.get_containers_by_status("atracado")
        if waiting_containers:
            crane_insight = services["ai_adapter"].recommend_crane_allocation(
                waiting_containers
            )
            insights.append(
                {
                    "id": crane_insight.insight_id,
                    "type": crane_insight.type,
                    "title": crane_insight.title,
                    "description": crane_insight.description,
                    "confidence": crane_insight.confidence,
                    "impact_level": crane_insight.impact_level,
                    "generated_at": crane_insight.generated_at.strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                }
            )

        return insights
    except Exception as e:
        return [{"error": str(e), "insights": []}]


@app.get("/api/analytics/peru-asia")
async def get_peru_asia_analytics() -> Dict[str, Any]:
    """API: Análisis específico del corredor Perú-Asia"""
    try:
        data_adapter = services["data_adapter"]

        # Datos del corredor comercial
        route_analytics = data_adapter.get_route_analytics()
        cargo_stats = data_adapter.get_cargo_statistics()

        peru_asia_data = {
            "corredor": "Perú-Asia",
            "puerto_estrategico": "Chancay",
            "rutas_activas": route_analytics["active_routes"],
            "principales_corredores": route_analytics["main_corridors"],
            "tiempos_transito": route_analytics["avg_transit_times"],
            "tipos_carga": cargo_stats["cargo_breakdown"],
            "exportaciones_peru": cargo_stats["peru_exports"],
            "importaciones_asia": cargo_stats["asia_imports"],
            "impacto_economico": {
                "conectividad": "Mejora significativa en conectividad América Latina-Asia",
                "tiempo_reducido": "Reducción de 7-10 días en tránsito vs rutas tradicionales",
                "capacidad": "1 millón TEU anuales",
                "beneficios": [
                    "Reducción de costos logísticos",
                    "Mejora en competitividad exportadora",
                    "Hub estratégico para América Latina",
                    "Impulso al comercio bilateral Perú-Asia",
                ],
            },
        }

        return peru_asia_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/efficiency")
async def get_efficiency_metrics() -> Dict[str, Any]:
    """API: Métricas de eficiencia del puerto"""
    try:
        efficiency_service = services["efficiency_service"]
        data_adapter = services["data_adapter"]

        # Calcular métricas de eficiencia
        efficiency_metrics = efficiency_service.calculate_daily_efficiency()
        performance_metrics = data_adapter.get_performance_metrics()

        efficiency_data = {
            "eficiencia_general": efficiency_metrics["overall_efficiency"],
            "contenedores_por_hora": efficiency_metrics["containers_per_hour"],
            "utilizacion_gruas": efficiency_metrics["crane_utilization"],
            "ocupacion_muelles": efficiency_metrics["berth_occupancy"],
            "tiempo_rotacion": efficiency_metrics["turnaround_time"],
            "metricas_detalladas": performance_metrics,
            "comparacion_mundial": {
                "top_10_mundial": False,
                "posicion_latam": 1,
                "eficiencia_vs_promedio": "+15%",
            },
        }

        return efficiency_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/container/{container_id}/update")
async def update_container_progress(
    container_id: str, update_data: ContainerProgressUpdate
):
    """API: Actualizar progreso de contenedor"""
    try:
        container_service = services["container_service"]
        success = container_service.update_unloading_progress(
            container_id, update_data.progress
        )

        if success:
            return {"success": True, "message": "Progreso actualizado"}
        else:
            raise HTTPException(status_code=404, detail="Contenedor no encontrado")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/crane/assign")
async def assign_crane(assignment_data: CraneAssignment):
    """API: Asignar grúa inteligentemente"""
    try:
        container_service = services["container_service"]
        success = container_service.assign_crane_intelligently(
            assignment_data.container_id
        )

        if success:
            return {"success": True, "message": "Grúa asignada exitosamente"}
        else:
            raise HTTPException(status_code=400, detail="No se pudo asignar grúa")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/status")
async def get_system_status() -> Dict[str, Any]:
    """API: Estado del sistema"""
    try:
        return {
            "sistema": "Puerto de Chancay - Container Tracker",
            "version": "1.0.0",
            "framework": "FastAPI",
            "arquitectura": "Hexagonal",
            "ia_integrada": "OpenAI GPT-4o mini",
            "estado": "operativo",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "servicios": {
                "container_tracking": "activo",
                "ai_analytics": "activo",
                "data_management": "activo",
                "efficiency_monitoring": "activo",
            },
            "documentacion": {"swagger_ui": "/docs", "redoc": "/redoc"},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Event handlers
@app.on_event("startup")
async def startup_event():
    """Configuración inicial al arrancar"""
    # Asegurar que las carpetas existen
    os.makedirs("data", exist_ok=True)
    os.makedirs("templates", exist_ok=True)

    print("🚢 Iniciando Puerto de Chancay Container Tracker...")
    print(f"📍 Puerto: {PUERTO_CONFIG['nombre']}, {PUERTO_CONFIG['pais']}")
    print(f"🤖 IA: OpenAI GPT-4o mini integrado")
    print(f"🏗️ Arquitectura: Hexagonal")
    print(f"🌐 Corredor: Perú-Asia")
    print(f"⚡ Framework: FastAPI")
    print(f"📖 Documentación: http://localhost:{FLASK_CONFIG['port']}/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=FLASK_CONFIG["host"],
        port=FLASK_CONFIG["port"],
        reload=FLASK_CONFIG["debug"],
        log_level="info",
    )
