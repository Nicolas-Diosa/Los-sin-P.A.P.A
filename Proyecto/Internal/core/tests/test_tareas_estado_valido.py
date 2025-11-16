"""
TEST: estado_valido

Objetivo:
---------
Validar que el estado de una tarea sea uno de los valores permitidos:
`Por realizar`, `Realizando`, `Realizada`.

Casos límite:
-------------
- valores permitidos en caso correcto → válido
- mismo texto en distinto case (`por realizar`) → inválido
- valores en otro idioma (`Completed`) → inválido
- `None` → inválido
"""

import pytest

from core.Negocio.tareas import estado_valido


@pytest.mark.parametrize(
    "estado, esperado",
    [
        ("Por realizar", True),
        ("Realizando", True),
        ("Realizada", True),
        ("por realizar", False),
        ("Completed", False),
        (None, False),
    ],
)
def test_estado_valido(estado, esperado):
    assert estado_valido(estado) == esperado
