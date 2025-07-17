"""
Domain Layer - Services
Arquitectura Hexagonal - Puerto de Chancay
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from .entities import (
    Container,
    Ship,
    PortOperation,
    AIInsight,
    ContainerStatus,
    Prioridad,
)
from .ports import (
    ContainerRepositoryPort,
    ShipTrackingPort,
    AIAnalyticsPort,
    NotificationPort,
    PortOperationsPort,
    DataAnalyticsPort,
)


class ContainerTrackingService:
    """Servicio principal para tracking de contenedores"""

    def __init__(
        self,
        container_repo: ContainerRepositoryPort,
        ship_tracking: ShipTrackingPort,
        ai_analytics: AIAnalyticsPort,
        notifications: NotificationPort,
        operations: PortOperationsPort,
    ):
        self.container_repo = container_repo
        self.ship_tracking = ship_tracking
        self.ai_analytics = ai_analytics
        self.notifications = notifications
        self.operations = operations

    def process_arriving_container(self, container: Container) -> bool:
        """Procesar llegada de contenedor"""
        try:
            # Actualizar estado
            container.status = ContainerStatus.LLEGANDO
            self.container_repo.update_container(container)

            # Generar recomendación de grúa con IA
            containers_waiting = self.container_repo.get_containers_by_status(
                "atracado"
            )
            crane_recommendation = self.ai_analytics.recommend_crane_allocation(
                containers_waiting + [container]
            )

            # Notificar
            self.notifications.send_status_update(container.container_id, "llegando")
            if crane_recommendation.is_high_confidence():
                self.notifications.send_ai_insight(crane_recommendation)

            return True
        except Exception as e:
            print(f"Error procesando llegada: {e}")
            return False

    def dock_container(self, container_id: str) -> bool:
        """Atracar contenedor"""
        container = self.container_repo.get_container_by_id(container_id)
        if not container:
            return False

        container.status = ContainerStatus.ATRACADO
        return self.container_repo.update_container(container)

    def assign_crane_intelligently(self, container_id: str) -> bool:
        """Asignar grúa usando IA"""
        container = self.container_repo.get_container_by_id(container_id)
        if not container:
            return False

        # Obtener recomendación de IA
        crane_assignments = self.operations.get_crane_assignments()
        containers_waiting = self.container_repo.get_containers_by_status("atracado")

        recommendation = self.ai_analytics.recommend_crane_allocation(
            containers_waiting
        )

        # Asignar grúa disponible
        available_cranes = self._get_available_cranes(crane_assignments)
        if available_cranes:
            crane_id = available_cranes[0]
            container.assign_crane(crane_id)
            self.container_repo.update_container(container)
            self.operations.assign_crane(container_id, crane_id)
            return True

        return False

    def update_unloading_progress(self, container_id: str, progress: int) -> bool:
        """Actualizar progreso de descarga"""
        container = self.container_repo.get_container_by_id(container_id)
        if not container:
            return False

        container.update_progress(progress)
        self.container_repo.update_container(container)

        if progress == 100:
            self.notifications.send_status_update(container_id, "completado")

        return True

    def get_priority_containers(self) -> List[Container]:
        """Obtener contenedores prioritarios"""
        all_containers = self.container_repo.get_all_containers()
        return [c for c in all_containers if c.is_priority_cargo()]

    def _get_available_cranes(self, assignments: Dict[str, List[str]]) -> List[str]:
        """Obtener grúas disponibles"""
        all_cranes = [f"Grua-{i+1:02d}" for i in range(12)]  # 12 grúas en Chancay
        busy_cranes = []
        for crane_containers in assignments.values():
            if crane_containers:  # Si tiene contenedores asignados
                busy_cranes.append(crane_containers[0])

        return [crane for crane in all_cranes if crane not in busy_cranes]


class AIAnalyticsService:
    """Servicio de análisis con IA"""

    def __init__(self, ai_port: AIAnalyticsPort, data_analytics: DataAnalyticsPort):
        self.ai_port = ai_port
        self.data_analytics = data_analytics

    def generate_daily_insights(self) -> List[AIInsight]:
        """Generar insights diarios"""
        insights = []

        # Análisis de congestión
        port_data = self.data_analytics.get_port_overview()
        congestion_insight = self.ai_port.predict_port_congestion(port_data)
        insights.append(congestion_insight)

        # Análisis de patrones de carga
        containers = []  # Se obtendría del repositorio
        cargo_patterns = self.ai_port.analyze_cargo_patterns(containers)
        insights.append(cargo_patterns)

        return insights

    def analyze_peru_asia_trade(self) -> AIInsight:
        """Analizar comercio Perú-Asia"""
        route_data = self.data_analytics.get_route_analytics()
        cargo_stats = self.data_analytics.get_cargo_statistics()

        # Combinar datos para análisis completo
        combined_data = {**route_data, **cargo_stats}

        return AIInsight(
            insight_id=f"trade_analysis_{datetime.now().strftime('%Y%m%d')}",
            type="analisis",
            title="Análisis Comercio Perú-Asia",
            description="Análisis de patrones comerciales en el corredor Perú-Asia",
            confidence=0.85,
            impact_level="alto",
            generated_at=datetime.now(),
            related_containers=[],
        )


class PortEfficiencyService:
    """Servicio de eficiencia portuaria"""

    def __init__(
        self,
        operations_port: PortOperationsPort,
        data_analytics: DataAnalyticsPort,
        ai_analytics: AIAnalyticsPort,
    ):
        self.operations = operations_port
        self.data_analytics = data_analytics
        self.ai_analytics = ai_analytics

    def calculate_daily_efficiency(self) -> Dict[str, float]:
        """Calcular eficiencia diaria"""
        metrics = self.data_analytics.get_performance_metrics()

        # Métricas específicas del Puerto de Chancay
        efficiency_metrics = {
            "containers_per_hour": metrics.get("containers_processed", 0) / 24,
            "crane_utilization": metrics.get("crane_usage", 0) / 12,  # 12 grúas
            "berth_occupancy": metrics.get("berth_usage", 0) / 4,  # 4 muelles
            "turnaround_time": metrics.get("avg_turnaround", 48),  # horas
            "overall_efficiency": 0.0,
        }

        # Cálculo de eficiencia general
        efficiency_metrics["overall_efficiency"] = (
            efficiency_metrics["containers_per_hour"] * 0.3
            + efficiency_metrics["crane_utilization"] * 0.3
            + efficiency_metrics["berth_occupancy"] * 0.2
            + (1.0 / max(efficiency_metrics["turnaround_time"] / 24, 0.1)) * 0.2
        )

        return efficiency_metrics

    def optimize_operations(self) -> List[AIInsight]:
        """Optimizar operaciones usando IA"""
        active_operations = self.operations.get_active_operations()
        efficiency_insights = self.ai_analytics.generate_efficiency_insights(
            active_operations
        )

        return [efficiency_insights]
