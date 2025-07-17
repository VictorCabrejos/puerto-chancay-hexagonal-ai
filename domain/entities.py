"""
Domain Layer - Entidades del Puerto de Chancay
Arquitectura Hexagonal
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List


class ContainerStatus(Enum):
    EN_TRANSITO = "en_transito"
    LLEGANDO = "llegando"
    ATRACADO = "atracado"
    DESCARGANDO = "descargando"
    COMPLETADO = "completado"
    PROBLEMA = "problema"


class TipoCarga(Enum):
    MINERALES = "minerales"
    AGRICOLA = "agricola"
    MANUFACTURA = "manufactura"
    TEXTILES = "textiles"
    QUIMICOS = "quimicos"
    GENERAL = "general"


class Prioridad(Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


@dataclass
class Container:
    """Entidad Container - Núcleo del dominio"""

    container_id: str
    ship_name: str
    origin_port: str
    destination_port: str
    cargo_type: TipoCarga
    weight_kg: float
    status: ContainerStatus
    eta: datetime
    priority: Prioridad
    progress_percent: int = 0
    crane_assigned: Optional[str] = None
    temperature_controlled: bool = False
    customs_cleared: bool = False

    def __post_init__(self):
        """Validaciones de negocio"""
        if self.weight_kg <= 0:
            raise ValueError("El peso debe ser positivo")
        if not (0 <= self.progress_percent <= 100):
            raise ValueError("El progreso debe estar entre 0 y 100")

    def assign_crane(self, crane_id: str) -> None:
        """Asignar grúa para descarga"""
        if self.status != ContainerStatus.ATRACADO:
            raise ValueError("Solo se puede asignar grúa a contenedores atracados")
        self.crane_assigned = crane_id
        self.status = ContainerStatus.DESCARGANDO

    def update_progress(self, progress: int) -> None:
        """Actualizar progreso de descarga"""
        if not (0 <= progress <= 100):
            raise ValueError("Progreso inválido")
        self.progress_percent = progress
        if progress == 100:
            self.status = ContainerStatus.COMPLETADO

    def is_priority_cargo(self) -> bool:
        """Verificar si es carga prioritaria"""
        return self.priority in [Prioridad.ALTA, Prioridad.CRITICA]

    def get_estimated_unload_time(self) -> int:
        """Estimar tiempo de descarga en horas"""
        base_time = 2  # horas base
        if self.cargo_type == TipoCarga.MINERALES:
            base_time = 4
        elif self.cargo_type == TipoCarga.QUIMICOS:
            base_time = 6

        # Ajuste por peso
        weight_factor = min(self.weight_kg / 20000, 2.0)
        return int(base_time * weight_factor)


@dataclass
class Ship:
    """Entidad Ship - Embarcación"""

    ship_id: str
    name: str
    captain: str
    origin_port: str
    containers_count: int
    max_capacity: int
    current_status: str
    eta_chancay: datetime

    def __post_init__(self):
        if self.containers_count > self.max_capacity:
            raise ValueError("Contenedores exceden capacidad")

    def get_load_percentage(self) -> float:
        """Porcentaje de carga del barco"""
        return (self.containers_count / self.max_capacity) * 100

    def is_overloaded(self) -> bool:
        """Verificar sobrecarga"""
        return self.containers_count > self.max_capacity * 0.95


@dataclass
class PortOperation:
    """Entidad PortOperation - Operación portuaria"""

    operation_id: str
    container_id: str
    operation_type: str  # "descarga", "carga", "inspeccion"
    start_time: datetime
    estimated_end_time: datetime
    actual_end_time: Optional[datetime] = None
    crane_id: Optional[str] = None
    operator_id: str = ""
    notes: str = ""

    def is_completed(self) -> bool:
        """Verificar si la operación está completada"""
        return self.actual_end_time is not None

    def get_duration_hours(self) -> Optional[float]:
        """Obtener duración en horas"""
        if self.actual_end_time:
            duration = self.actual_end_time - self.start_time
            return duration.total_seconds() / 3600
        return None


@dataclass
class AIInsight:
    """Entidad AIInsight - Insights generados por IA"""

    insight_id: str
    type: str  # "prediccion", "recomendacion", "alerta"
    title: str
    description: str
    confidence: float
    impact_level: str  # "bajo", "medio", "alto"
    generated_at: datetime
    related_containers: List[str]

    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("La confianza debe estar entre 0 y 1")

    def is_high_confidence(self) -> bool:
        """Verificar si es un insight de alta confianza"""
        return self.confidence >= 0.8
