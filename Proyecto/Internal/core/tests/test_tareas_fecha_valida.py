"""
TEST: fecha_valida

Objetivo:
---------
Probar la validación de la fecha de una tarea: la fecha debe estar en el futuro.

Casos límite:
-------------
- fecha en el pasado (`datetime.now() - timedelta(minutes=1)`) → inválido
- fecha exactamente ahora (`datetime.now()`) → inválido
- fecha inmediatamente en el futuro (`datetime.now() + timedelta(minutes=1)`) → válido
- fecha en formato ISO en el futuro → válido
- texto no parseable (`"not-a-date"`) → inválido
- `None` → inválido
Ejecutar con pytest .\Proyecto\Internal\core\tests\test_tareas_fecha_valida.py
"""

import pytest
from datetime import datetime, timedelta

from core.Negocio.tareas import fecha_valida


@pytest.mark.parametrize(
    "valor, esperado",
    [
        (datetime.now() - timedelta(minutes=1), False),
        (datetime.now(), False),
        (datetime.now() + timedelta(minutes=1), True),
        ((datetime.now() + timedelta(days=1)), True),
        ("not-a-date", False),
        (None, False),
    ],
)
def test_fecha_valida(valor, esperado):
    assert fecha_valida(valor) == esperado
