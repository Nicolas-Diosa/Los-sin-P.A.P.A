"""
TEST: prioridad_valida

Objetivo:
---------
Comprobar que la función `prioridad_valida` acepte únicamente los
números `1`, `2` o `3` como prioridad.

Casos límite:
-------------
- `1`, `2`, `3` → válidos
- `0`, `4`, `-1` → inválidos
- valores no enteros (`"1"`, `1.0`) → inválidos
- `None` → inválido
Ejecutar con pytest .\Proyecto\Internal\core\tests\test_tareas_prioridad_valida.py
"""

import pytest

from core.Negocio.tareas import prioridad_valida


@pytest.mark.parametrize(
    "valor, esperado",
    [
        (1, True),
        (2, True),
        (3, True),
        (0, False),
        (4, False),
        (-1, False),
        ("1", False),
        (1.0, False),
        (None, False),
    ],
)
def test_prioridad_valida(valor, esperado):
    assert prioridad_valida(valor) == esperado
