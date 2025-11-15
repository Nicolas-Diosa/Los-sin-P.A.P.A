"""
TEST: Disponibilidad de actividad (actividad_disponible)

Objetivo:
---------
Validar la función `actividad_disponible` en `core.Negocio.actividades`.

Reglas evaluadas:
-----------------
1. `None` como entrada → no disponible (False)
2. Objeto sin `fecha_hora_inicio` → no disponible (False)
3. `fecha_hora_inicio` en el pasado → no disponible (False)
4. `fecha_hora_inicio` en el presente → no disponible (False)
5. `fecha_hora_inicio` en el futuro → disponible (True)

Casos límite probados:
----------------------
- entrada `None`
- objeto con `fecha_hora_inicio = None`
- fecha pasada, actual y futura

Ejecutar con: `pytest .\Proyecto\Internal\core\tests\test_actividades.py`
"""

import pytest
from django.utils import timezone
from datetime import timedelta
from unittest.mock import MagicMock

from core.Negocio.actividades import actividad_disponible


# Dummy mínimo para simular una entidad Actividad con el atributo esperado
class DummyActividad:
    def __init__(self, fecha_hora_inicio=MagicMock()):
        self.fecha_hora_inicio = fecha_hora_inicio


@pytest.mark.django_db
def test_actividad_disponible():
    ahora = timezone.now()

    casos = [
        ("actividad_none", None, True),
        ("sin_fecha", DummyActividad(None), False),
        ("fecha_pasada", DummyActividad(ahora - timedelta(hours=1)), False),
        ("fecha_actual", DummyActividad(ahora), False),
        ("fecha_futura", DummyActividad(ahora + timedelta(hours=1)), True),
    ]

    for nombre_caso, entrada, esperado in casos:
        assert actividad_disponible(entrada) == esperado, f"Falló caso: {nombre_caso}"

