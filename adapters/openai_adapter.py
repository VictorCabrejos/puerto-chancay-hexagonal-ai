"""
Adapter - OpenAI GPT-4o mini Integration
Arquitectura Hexagonal - Puerto de Chancay
"""

import openai
import os
import json
from typing import List, Dict, Any
from datetime import datetime
from domain.ports import AIAnalyticsPort
from domain.entities import Container, PortOperation, AIInsight


class OpenAIAnalyticsAdapter(AIAnalyticsPort):
    """Adaptador para análisis con OpenAI GPT-4o mini"""

    def __init__(self):
        # Obtener API key del environment o config
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            # Fallback a config.py
            try:
                from config import OPENAI_API_KEY

                api_key = OPENAI_API_KEY
                os.environ["OPENAI_API_KEY"] = api_key
            except ImportError:
                raise ValueError(
                    "OPENAI_API_KEY no configurada en environment ni en config.py"
                )

        # Crear cliente OpenAI con la nueva sintaxis
        self.client = openai.OpenAI(api_key=api_key)

    def predict_port_congestion(self, current_data: Dict[str, Any]) -> AIInsight:
        """Predecir congestión portuaria usando GPT-4o mini"""

        prompt = f"""
        Eres un experto en operaciones portuarias del Puerto de Chancay, Perú.

        Datos actuales del puerto:
        - Contenedores totales: {current_data.get('total_containers', 0)}
        - Barcos en puerto: {current_data.get('ships_count', 0)}
        - Grúas activas: {current_data.get('active_cranes', 0)}/12
        - Muelles ocupados: {current_data.get('occupied_berths', 0)}/4
        - Contenedores descargando: {current_data.get('unloading_containers', 0)}

        Analiza estos datos y predice si habrá congestión en las próximas 6-12 horas.
        Considera que Chancay es un puerto estratégico para el comercio Perú-Asia.

        Responde en formato JSON:
        {{
            "prediction": "baja/media/alta congestión",
            "confidence": 0.0-1.0,
            "reasoning": "explicación detallada",
            "recommendations": ["recomendación 1", "recomendación 2"],
            "impact": "bajo/medio/alto"
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en análisis portuario y logística del Puerto de Chancay.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )

            result = json.loads(response.choices[0].message.content)

            return AIInsight(
                insight_id=f"congestion_pred_{datetime.now().strftime('%Y%m%d_%H%M')}",
                type="prediccion",
                title=f"Predicción de Congestión: {result['prediction']}",
                description=f"{result['reasoning']} Recomendaciones: {', '.join(result['recommendations'])}",
                confidence=result["confidence"],
                impact_level=result["impact"],
                generated_at=datetime.now(),
                related_containers=[],
            )

        except Exception as e:
            return self._create_fallback_insight(
                "congestion", f"Error en predicción: {e}"
            )

    def recommend_crane_allocation(self, containers: List[Container]) -> AIInsight:
        """Recomendar asignación de grúas"""

        container_data = []
        for c in containers:
            container_data.append(
                {
                    "id": c.container_id,
                    "cargo": c.cargo_type.value,
                    "weight": c.weight_kg,
                    "priority": c.priority.value,
                    "status": c.status.value,
                }
            )

        prompt = f"""
        Eres un experto en operaciones de grúas del Puerto de Chancay.
        El puerto tiene 12 grúas disponibles para asignación.

        Contenedores esperando asignación:
        {json.dumps(container_data, indent=2)}

        Considera:
        - Prioridad de carga (crítica > alta > media > baja)
        - Tipo de carga (minerales requieren más tiempo)
        - Peso del contenedor
        - Eficiencia operativa del puerto

        Genera recomendaciones para optimizar la asignación de grúas.

        Responde en JSON:
        {{
            "priority_order": ["container_id1", "container_id2", ...],
            "crane_assignments": {{"container_id": "grua_number"}},
            "reasoning": "explicación de la estrategia",
            "estimated_efficiency": 0.0-1.0,
            "recommendations": ["recomendación 1", "recomendación 2"]
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en optimización de operaciones portuarias.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )

            result = json.loads(response.choices[0].message.content)

            return AIInsight(
                insight_id=f"crane_alloc_{datetime.now().strftime('%Y%m%d_%H%M')}",
                type="recomendacion",
                title=f"Optimización de Grúas (Eficiencia: {result['estimated_efficiency']:.0%})",
                description=f"{result['reasoning']} Recomendaciones: {', '.join(result['recommendations'])}",
                confidence=result["estimated_efficiency"],
                impact_level=(
                    "medio" if result["estimated_efficiency"] > 0.7 else "bajo"
                ),
                generated_at=datetime.now(),
                related_containers=result["priority_order"][:3],
            )

        except Exception as e:
            return self._create_fallback_insight(
                "crane_allocation", f"Error en recomendación: {e}"
            )

    def analyze_cargo_patterns(self, containers: List[Container]) -> AIInsight:
        """Analizar patrones de carga Perú-Asia"""

        cargo_summary = {}
        for container in containers:
            cargo_type = container.cargo_type.value
            cargo_summary[cargo_type] = cargo_summary.get(cargo_type, 0) + 1

        prompt = f"""
        Eres un experto en comercio internacional Perú-Asia y análisis del Puerto de Chancay.

        Patrones de carga actuales:
        {json.dumps(cargo_summary, indent=2)}

        Analiza estos patrones considerando:
        - El Puerto de Chancay como hub estratégico Perú-Asia
        - Principales exportaciones peruanas (minerales, productos agrícolas)
        - Tendencias del comercio bilateral
        - Estacionalidad de productos

        Responde en JSON:
        {{
            "trends": ["tendencia 1", "tendencia 2"],
            "insights": "análisis detallado",
            "predictions": "predicciones futuras",
            "opportunities": ["oportunidad 1", "oportunidad 2"],
            "impact_score": 0.0-1.0
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en análisis de comercio internacional Perú-Asia.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
            )

            result = json.loads(response.choices[0].message.content)

            return AIInsight(
                insight_id=f"cargo_patterns_{datetime.now().strftime('%Y%m%d')}",
                type="analisis",
                title="Análisis Patrones Comercio Perú-Asia",
                description=f"{result['insights']} Oportunidades: {', '.join(result['opportunities'])}",
                confidence=result["impact_score"],
                impact_level="alto" if result["impact_score"] > 0.7 else "medio",
                generated_at=datetime.now(),
                related_containers=[],
            )

        except Exception as e:
            return self._create_fallback_insight(
                "cargo_patterns", f"Error en análisis: {e}"
            )

    def generate_efficiency_insights(
        self, operations: List[PortOperation]
    ) -> AIInsight:
        """Generar insights de eficiencia"""

        ops_data = []
        for op in operations:
            duration = op.get_duration_hours()
            ops_data.append(
                {
                    "type": op.operation_type,
                    "duration_hours": duration,
                    "crane": op.crane_id,
                    "completed": op.is_completed(),
                }
            )

        prompt = f"""
        Eres un experto en eficiencia operativa del Puerto de Chancay.

        Operaciones recientes:
        {json.dumps(ops_data, indent=2)}

        Analiza la eficiencia operativa y genera insights para mejorar:
        - Tiempos de operación
        - Utilización de grúas
        - Cuellos de botella
        - Oportunidades de mejora

        Responde en JSON:
        {{
            "efficiency_score": 0.0-1.0,
            "bottlenecks": ["cuello 1", "cuello 2"],
            "improvements": ["mejora 1", "mejora 2"],
            "analysis": "análisis detallado",
            "priority": "baja/media/alta"
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en optimización de eficiencia portuaria.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )

            result = json.loads(response.choices[0].message.content)

            return AIInsight(
                insight_id=f"efficiency_{datetime.now().strftime('%Y%m%d')}",
                type="recomendacion",
                title=f"Eficiencia Operativa ({result['efficiency_score']:.0%})",
                description=f"{result['analysis']} Mejoras: {', '.join(result['improvements'])}",
                confidence=result["efficiency_score"],
                impact_level=result["priority"],
                generated_at=datetime.now(),
                related_containers=[],
            )

        except Exception as e:
            return self._create_fallback_insight(
                "efficiency", f"Error en análisis: {e}"
            )

    def predict_delays(self, ship, weather_data: Dict) -> AIInsight:
        """Predecir demoras potenciales"""
        return self._create_fallback_insight(
            "delays", "Predicción de demoras no implementada"
        )

    def _create_fallback_insight(self, insight_type: str, message: str) -> AIInsight:
        """Crear insight de respaldo en caso de error"""
        return AIInsight(
            insight_id=f"fallback_{insight_type}_{datetime.now().strftime('%Y%m%d_%H%M')}",
            type="error",
            title=f"Análisis {insight_type} - Modo Básico",
            description=f"Sistema funcionando en modo básico: {message}",
            confidence=0.5,
            impact_level="bajo",
            generated_at=datetime.now(),
            related_containers=[],
        )
