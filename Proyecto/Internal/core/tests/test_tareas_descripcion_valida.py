"""
TEST: descripcion_valida

Objetivo:
---------
Probar la validación de la descripción de una tarea: debe aceptar
textos de longitud entre 0 y 280 caracteres inclusive.

Casos límite:
-------------
- cadena vacía (`""`) → válido
- 1 carácter (`"a"`) → válido
- límite superior (`"a" * 280`) → válido
- justo por encima del límite (`"a" * 281`) → inválido
- tipo no-string (`123`) → inválido
- `None` → inválido
"""

import pytest

from core.Negocio.tareas import descripcion_valida


@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("", True),
        ("a", True),
        ("a" * 280, True),
        ("a" * 281, False),
        (123, False),
        (None, False),
    ],
)
def test_descripcion_valida(texto, esperado):
    assert descripcion_valida(texto) == esperado
