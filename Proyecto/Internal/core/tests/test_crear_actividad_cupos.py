"""
TEST: Validación del campo 'cupos' en ActividadService.crear_actividad

Objetivo:
---------
Validar que la capa de negocio rechace cupos inválidos y acepte cupos válidos.

Reglas evaluadas:
-----------------
1. cupos < 0 → inválido
2. cupos = 0 → válido (permite actividades sin cupos)
3. cupos > 0 → válido
4. cupos no numérico → inválido
5. cupos vacío → inválido

Casos límite probados:
----------------------
- -5      → inválido
- 0       → válido
- 10      → válido
- ""      → inválido
- "abc"   → inválido

Técnicas de testeo:
-------------------
- pytest + pytest-django
- uso de unittest.mock.patch para reemplazar DB_Manager y evitar acceso a la BD
- validación con pytest.raises en casos inválidos
"""

import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from datetime import timedelta

from core.Negocio.actividad_service import ActividadService


@pytest.mark.django_db
def test_crear_actividad_cupos():

    # Parcheamos DB_Manager para evitar consultas reales
    with patch("core.Negocio.actividad_service.DB_Manager") as MockDB:

        mock_db = MockDB.return_value

        # Mock del usuario retornado por la base de datos
        mock_usuario = MagicMock()
        mock_db.get_usuario_by_nombre_usuario.return_value = mock_usuario

        # Mock de creación de actividad
        mock_db.create_actividad.return_value = MagicMock()

        service = ActividadService()
        request = MagicMock()
        request.session = {"username": "testuser"}

        ahora = timezone.now()

        casos = [
            (-5, False),
            (0, True),
            (10, True),
            ("", False),
            ("abc", False),
        ]

        for cupos_caso, esperado in casos:

            datos = {
                "nombre_actividad": "Prueba Cupos",
                "descripcion": "Test",
                "categoria": "Ensayo",
                "ubicacion": "Salón",
                "fecha_hora_inicio": (ahora + timedelta(hours=1)).isoformat(),
                "fecha_hora_fin": (ahora + timedelta(hours=2)).isoformat(),
                "cupos": cupos_caso,
            }

            if not esperado:
                # Si es caso inválido → debe lanzar excepción
                with pytest.raises(ValueError):
                    service.crear_actividad(request, datos)

            else:
                # Si es válido → no debe lanzar error
                service.crear_actividad(request, datos)
                mock_db.create_actividad.assert_called()
