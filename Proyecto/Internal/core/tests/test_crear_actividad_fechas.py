"""
TEST: Validación de fechas en ActividadService.crear_actividad

Reglas probadas:
----------------
1. La fecha de inicio es obligatoria.
2. La fecha de fin es obligatoria.
3. La fecha de fin debe ser mayor que la fecha de inicio.

Casos límite:
-------------
- falta fecha inicio      → inválido
- falta fecha fin         → inválido
- fecha fin < inicio      → inválido
- fecha fin = inicio      → inválido
- rango válido            → válido
"""

import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from datetime import timedelta

from core.Negocio.actividad_service import ActividadService


@pytest.mark.django_db
def test_crear_actividad_fechas():

    with patch("core.Negocio.actividad_service.DB_Manager") as MockDB:

        mock_db = MockDB.return_value

        # Mock usuario creador
        mock_usuario = MagicMock()
        mock_db.get_usuario_by_nombre_usuario.return_value = mock_usuario

        # Mock creación de actividad
        mock_db.create_actividad.return_value = MagicMock()

        service = ActividadService()

        request = MagicMock()
        request.session = {"username": "testuser"}

        ahora = timezone.now()

        casos = [
            (None, ahora.isoformat(), False),   # Falta inicio
            (ahora.isoformat(), None, False),   # Falta fin
            (ahora.isoformat(), (ahora - timedelta(hours=1)).isoformat(), False), # Fin antes de inicio
            (ahora.isoformat(), ahora.isoformat(), False), # Fin = inicio
            (ahora.isoformat(), (ahora + timedelta(hours=1)).isoformat(), True),  # Correcto
        ]

        for fecha_inicio, fecha_fin, valido in casos:

            datos = {
                "nombre_actividad": "Test Fechas",
                "descripcion": "Test",
                "categoria": "Ensayo",
                "ubicacion": "Salón",
                "fecha_hora_inicio": fecha_inicio,
                "fecha_hora_fin": fecha_fin,
                "cupos": 5,
            }

            if not valido:
                with pytest.raises(Exception):
                    service.crear_actividad(request, datos)
            else:
                service.crear_actividad(request, datos)
                mock_db.create_actividad.assert_called()
