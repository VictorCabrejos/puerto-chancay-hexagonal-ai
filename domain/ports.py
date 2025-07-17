"""
Domain Layer - Ports (Interfaces)
Arquitectura Hexagonal - Puerto de Chancay
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
from .entities import Container, Ship, PortOperation, AIInsight


class ContainerRepositoryPort(ABC):
    """Puerto para gestión de contenedores"""

    @abstractmethod
    def get_all_containers(self) -> List[Container]:
        """Obtener todos los contenedores"""
        pass

    @abstractmethod
    def get_container_by_id(self, container_id: str) -> Optional[Container]:
        """Obtener contenedor por ID"""
        pass

    @abstractmethod
    def get_containers_by_status(self, status: str) -> List[Container]:
        """Obtener contenedores por estado"""
        pass

    @abstractmethod
    def update_container(self, container: Container) -> bool:
        """Actualizar contenedor"""
        pass

    @abstractmethod
    def add_container(self, container: Container) -> bool:
        """Agregar nuevo contenedor"""
        pass


class ShipTrackingPort(ABC):
    """Puerto para seguimiento de embarcaciones"""

    @abstractmethod
    def get_all_ships(self) -> List[Ship]:
        """Obtener todas las embarcaciones"""
        pass

    @abstractmethod
    def get_ship_by_id(self, ship_id: str) -> Optional[Ship]:
        """Obtener embarcación por ID"""
        pass

    @abstractmethod
    def get_arriving_ships(self) -> List[Ship]:
        """Obtener embarcaciones que llegan"""
        pass

    @abstractmethod
    def update_ship_status(self, ship_id: str, status: str) -> bool:
        """Actualizar estado de embarcación"""
        pass


class AIAnalyticsPort(ABC):
    """Puerto para análisis con IA (GPT-4o mini)"""

    @abstractmethod
    def predict_port_congestion(self, current_data: Dict[str, Any]) -> AIInsight:
        """Predecir congestión portuaria"""
        pass

    @abstractmethod
    def recommend_crane_allocation(self, containers: List[Container]) -> AIInsight:
        """Recomendar asignación de grúas"""
        pass

    @abstractmethod
    def analyze_cargo_patterns(self, containers: List[Container]) -> AIInsight:
        """Analizar patrones de carga Perú-Asia"""
        pass

    @abstractmethod
    def generate_efficiency_insights(
        self, operations: List[PortOperation]
    ) -> AIInsight:
        """Generar insights de eficiencia"""
        pass

    @abstractmethod
    def predict_delays(self, ship: Ship, weather_data: Dict) -> AIInsight:
        """Predecir demoras potenciales"""
        pass


class NotificationPort(ABC):
    """Puerto para notificaciones"""

    @abstractmethod
    def send_alert(self, message: str, priority: str, recipients: List[str]) -> bool:
        """Enviar alerta"""
        pass

    @abstractmethod
    def send_status_update(self, container_id: str, status: str) -> bool:
        """Enviar actualización de estado"""
        pass

    @abstractmethod
    def send_ai_insight(self, insight: AIInsight) -> bool:
        """Enviar insight de IA"""
        pass


class PortOperationsPort(ABC):
    """Puerto para operaciones portuarias"""

    @abstractmethod
    def get_active_operations(self) -> List[PortOperation]:
        """Obtener operaciones activas"""
        pass

    @abstractmethod
    def create_operation(self, operation: PortOperation) -> bool:
        """Crear nueva operación"""
        pass

    @abstractmethod
    def complete_operation(self, operation_id: str, end_time: datetime) -> bool:
        """Completar operación"""
        pass

    @abstractmethod
    def get_crane_assignments(self) -> Dict[str, List[str]]:
        """Obtener asignaciones de grúas"""
        pass

    @abstractmethod
    def assign_crane(self, container_id: str, crane_id: str) -> bool:
        """Asignar grúa a contenedor"""
        pass


class DataAnalyticsPort(ABC):
    """Puerto para análisis de datos"""

    @abstractmethod
    def get_port_overview(self) -> Dict[str, Any]:
        """Obtener resumen del puerto"""
        pass

    @abstractmethod
    def get_performance_metrics(self) -> Dict[str, float]:
        """Obtener métricas de rendimiento"""
        pass

    @abstractmethod
    def get_cargo_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas de carga"""
        pass

    @abstractmethod
    def get_route_analytics(self) -> Dict[str, Any]:
        """Obtener análisis de rutas Perú-Asia"""
        pass
