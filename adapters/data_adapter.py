"""
Adapter - Data Management
Arquitectura Hexagonal - Puerto de Chancay
"""

import csv
import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import random
from domain.ports import ContainerRepositoryPort, ShipTrackingPort, DataAnalyticsPort
from domain.entities import Container, Ship, ContainerStatus, TipoCarga, Prioridad


class CSVDataAdapter(ContainerRepositoryPort, ShipTrackingPort, DataAnalyticsPort):
    """Adaptador para gestión de datos en CSV"""

    def __init__(self, data_path: str = "data/"):
        self.data_path = data_path
        self.containers_file = f"{data_path}containers_chancay.csv"
        self.ships_file = f"{data_path}ships_chancay.csv"
        self._initialize_sample_data()

    def _initialize_sample_data(self):
        """Inicializar datos de ejemplo del Puerto de Chancay"""
        # Datos de contenedores de ejemplo
        sample_containers = [
            {
                "container_id": "TCLU-2024-001",
                "ship_name": "Perú Express",
                "origin_port": "Shanghai",
                "destination_port": "Chancay",
                "cargo_type": "minerales",
                "weight_kg": 25000,
                "status": "descargando",
                "eta": "2025-01-17 14:30",
                "priority": "alta",
                "progress_percent": 65,
                "crane_assigned": "Grua-03",
                "temperature_controlled": False,
                "customs_cleared": True,
            },
            {
                "container_id": "TCLU-2024-002",
                "ship_name": "Asia Dream",
                "origin_port": "Qingdao",
                "destination_port": "Chancay",
                "cargo_type": "agricola",
                "weight_kg": 18000,
                "status": "atracado",
                "eta": "2025-01-17 12:00",
                "priority": "media",
                "progress_percent": 0,
                "crane_assigned": None,
                "temperature_controlled": True,
                "customs_cleared": False,
            },
            {
                "container_id": "TCLU-2024-003",
                "ship_name": "Chancay Pioneer",
                "origin_port": "Busan",
                "destination_port": "Chancay",
                "cargo_type": "textiles",
                "weight_kg": 12000,
                "status": "llegando",
                "eta": "2025-01-17 18:45",
                "priority": "baja",
                "progress_percent": 0,
                "crane_assigned": None,
                "temperature_controlled": False,
                "customs_cleared": False,
            },
            {
                "container_id": "TCLU-2024-004",
                "ship_name": "Lima Trader",
                "origin_port": "Ningbo",
                "destination_port": "Chancay",
                "cargo_type": "quimicos",
                "weight_kg": 22000,
                "status": "descargando",
                "eta": "2025-01-17 09:15",
                "priority": "critica",
                "progress_percent": 90,
                "crane_assigned": "Grua-01",
                "temperature_controlled": True,
                "customs_cleared": True,
            },
            {
                "container_id": "TCLU-2024-005",
                "ship_name": "Pacific Bridge",
                "origin_port": "Yokohama",
                "destination_port": "Chancay",
                "cargo_type": "manufactura",
                "weight_kg": 16500,
                "status": "completado",
                "eta": "2025-01-17 06:00",
                "priority": "media",
                "progress_percent": 100,
                "crane_assigned": None,
                "temperature_controlled": False,
                "customs_cleared": True,
            },
        ]

        # Datos de barcos de ejemplo
        sample_ships = [
            {
                "ship_id": "SHIP-001",
                "name": "Perú Express",
                "captain": "Capitán Rodriguez",
                "origin_port": "Shanghai",
                "containers_count": 450,
                "max_capacity": 500,
                "current_status": "atracado",
                "eta_chancay": "2025-01-17 14:30",
            },
            {
                "ship_id": "SHIP-002",
                "name": "Asia Dream",
                "captain": "Captain Chen",
                "origin_port": "Qingdao",
                "containers_count": 380,
                "max_capacity": 400,
                "current_status": "descargando",
                "eta_chancay": "2025-01-17 12:00",
            },
            {
                "ship_id": "SHIP-003",
                "name": "Chancay Pioneer",
                "captain": "Captain Kim",
                "origin_port": "Busan",
                "containers_count": 320,
                "max_capacity": 450,
                "current_status": "llegando",
                "eta_chancay": "2025-01-17 18:45",
            },
        ]

        self._save_sample_data(sample_containers, sample_ships)

    def _save_sample_data(self, containers_data: List[Dict], ships_data: List[Dict]):
        """Guardar datos de ejemplo en archivos CSV"""
        try:
            # Guardar contenedores
            import os

            os.makedirs(self.data_path, exist_ok=True)

            with open(self.containers_file, "w", newline="", encoding="utf-8") as f:
                if containers_data:
                    writer = csv.DictWriter(f, fieldnames=containers_data[0].keys())
                    writer.writeheader()
                    writer.writerows(containers_data)

            # Guardar barcos
            with open(self.ships_file, "w", newline="", encoding="utf-8") as f:
                if ships_data:
                    writer = csv.DictWriter(f, fieldnames=ships_data[0].keys())
                    writer.writeheader()
                    writer.writerows(ships_data)

        except Exception as e:
            print(f"Error guardando datos de ejemplo: {e}")

    # Implementación ContainerRepositoryPort

    def get_all_containers(self) -> List[Container]:
        """Obtener todos los contenedores"""
        containers = []
        try:
            with open(self.containers_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    container = self._dict_to_container(row)
                    if container:
                        containers.append(container)
        except FileNotFoundError:
            print(f"Archivo {self.containers_file} no encontrado")
        except Exception as e:
            print(f"Error leyendo contenedores: {e}")

        return containers

    def get_container_by_id(self, container_id: str) -> Optional[Container]:
        """Obtener contenedor por ID"""
        containers = self.get_all_containers()
        for container in containers:
            if container.container_id == container_id:
                return container
        return None

    def get_containers_by_status(self, status: str) -> List[Container]:
        """Obtener contenedores por estado"""
        containers = self.get_all_containers()
        return [c for c in containers if c.status.value == status]

    def update_container(self, container: Container) -> bool:
        """Actualizar contenedor"""
        containers = self.get_all_containers()
        updated = False

        for i, c in enumerate(containers):
            if c.container_id == container.container_id:
                containers[i] = container
                updated = True
                break

        if updated:
            self._save_containers(containers)

        return updated

    def add_container(self, container: Container) -> bool:
        """Agregar nuevo contenedor"""
        containers = self.get_all_containers()
        containers.append(container)
        self._save_containers(containers)
        return True

    # Implementación ShipTrackingPort

    def get_all_ships(self) -> List[Ship]:
        """Obtener todas las embarcaciones"""
        ships = []
        try:
            with open(self.ships_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ship = self._dict_to_ship(row)
                    if ship:
                        ships.append(ship)
        except FileNotFoundError:
            print(f"Archivo {self.ships_file} no encontrado")
        except Exception as e:
            print(f"Error leyendo barcos: {e}")

        return ships

    def get_ship_by_id(self, ship_id: str) -> Optional[Ship]:
        """Obtener embarcación por ID"""
        ships = self.get_all_ships()
        for ship in ships:
            if ship.ship_id == ship_id:
                return ship
        return None

    def get_arriving_ships(self) -> List[Ship]:
        """Obtener embarcaciones que llegan"""
        ships = self.get_all_ships()
        return [s for s in ships if s.current_status in ["llegando", "atracado"]]

    def update_ship_status(self, ship_id: str, status: str) -> bool:
        """Actualizar estado de embarcación"""
        ships = self.get_all_ships()
        for ship in ships:
            if ship.ship_id == ship_id:
                ship.current_status = status
                self._save_ships(ships)
                return True
        return False

    # Implementación DataAnalyticsPort

    def get_port_overview(self) -> Dict[str, Any]:
        """Obtener resumen del puerto"""
        containers = self.get_all_containers()
        ships = self.get_all_ships()

        status_breakdown = {}
        total_weight = 0
        active_cranes = 0

        for container in containers:
            status = container.status.value
            status_breakdown[status] = status_breakdown.get(status, 0) + 1
            total_weight += container.weight_kg
            if container.crane_assigned:
                active_cranes += 1

        return {
            "total_containers": len(containers),
            "total_weight_kg": total_weight,
            "ships_count": len(ships),
            "status_breakdown": status_breakdown,
            "active_cranes": active_cranes,
            "occupied_berths": len(
                [s for s in ships if s.current_status == "atracado"]
            ),
            "unloading_containers": status_breakdown.get("descargando", 0),
        }

    def get_performance_metrics(self) -> Dict[str, float]:
        """Obtener métricas de rendimiento"""
        containers = self.get_all_containers()
        completed = len(
            [c for c in containers if c.status == ContainerStatus.COMPLETADO]
        )

        return {
            "containers_processed": completed,
            "crane_usage": random.uniform(0.7, 0.95) * 12,  # Simulado
            "berth_usage": random.uniform(0.6, 0.9) * 4,  # Simulado
            "avg_turnaround": random.uniform(36, 48),  # Simulado
        }

    def get_cargo_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas de carga"""
        containers = self.get_all_containers()
        cargo_stats = {}

        for container in containers:
            cargo_type = container.cargo_type.value
            cargo_stats[cargo_type] = cargo_stats.get(cargo_type, 0) + 1

        return {
            "cargo_breakdown": cargo_stats,
            "total_weight_by_type": {},  # Se calcularía según necesidades
            "peru_exports": ["cobre", "zinc", "harina_pescado", "palta"],
            "asia_imports": ["manufactura", "textiles", "quimicos"],
        }

    def get_route_analytics(self) -> Dict[str, Any]:
        """Obtener análisis de rutas Perú-Asia"""
        ships = self.get_all_ships()
        routes = {}

        for ship in ships:
            origin = ship.origin_port
            routes[origin] = routes.get(origin, 0) + 1

        return {
            "active_routes": routes,
            "main_corridors": ["Shanghai-Chancay", "Qingdao-Chancay", "Busan-Chancay"],
            "avg_transit_times": {
                "Shanghai": 23,
                "Qingdao": 25,
                "Busan": 26,
                "Ningbo": 24,
                "Yokohama": 22,
            },
        }

    # Métodos auxiliares

    def _dict_to_container(self, data: Dict) -> Optional[Container]:
        """Convertir diccionario a Container"""
        try:
            return Container(
                container_id=data["container_id"],
                ship_name=data["ship_name"],
                origin_port=data["origin_port"],
                destination_port=data["destination_port"],
                cargo_type=TipoCarga(data["cargo_type"]),
                weight_kg=float(data["weight_kg"]),
                status=ContainerStatus(data["status"]),
                eta=datetime.fromisoformat(data["eta"]),
                priority=Prioridad(data["priority"]),
                progress_percent=int(data["progress_percent"]),
                crane_assigned=(
                    data["crane_assigned"] if data["crane_assigned"] != "None" else None
                ),
                temperature_controlled=data["temperature_controlled"].lower() == "true",
                customs_cleared=data["customs_cleared"].lower() == "true",
            )
        except Exception as e:
            print(f"Error convirtiendo contenedor: {e}")
            return None

    def _dict_to_ship(self, data: Dict) -> Optional[Ship]:
        """Convertir diccionario a Ship"""
        try:
            return Ship(
                ship_id=data["ship_id"],
                name=data["name"],
                captain=data["captain"],
                origin_port=data["origin_port"],
                containers_count=int(data["containers_count"]),
                max_capacity=int(data["max_capacity"]),
                current_status=data["current_status"],
                eta_chancay=datetime.fromisoformat(data["eta_chancay"]),
            )
        except Exception as e:
            print(f"Error convirtiendo barco: {e}")
            return None

    def _save_containers(self, containers: List[Container]):
        """Guardar contenedores en CSV"""
        try:
            with open(self.containers_file, "w", newline="", encoding="utf-8") as f:
                if containers:
                    fieldnames = [
                        "container_id",
                        "ship_name",
                        "origin_port",
                        "destination_port",
                        "cargo_type",
                        "weight_kg",
                        "status",
                        "eta",
                        "priority",
                        "progress_percent",
                        "crane_assigned",
                        "temperature_controlled",
                        "customs_cleared",
                    ]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()

                    for container in containers:
                        writer.writerow(
                            {
                                "container_id": container.container_id,
                                "ship_name": container.ship_name,
                                "origin_port": container.origin_port,
                                "destination_port": container.destination_port,
                                "cargo_type": container.cargo_type.value,
                                "weight_kg": container.weight_kg,
                                "status": container.status.value,
                                "eta": container.eta.isoformat(),
                                "priority": container.priority.value,
                                "progress_percent": container.progress_percent,
                                "crane_assigned": container.crane_assigned,
                                "temperature_controlled": container.temperature_controlled,
                                "customs_cleared": container.customs_cleared,
                            }
                        )
        except Exception as e:
            print(f"Error guardando contenedores: {e}")

    def _save_ships(self, ships: List[Ship]):
        """Guardar barcos en CSV"""
        try:
            with open(self.ships_file, "w", newline="", encoding="utf-8") as f:
                if ships:
                    fieldnames = [
                        "ship_id",
                        "name",
                        "captain",
                        "origin_port",
                        "containers_count",
                        "max_capacity",
                        "current_status",
                        "eta_chancay",
                    ]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()

                    for ship in ships:
                        writer.writerow(
                            {
                                "ship_id": ship.ship_id,
                                "name": ship.name,
                                "captain": ship.captain,
                                "origin_port": ship.origin_port,
                                "containers_count": ship.containers_count,
                                "max_capacity": ship.max_capacity,
                                "current_status": ship.current_status,
                                "eta_chancay": ship.eta_chancay.isoformat(),
                            }
                        )
        except Exception as e:
            print(f"Error guardando barcos: {e}")
