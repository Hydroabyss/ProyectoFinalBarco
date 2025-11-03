"""
Integración de Maxsurf con Python
=================================

Este paquete proporciona herramientas para automatizar tareas en Maxsurf
utilizando la API COM de Windows.

Módulos:
    - maxsurf_connector: Conexión básica con Maxsurf
    - hull_design: Diseño y parametrización de cascos
    - stability: Análisis de estabilidad
    - tanks: Diseño y cubicación de tanques
    - reports: Generación de reportes

Autor: Proyecto Final - Diseño Naval
Fecha: 2 de noviembre de 2025
"""

__version__ = "1.0.0"
__author__ = "Proyecto Final - Diseño Naval"

from .maxsurf_connector import MaxsurfConnector
from .hull_design.hull_designer import HullDesigner
from .stability.stability_analyzer import StabilityAnalyzer
from .tanks.tank_designer import TankDesigner
from .reports.report_generator import ReportGenerator

def _cli_ping():
    """CLI mínima: informa backend y una hidro estática simple."""
    c = MaxsurfConnector(visible=False)
    ok = c.connect()
    print({
        'connected': ok and c.is_connected(),
        'mock': getattr(c, '_is_mock', False)
    })
    c.set_length(12.0); c.set_beam(3.8); c.set_draft(1.8)
    print(c.run_hydrostatics())

if __name__ == '__main__':
    _cli_ping()

__all__ = [
    'MaxsurfConnector',
    'HullDesigner',
    'StabilityAnalyzer',
    'TankDesigner',
    'ReportGenerator'
]
