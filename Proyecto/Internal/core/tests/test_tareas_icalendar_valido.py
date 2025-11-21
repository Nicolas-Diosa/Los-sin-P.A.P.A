"""
TEST: icalendar_valido

Objetivo:
---------
Verificar que un texto tenga el formato válido de recurrencia iCalendar RRULE.
Debe comenzar con FREQ= seguido de un valor válido (DAILY, WEEKLY, MONTHLY, YEARLY)
y opcionalmente otros parámetros separados por punto y coma.

Casos límite:
-------------
- FREQ=DAILY → válido
- FREQ=WEEKLY → válido
- FREQ=MONTHLY → válido
- FREQ=YEARLY → válido
- FREQ=DAILY;INTERVAL=1 → válido
- FREQ=WEEKLY;BYDAY=MO,WE → válido
- FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=15 → válido
- texto sin FREQ= → inválido
- FREQ con valor inválido → inválido
- texto aleatorio → inválido
- string vacío → inválido
- `None` → inválido
Ejecutar con pytest .\Proyecto\Internal\core\tests\test_tareas_icalendar_valido.py
"""

import pytest

from core.Negocio.tareas import icalendar_valido


@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("FREQ=DAILY", True),
        ("FREQ=WEEKLY", True),
        ("FREQ=MONTHLY", True),
        ("FREQ=YEARLY", True),
        ("FREQ=DAILY;INTERVAL=1", True),
        ("FREQ=WEEKLY;BYDAY=MO,WE", True),
        ("FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=15", True),
        ("FREQ=WEEKLY;BYDAY=MO,WE,FR", True),
        ("FREQ=INVALID", False),
        ("random text", False),
        ("BEGIN:VCALENDAR", False),
        ("", False),
        (None, False),
    ],
)
def test_icalendar_valido(texto, esperado):
    assert icalendar_valido(texto) == esperado
