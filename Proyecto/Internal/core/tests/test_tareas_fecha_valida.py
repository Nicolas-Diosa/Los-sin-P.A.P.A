"""
TEST: fecha_valida

Objetivo:
---------
Probar la validación de la fecha de una tarea: la fecha debe estar en el futuro.

Casos límite:
-------------
- fecha en el pasado (`timezone.now() - timedelta(minutes=1)`) → inválido
- fecha exactamente ahora (`timezone.now()`) → inválido
- fecha inmediatamente en el futuro (`timezone.now() + timedelta(minutes=1)`) → válido
- fecha en formato ISO en el futuro → válido
- texto no parseable (`"not-a-date"`) → inválido
- `None` → inválido
"""

import pytest
from django.utils import timezone
from datetime import timedelta

from core.Negocio.tareas import fecha_valida


@pytest.mark.parametrize(
    "valor, esperado",
    [
        (timezone.now() - timedelta(minutes=1), False),
        (timezone.now(), False),
        (timezone.now() + timedelta(minutes=1), True),
        ((timezone.now() + timedelta(days=1)).isoformat(), True),
        ("not-a-date", False),
        (None, False),
    ],
)
def test_fecha_valida(valor, esperado):
    assert fecha_valida(valor) == esperado
