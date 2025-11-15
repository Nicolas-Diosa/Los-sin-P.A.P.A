"""
TEST: icalendar_valido

Objetivo:
---------
Verificar que un texto tenga el formato mínimo esperado de iCalendar
conteniendo `BEGIN:VCALENDAR` y `END:VCALENDAR`.

Casos límite:
-------------
- calendario completo con evento → válido
- calendario vacío (`BEGIN:VCALENDAR` / `END:VCALENDAR`) → válido
- solo evento (`BEGIN:VEVENT` / `END:VEVENT`) → inválido
- texto aleatorio → inválido
- `None` → inválido
"""

import pytest

from core.Negocio.tareas import icalendar_valido


@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("BEGIN:VCALENDAR\nBEGIN:VEVENT\nEND:VEVENT\nEND:VCALENDAR", True),
        ("BEGIN:VCALENDAR\nEND:VCALENDAR", True),
        ("BEGIN:VEVENT\nEND:VEVENT", False),
        ("random text", False),
        (None, False),
    ],
)
def test_icalendar_valido(texto, esperado):
    assert icalendar_valido(texto) == esperado
