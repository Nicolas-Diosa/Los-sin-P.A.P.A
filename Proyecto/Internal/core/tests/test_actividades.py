from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from ..Negocio.actividades import actividad_disponible

# Dummy para simular el modelo Actividad
class DummyActividad:
    def __init__(self, fecha_hora_inicio=None):
        self.fecha_hora_inicio = fecha_hora_inicio

class TestActividadDisponible(TestCase):

    def test_actividad_disponible(self):
        ahora = timezone.now()

        # DICCIONARIO ÚNICO solicitado
        casos = [
            ("actividad_none", False),
            ("sin_fecha", False),
            ("fecha_pasada", False),
            ("fecha_actual", False),
            ("fecha_futura", True),
        ]

        for nombre_caso, esperado in casos:

            # Construcción dinámica del caso según la clave del diccionario
            if nombre_caso == "actividad_none":
                entrada = None

            elif nombre_caso == "sin_fecha":
                # Objeto sin atributo fecha_hora_inicio
                entrada = DummyActividad()

            elif nombre_caso == "fecha_pasada":
                entrada = DummyActividad(ahora - timedelta(hours=1))

            elif nombre_caso == "fecha_actual":
                entrada = DummyActividad(ahora)

            elif nombre_caso == "fecha_futura":
                entrada = DummyActividad(ahora + timedelta(hours=1))

            else:
                raise ValueError(f"Caso no reconocido: {nombre_caso}")

            with self.subTest(caso=nombre_caso):
                self.assertEqual(actividad_disponible(entrada), esperado)



# Ejecutar con: `python manage.py test core.tests.test_actividades` o `python manage.py test` 
