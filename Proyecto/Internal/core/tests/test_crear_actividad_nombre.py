"""
TEST: Validación del nombre de actividad en ActividadService

Objetivo:
---------
Validar que la lógica de negocio para crear actividades (ActividadService.crear_actividad)
aplique correctamente las reglas sobre el nombre de la actividad.

Casos límite probados:
----------------------
1. Nombre vacío ("") → debe rechazarlo (no es válido)
2. Nombre muy corto ("A") → debe rechazarlo
3. Nombre numérico ("12345") → debe rechazarlo
4. Nombre válido simple ("Mi actividad") → debe aceptarlo
5. Nombre válido largo ("Actividad deportiva") → debe aceptarlo

Técnicas empleadas:
-------------------
- Uso de pytest + pytest-django.
- Uso de `unittest.mock.patch` para reemplazar DB_Manager con un mock
  y evitar interacción real con la base de datos.
- Validación de excepciones cuando el nombre es inválido.
- Validación de que `create_actividad` se llama cuando los datos son válidos.

Este test es esencial en el sistema porque garantiza que la creación
de actividades cumpla con las reglas de negocio antes de intentar guardar
en la base de datos.
"""

import pytest
from unittest.mock import MagicMock, patch
from django.utils import timezone
from datetime import timedelta

from core.Negocio.actividad_service import ActividadService


@pytest.mark.django_db
def test_crear_actividad_nombre():

    # Parcheamos DB_Manager dentro del servicio
    with patch("core.Negocio.actividad_service.DB_Manager") as MockDB:

        mock_db = MockDB.return_value

        # Mock del usuario obtenido desde la BD
        mock_usuario = MagicMock()
        mock_db.get_usuario_by_nombre_usuario.return_value = mock_usuario

        # Mock de creación de actividad (para evitar insert real en BD)
        mock_db.create_actividad.return_value = MagicMock()

        # Instanciamos el servicio
        service = ActividadService()

        # Mock del request con sesión
        request = MagicMock()
        request.session = {"username": "testuser"}

        ahora = timezone.now()

        # Casos límite
        casos = [
            ("", False),                      # Nombre vacío → inválido
            ("Mi actividad", True),           # Válido
            ("A", False),                     # Muy corto → inválido
            ("12345", False),                 # Numérico → inválido
            ("Actividad deportiva", True),    # Válido
        ]

        for nombre_caso, esperado in casos:

            datos = {
                "nombre_actividad": nombre_caso,
                "descripcion": "Algo",
                "categoria": "Ocio",
                "ubicacion": "Canchas",
                "fecha_hora_inicio": (ahora + timedelta(hours=1)).isoformat(),
                "fecha_hora_fin": (ahora + timedelta(hours=2)).isoformat(),
                "cupos": 10,
            }

            if not esperado:
                # Si se espera que falle → debe lanzar excepción
                with pytest.raises(Exception):
                    service.crear_actividad(request, datos)
            else:
                # Si es válido → NO debe lanzar excepción
                service.crear_actividad(request, datos)
                mock_db.create_actividad.assert_called()
